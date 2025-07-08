from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from prompts import agent_prompts

# ✅ Import wrapped tool instances
from tools.task_processor import process_task_tool
from tools.check_and_close_tasks import check_and_close_tasks_tool

load_dotenv()

root_agent = LlmAgent(
    name="task_creator_agent",
    model="gemini-2.0-flash",
    description="An intelligent assistant that creates or updates tasks based on user input.",
    instruction=agent_prompts.TASK_ROUTER_PROMPT,
    tools=[process_task_tool, check_and_close_tasks_tool]  # ✅ Correct tool objects
)
