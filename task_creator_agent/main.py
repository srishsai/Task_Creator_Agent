from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
import sys, os
import logging

# ---------------------------
# Logging Configuration
# ---------------------------
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

# ---------------------------
# Add current directory to sys.path
# ---------------------------
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from agent.root_agent import root_agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

APP_NAME = "task-agent"
USER_ID = "user"
SESSION_ID = "session"

session_service = InMemorySessionService()
runner = Runner(agent=root_agent, session_service=session_service, app_name=APP_NAME)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------
# Request body model
# ---------------------------
class PromptInput(BaseModel):
    prompt: str
    task_id: int | None = None
    approver_email: str | None = None

# ---------------------------
# Agent Entry Point
# ---------------------------
@app.post("/api/agent/process")
async def process_prompt(prompt_input: PromptInput):
    logger.debug("Received prompt input: %s", prompt_input)

    final_prompt = prompt_input.prompt

    # Inject context if it's an approver action
    if prompt_input.task_id is not None and prompt_input.approver_email:
        decision = "Rejected" if "reject" in final_prompt.lower() else "Approved"
        context_block = (
            f"\n\n[context] task_id={prompt_input.task_id}, "
            f"approver_email={prompt_input.approver_email}, decision={decision}"
        )
        final_prompt += context_block
        logger.debug("Injected context: %s", context_block.strip())

    logger.debug("Final prompt sent to agent: %s", final_prompt)

    # Create session
    await session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )
    logger.debug("Session created for user_id=%s, session_id=%s", USER_ID, SESSION_ID)

    content = types.Content(role="user", parts=[types.Part(text=final_prompt)])

    tool_result_text = None
    llm_response_text = None

    try:
        async for event in runner.run_async(
            user_id=USER_ID,
            session_id=SESSION_ID,
            new_message=content
        ):
            logger.debug("Received event: %s", event)

            if hasattr(event, "tool_result"):
                output = getattr(event.tool_result, "output", None)
                if not output and isinstance(event.tool_result, dict):
                    output = event.tool_result.get("output")
                if isinstance(output, dict):
                    tool_result_text = output.get("status") or str(output)
                elif output:
                    tool_result_text = str(output)
                logger.debug("Tool result received: %s", tool_result_text)

            elif hasattr(event, "content"):
                for part in event.content.parts:
                    if hasattr(part, "tool_output") and part.tool_output:
                        tool_result_text = str(part.tool_output)
                        logger.debug("Tool output from LLM: %s", tool_result_text)
                    elif hasattr(part, "function_response") and part.function_response:
                        resp = part.function_response.response
                        if isinstance(resp, dict):
                            tool_result_text = resp.get("status") or str(resp)
                        elif resp:
                            tool_result_text = str(resp)
                        logger.debug("Function response output: %s", tool_result_text)
                    elif hasattr(part, "text") and part.text:
                        llm_response_text = part.text
                        logger.debug("Text response from LLM: %s", llm_response_text)

    except Exception as e:
        logger.error("Error during agent run: %s", str(e))

    final_response = tool_result_text or llm_response_text or "⚠️ No response returned from agent."
    logger.debug("Final response to client: %s", final_response)

    return {"response": final_response}

# ---------------------------
# Fetch tasks pending approval
# ---------------------------
@app.get("/api/tasks/pending-approver")
def get_pending_approver_tasks():
    logger.debug("Fetching pending approver tasks from DB.")
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT t.id, t.task_description, a.approver_email
        FROM tasks t
        JOIN approvers a ON t.id = a.task_id
        WHERE a.approver_status = 'Pending'
    """)
    rows = cursor.fetchall()
    conn.close()

    tasks = [
        {
            "task_id": row[0],
            "task_description": row[1],
            "approver_email": row[2]
        }
        for row in rows
    ]

    logger.debug("Pending tasks fetched: %d", len(tasks))
    return {"tasks": tasks}

# ---------------------------
# Fetch tasks that are completed (approved/rejected)
# ---------------------------
@app.get("/api/tasks/completed")
def get_completed_tasks():
    logger.debug("Fetching completed tasks from DB.")
    conn = sqlite3.connect("tasks.db")
    conn.row_factory = sqlite3.Row  # Allows dict(row)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            t.id AS task_id,
            t.task_description,
            t.approval_status,
            t.creator_user_id,
            a.approver_email,
            a.approver_status
        FROM tasks t
        JOIN approvers a ON t.id = a.task_id
        WHERE t.approval_status IN ('Approved', 'Rejected')
    """)
    rows = cursor.fetchall()
    conn.close()

    tasks = [dict(row) for row in rows]

    logger.debug("Completed tasks fetched: %d", len(tasks))
    return {"completed_tasks": tasks}
