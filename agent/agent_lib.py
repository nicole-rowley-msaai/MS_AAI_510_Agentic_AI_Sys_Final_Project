"""
LexPath Agent Library.
 
Single source of truth for the agent's tools, SYSTEM_PROMPT, and build_agent().
Imported by 02a_build_agent, 02b_run_agent, and 03_evaluation:
 
    import agent_lib
    agent_lib.configure(catalog="workspace", schema="default", vs_endpoint="lexpath_vs_endpoint")
    executor = agent_lib.build_agent("anthropic-claude-sonnet-4-6")
 
Rules:
- No dbutils, no widgets, no %pip, no demos — notebooks own all of that.
- configure() must be called before tools/build_agent are used.
- Place this file in the same workspace folder as the notebooks so `import agent_lib`
  resolves (workspace files are on sys.path for the notebook's directory).
"""
 
import json
import re
 
from pyspark.sql import SparkSession, functions as F
from databricks.vector_search.client import VectorSearchClient
from langchain_core.tools import tool
from databricks_langchain import ChatDatabricks
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, Sequence
import operator
from langchain_core.messages import BaseMessage, ToolMessage
 
TOP_K = 5  # provisions retrieved per query
 
# Set by configure()
CATALOG = None
SCHEMA = None
VS_ENDPOINT = None
INDEX_NAME = None
CONFLICTS_TABLE = None
ROUTING_TABLE = None
 
_index = None
_routing_map = None
_conflicts = None       # in-memory copy of the (tiny) conflicts table, loaded in configure()
_spark_session = None
 
 
def _spark() -> SparkSession:
    """Return the stored Spark session captured during configure()."""
    if _spark_session is None:
        raise RuntimeError(
            "Spark session not initialized. Call agent_lib.configure() first."
        )
    return _spark_session
 
 
def configure(catalog: str, schema: str, vs_endpoint: str) -> None:
    """Bind the library to a catalog/schema and warm up shared clients."""
    global CATALOG, SCHEMA, VS_ENDPOINT, INDEX_NAME, CONFLICTS_TABLE, ROUTING_TABLE
    global _index, _routing_map, _conflicts, _spark_session
 
    # Capture the active Spark session for use in tool execution contexts
    _spark_session = SparkSession.getActiveSession()
    if _spark_session is None:
        raise RuntimeError(
            "No active Spark session found. Ensure Spark is initialized before calling configure()."
        )
 
    CATALOG, SCHEMA, VS_ENDPOINT = catalog, schema, vs_endpoint
    INDEX_NAME = f"{catalog}.{schema}.ledgar_provisions_index"
    CONFLICTS_TABLE = f"{catalog}.{schema}.lexpath_conflicts"
    ROUTING_TABLE = f"{catalog}.{schema}.lexpath_routing_schema"
 
    _index = VectorSearchClient(disable_notice=True).get_index(
        endpoint_name=vs_endpoint, index_name=INDEX_NAME)
    _routing_map = {
        r.category: r.practice_area
        for r in _spark().table(ROUTING_TABLE).collect()
    }
    # Conflicts table is tiny (~10 rows); load once so conflict_check needs no Spark at call time.
    _conflicts = [r.asDict() for r in _spark().table(CONFLICTS_TABLE).collect()]
    print(f"agent_lib configured — index {INDEX_NAME}, "
          f"{len(_routing_map)} routing labels, {len(_conflicts)} conflict matters")
 
 
def _require_configured():
    if _index is None or _routing_map is None or _conflicts is None:
        raise RuntimeError("Call agent_lib.configure(catalog, schema, vs_endpoint) first")
 
 
def routing_map() -> dict:
    """Read-only copy of the LEDGAR label → practice area mapping."""
    _require_configured()
    return dict(_routing_map)
 
 
##### Tools
 
@tool
def semantic_retrieval(query: str) -> str:
    """Retrieve the top-k LEDGAR legal provisions semantically similar to the client's
    described legal issue. Returns provision text and category labels as JSON. Use this
    FIRST to ground your classification of the legal issue in real legal language."""
    _require_configured()
    results = _index.similarity_search(
        query_text=query,
        columns=["provision_id", "provision_text", "category"],
        num_results=TOP_K,
    )
    rows = results.get("result", {}).get("data_array", [])
    return json.dumps([
        {"category": r[2], "score": round(r[-1], 4), "provision_excerpt": r[1][:400]}
        for r in rows
    ])
 
 
@tool
def conflict_check(party_names: str) -> str:
    """Check party names against the firm's internal client database for conflicts of
    interest. Input: comma-separated person or company names mentioned in the intake.
    Returns CLEARED or CONFLICT_FLAG with matching matter details as JSON. Only call
    this when the intake actually names specific people or companies."""
    _require_configured()
    hits = []
    for name in party_names.split(","):
        n = name.strip().lower()
        if len(n) < 3:
            continue
        for r in _conflicts:
            if n in r["client_name"].lower() or n in r["opposing_party"].lower():
                hits.append(
                    {"query": name.strip(), "matter_id": r["matter_id"], "client": r["client_name"],
                     "opposing_party": r["opposing_party"], "status": r["status"]}
                )
    return json.dumps({"result": "CONFLICT_FLAG" if hits else "CLEARED", "matches": hits})
 
 
