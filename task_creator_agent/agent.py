from dotenv import load_dotenv
from google.adk.agents import LlmAgent, Agent
from task_creator_agent.prompts import agent_prompts
from task_creator_agent.tools.task_processor import process_task

load_dotenv()

root_agent = LlmAgent(
    name="task_creator_agent",
    model="gemini-1.5-flash-latest",
    description=(
        "An intelligent assistant that helps create and manage tasks based on user requests."
    ),
    instruction=agent_prompts.TASK_CREATOR_AGENT_PROMPT,
    tools=[process_task],
)
