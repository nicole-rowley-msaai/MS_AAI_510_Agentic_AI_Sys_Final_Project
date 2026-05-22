# MS_AAI_510_Agentic_AI_Sys_Final_Project
Custom AI Agent with Technical and Business Artifacts

Team members: 
Product Manager (PM)
Data Engineer (DE)
AI Engineer (AIE)

Your responsibility as a team is to develop a project plan and deliver an AI Agent for your company. Can split up roles distinctly within the team, or share the responsibilities of each role across the team. The AIE likely has more responsibilities than the DE, so sharing those responsibilities might make the most sense. This project will involve two stages:

Part A: Agent Deliverable - Technical Artifacts
A notebook that contains your data pipeline (DE is the owner)
A notebook that shows your agent definition (AIE is the owner)
Review the rubric to determine agent requirements.
An example of five traces, including the evaluation of the agent (AIE is the owner)
Traces should be presented via an established provider. Databricks will leverage MLflow by default; alternatives are Arize Phoenix, LangSmith, and Braintrust, among others.
There should be at least 2 different LLMs used within the agent on the same trace to compare performance (this counts as one trace per the five above).
Evaluation can be an LLM judge (strongly encouraged) or manual.
Provide commentary in a notebook cell that talks about the agent performance, and what the evaluation showed, including a comparison between the agent using different LLMs.
Show 2 examples of the agent gracefully rejecting an irrelevant user input.
This agent fits the definition of an agent in the course, meaning it must leverage an LLM and relevant tooling, which can be MCP servers, custom functions, vector search indices, etc.

Part B: Agent Deliverable - Business Artifacts
A 10-15 minute video presentation that does the following:
Use the notebook for this portion and slides for the rest.
You must describe how a human is involved in the evaluation process.
You can also use a notebook for this portion if it is easier.
This should include an explicit ROI calculation for the different LLMs chosen.
  Ex. if LLM 1 costs 2x LLM 2, and LLM 1 is 20% more effective than LLM 2, what is the ROI of leveraging each LLM based on the business value associated with that 20% increase in effectiveness?
Note: the deployment is not a mandatory part of the solution.
If you deviated from your plan, describe why.
Walks through the technical solution.
Describes how the solution was evaluated with example evaluations.
Describes the final business value of the solution.
Recommends how the agent would be deployed.
Opinionated commentary about the quality of the agent. Did it exceed expectations? What was it good at? What was it bad at? What did you learn about building agents in this process?
PM is the owner, but everyone must participate in the video.

Bay Day 7 of Week 7, submit your final project as:
A file upload of your GitHub repository
A file upload of your video presentation

Grading Rubric:
Data Pipeline Code (10%) - Data pipeline code executes and extracts data needed for the use case.
Agent Code (25%) - Agent Code includes an LLM, at least two tools, is not missing obvious tools that would be useful for the agent, and can gracefully handles errors and out of scope user queries.
Evaluation Examples (15%) - 5 evaluation examples are shown including at least one trace that has different LLMs. Written description articulates how the agent is performing.
Video Presentation (50%) - No AI Usage: All team members participate, the technical solution overview includes relevant details and covers evaluation. The business value is articulated, and there is a recommendation on deployment. The opinionated commentary is thoughtful, and everyone on the team participates.