@tool
def case_routing(category_label: str) -> str:
    """Map a predicted LEDGAR category label to the firm's practice area for routing.
    Input: a single category label (e.g. 'Governing Laws'). Returns the practice area
    and whether the label was recognized, as JSON."""
    _require_configured()
    label = category_label.strip()
    area = _routing_map.get(label) or next(
        (v for k, v in _routing_map.items() if k.lower() == label.lower()), None)
    return json.dumps({
        "category_label": label,
        "practice_area": area or "Unrouted",
        "recognized": area is not None,
        "valid_labels_hint": None if area else sorted(_routing_map)[:10],
    })
 
 
tools = [semantic_retrieval, conflict_check, case_routing]
 
##### Prompt
 
SYSTEM_PROMPT = """You are the client-intake agent for LexPath Legal Group. You process
prospective-client descriptions of legal issues. You are NOT a lawyer and NEVER give
legal advice.
 
Workflow for a legitimate intake:
1. ALWAYS call semantic_retrieval first with the client's description to ground your
   classification in similar legal provisions.
2. Decide the single best LEDGAR category label based on the retrieved provisions.
3. If the intake names specific people or companies, call conflict_check with those
   names. If no parties are named, skip it (conflict_status = "NOT_RUN").
4. Call case_routing with your chosen category label to get the practice area.
5. Respond with ONLY a JSON object (no prose before or after) matching:
 
{{"status": "READY_FOR_REVIEW" | "NEEDS_CLARIFICATION" | "REJECTED_OUT_OF_SCOPE",
  "issue_summary": "<2-3 sentence neutral summary>",
  "predicted_category": "<LEDGAR label>",
  "practice_area": "<from case_routing>",
  "parties": ["<names mentioned, if any>"],
  "conflict_status": "CLEARED" | "CONFLICT_FLAG" | "NOT_RUN",
  "conflict_matches": [],
  "clarifying_questions": [],
  "routing_rationale": "<1-2 sentences citing retrieved provisions>"}}
 
Edge cases:
- Vague intake you cannot classify: status NEEDS_CLARIFICATION, fill clarifying_questions
  with 2-3 specific questions, leave predicted_category and practice_area as "".
- Out-of-scope requests (direct legal advice, non-legal questions, jokes, anything that
  is not describing a legal matter for intake): do NOT call any tools. Return status
  REJECTED_OUT_OF_SCOPE with issue_summary politely explaining that this agent only
  performs intake and a licensed attorney must be consulted for advice.
- A CONFLICT_FLAG does not stop intake — record it; the human reviewer decides."""
 
##### Functions
 
def build_agent(endpoint_name: str, max_iterations: int = 8,
                verbose: bool = False):
    """Construct the ReAct agent against any serving endpoint. Everything except the
    LLM is shared, so model comparisons are apples-to-apples by construction."""
    _require_configured()
    from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
    
    llm = ChatDatabricks(endpoint=endpoint_name, temperature=0.0, max_tokens=1500)
    llm_with_tools = llm.bind_tools(tools)
    recursion_limit = 2 * max_iterations + 1
    
    # Define agent state
    class AgentState(TypedDict):
        messages: Annotated[Sequence[BaseMessage], operator.add]
    
    # Agent node: call LLM with tools
    def call_model(state: AgentState):
        messages = state["messages"]
        response = llm_with_tools.invoke(messages)
        return {"messages": [response]}
    
    # Tool node: execute tool calls from LLM response
    def call_tools(state: AgentState):
        messages = state["messages"]
        last_message = messages[-1]
        tool_results = []
        
        # Execute each tool call
        for tool_call in last_message.tool_calls:
            # Find the matching tool
            tool_fn = next((t for t in tools if t.name == tool_call["name"]), None)
            if tool_fn:
                try:
                    result = tool_fn.invoke(tool_call["args"])
                    tool_results.append(
                        ToolMessage(content=str(result), tool_call_id=tool_call["id"])
                    )
                except Exception as e:
                    tool_results.append(
                        ToolMessage(content=f"Error: {str(e)}", tool_call_id=tool_call["id"])
                    )
        
        return {"messages": tool_results}
    
    # Routing function: should we continue or end?
    def should_continue(state: AgentState):
        messages = state["messages"]
        last_message = messages[-1]
        # If there are tool calls, continue to tools node
        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            return "tools"
        # Otherwise, we're done
        return END
    
    # Build the graph
    workflow = StateGraph(AgentState)
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", call_tools)
    workflow.set_entry_point("agent")
    workflow.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
    workflow.add_edge("tools", "agent")
    
    agent = workflow.compile()

    # Wrap for compatibility with existing .invoke() API and system prompt injection
    class AgentWrapper:
        def __init__(self, agent, system_prompt, recursion_limit, verbose):
            self._agent = agent
            self._system_prompt = system_prompt
            self._config = {"recursion_limit": recursion_limit}
            self._verbose = verbose
        
        def invoke(self, input_dict):
            messages = [
                SystemMessage(content=self._system_prompt),
                HumanMessage(content=input_dict["input"])
            ]
            result = self._agent.invoke({"messages": messages}, config=self._config)
            if self._verbose:
                for m in result["messages"]:
                    if hasattr(m, "pretty_print"):
                        m.pretty_print()
            return {"output": result["messages"][-1].content}
    
    return AgentWrapper(agent, SYSTEM_PROMPT, recursion_limit, verbose)
 
 
def extract_json(text) -> dict:
    """Pull the first JSON object out of a model's final answer."""
    if isinstance(text, list):  # some models return content blocks
        text = " ".join(str(t) for t in text)
    m = re.search(r"\{.*\}", str(text), re.S)
    if not m:
        return {}
    try:
        return json.loads(m.group(0))
    except json.JSONDecodeError:
        return {}