import sqlite3
import json
from typing import Dict, List

# DB initialization
def init_db():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    # Create tasks table with approval_status
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_description TEXT,
            form_data TEXT,
            requires_approval BOOLEAN,
            approval_status TEXT DEFAULT 'Pending',
            creator_user_id TEXT
        )
    """)

    # Create approvers table with approver_status
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS approvers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INTEGER,
            approver_email TEXT,
            approver_status TEXT DEFAULT 'Pending',
            FOREIGN KEY (task_id) REFERENCES tasks (id)
        )
    """)

    conn.commit()
    conn.close()

# Initialize DB when module is loaded
init_db()

# Tool function for ADK
def process_task(
    task_description: str,
    employee_name: str = "",
    department: str = "",
    laptop_model: str = "",
    ram: str = "",
    meeting_topic: str = "",
    proposed_time: str = "",
    trip_destination: str = "",
    flight_cost: str = "",
    hotel_cost: str = "",
    requires_approval: bool = False,
    approvers: List[str] = [],
    creator_user_id: str = "user_originator"
) -> Dict[str, str]:

    # Build form_data dictionary from flattened fields
    form_data = {
        "employee_name": employee_name,
        "department": department,
        "laptop_model": laptop_model,
        "ram": ram,
        "meeting_topic": meeting_topic,
        "proposed_time": proposed_time,
        "trip_destination": trip_destination,
        "flight_cost": flight_cost,
        "hotel_cost": hotel_cost
    }

    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    # Insert into tasks table with approval_status
    approval_status = "Pending" if requires_approval else "AutoApproved"
    cursor.execute(
        """
        INSERT INTO tasks (task_description, form_data, requires_approval, approval_status, creator_user_id)
        VALUES (?, ?, ?, ?, ?)
        """,
        (task_description, json.dumps(form_data), requires_approval, approval_status, creator_user_id)
    )

    task_id = cursor.lastrowid
    message = "Task created successfully."

    # If approval required, insert approvers
    if requires_approval:
        for approver in approvers:
            cursor.execute(
                """
                INSERT INTO approvers (task_id, approver_email, approver_status)
                VALUES (?, ?, ?)
                """,
                (task_id, approver, "Pending")
            )
        message = "Task created successfully and sent to approvers."

    conn.commit()
    conn.close()

    return {"status": message}

# ----------------------------------------
# Extra function to update approver status (can be exposed later as a tool)

# def update_approver_status(task_id: int, approver_email: str, status: str) -> Dict[str, str]:
#     conn = sqlite3.connect("tasks.db")
#     cursor = conn.cursor()
# 
#     # Update approver record
#     cursor.execute("""
#         UPDATE approvers
#         SET approver_status = ?
#         WHERE task_id = ? AND approver_email = ?
#     """, (status, task_id, approver_email))
# 
#     # Check if all approvers have responded
#     cursor.execute("""
#         SELECT COUNT(*) FROM approvers
#         WHERE task_id = ? AND approver_status = 'Pending'
#     """, (task_id,))
#     pending_count = cursor.fetchone()[0]
# 
#     final_task_status = None
#     if pending_count == 0:
#         # All approvers responded, check if any rejected
#         cursor.execute("""
#             SELECT COUNT(*) FROM approvers
#             WHERE task_id = ? AND approver_status = 'Rejected'
#         """, (task_id,))
#         rejected_count = cursor.fetchone()[0]
# 
#         final_task_status = 'Rejected' if rejected_count > 0 else 'Approved'
# 
#         cursor.execute("""
#             UPDATE tasks
#             SET approval_status = ?
#             WHERE id = ?
#         """, (final_task_status, task_id))
# 
#     conn.commit()
#     conn.close()
#     return {"status": f"Approver status updated. Final task status: {final_task_status if final_task_status else 'Pending'}"}
# ----------------------------------------
