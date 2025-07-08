# tools/task_processor.py

import sqlite3
import json
from typing import Dict, List
from google.adk.tools import FunctionTool

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
    creator_user_id: str = "",
) -> Dict[str, str]:
    creator_user_id = "user_originator"
    form_data = {
        k: v for k, v in {
            "employee_name": employee_name,
            "department": department,
            "laptop_model": laptop_model,
            "ram": ram,
            "meeting_topic": meeting_topic,
            "proposed_time": proposed_time,
            "trip_destination": trip_destination,
            "flight_cost": flight_cost,
            "hotel_cost": hotel_cost
        }.items() if v
    }

    print("🔧 [process_task] Creating task with data:", task_description, form_data)

    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    approval_status = "Pending" if requires_approval else "AutoApproved"
    cursor.execute(
        """
        INSERT INTO tasks (task_description, form_data, requires_approval, approval_status, creator_user_id)
        VALUES (?, ?, ?, ?, ?)
        """,
        (task_description, json.dumps(form_data), requires_approval, approval_status, creator_user_id)
    )

    task_id = cursor.lastrowid
    message = "✅ Task created successfully."

    if requires_approval:
        for approver in approvers:
            cursor.execute(
                """
                INSERT INTO approvers (task_id, approver_email, approver_status)
                VALUES (?, ?, ?)
                """,
                (task_id, approver, "Pending")
            )
        message = "✅ Task created and sent to approvers."

    conn.commit()
    conn.close()

    return {"status": message}

process_task_tool = FunctionTool(func=process_task)
