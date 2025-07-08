# tools/check_and_close_tasks_tool.py

import sqlite3
from typing import Dict
from google.adk.tools import FunctionTool  # ✅ Correct import

def check_and_close_tasks(task_id: int, approver_email: str, decision: str) -> Dict[str, str]:
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    # 1. Update the approver's decision
    cursor.execute(
        """
        UPDATE approvers
        SET approver_status = ?
        WHERE task_id = ? AND approver_email = ?
        """,
        (decision, task_id, approver_email)
    )

    # 2. Fetch all approver statuses for the task
    cursor.execute(
        """
        SELECT approver_status FROM approvers WHERE task_id = ?
        """,
        (task_id,)
    )
    statuses = [row[0] for row in cursor.fetchall()]

    # 3. Determine overall approval status
    if any(status == "Rejected" for status in statuses):
        final_status = "Rejected"
    elif all(status == "Approved" for status in statuses):
        final_status = "Approved"
    else:
        final_status = "Pending"

    # 4. Update the tasks table with the final status
    cursor.execute(
        """
        UPDATE tasks
        SET approval_status = ?
        WHERE id = ?
        """,
        (final_status, task_id)
    )

    conn.commit()
    conn.close()

    return {
        "task_id": str(task_id),
        "status": f"{approver_email} marked as {decision}.",
        "final_task_approval_status": final_status
    }

# ✅ Wrap with FunctionTool so ADK agent can call it
check_and_close_tasks_tool = FunctionTool(func=check_and_close_tasks)
