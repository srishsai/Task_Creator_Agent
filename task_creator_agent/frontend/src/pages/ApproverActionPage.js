import React, { useEffect, useState } from "react";

const ApproverActionPage = () => {
  const [tasks, setTasks] = useState([]);
  const [selectedTaskId, setSelectedTaskId] = useState(null);
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);
  const [actionTaken, setActionTaken] = useState(false);

  const selectedTask = tasks.find((t) => t.task_id === selectedTaskId) || null;

  // Fetch approver tasks on load
  useEffect(() => {
    const fetchTasks = async () => {
      try {
        const res = await fetch("http://localhost:8000/api/tasks/pending-approver");
        const data = await res.json();
        setTasks(data.tasks || []);
      } catch (error) {
        console.error("Failed to fetch tasks:", error);
      }
    };

    fetchTasks();
  }, []);

  const handleDecision = async (decision) => {
    if (!selectedTask) return;

    setLoading(true);
    setResponse("");
    setActionTaken(false);

    try {
      const res = await fetch("http://localhost:8000/api/agent/process", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          prompt: decision === "Approved" ? "I approve this task" : "I reject this task",
          task_id: selectedTask.task_id,
          approver_email: selectedTask.approver_email,
        }),
      });

      const data = await res.json();
      setResponse(data.response || "No response.");
      setActionTaken(true);
    } catch (error) {
      console.error("Error submitting decision:", error);
      setResponse("Submission failed.");
    } finally {
      setLoading(false);
    }
  };

  const handleClose = () => {
    // Remove task from list only after showing response
    setTasks((prev) => prev.filter((t) => t.task_id !== selectedTaskId));
    setSelectedTaskId(null);
    setResponse("");
    setActionTaken(false);
  };

  return (
    <div className="max-w-5xl mx-auto mt-10 p-4 border rounded shadow-md bg-white">
      <h1 className="text-2xl font-semibold mb-6">Pending Approvals</h1>

      {tasks.length === 0 ? (
        <p className="text-gray-600">No pending tasks to approve.</p>
      ) : (
        <table className="w-full text-left border">
          <thead className="bg-gray-100">
            <tr>
              <th className="p-2 border">Select</th>
              <th className="p-2 border">Task ID</th>
              <th className="p-2 border">Description</th>
              <th className="p-2 border">Approver</th>
            </tr>
          </thead>
          <tbody>
            {tasks.map((task) => (
              <tr key={task.task_id} className={selectedTaskId === task.task_id ? "bg-blue-50" : ""}>
                <td className="p-2 border text-center">
                  <input
                    type="checkbox"
                    checked={selectedTaskId === task.task_id}
                    onChange={() =>
                      setSelectedTaskId(selectedTaskId === task.task_id ? null : task.task_id)
                    }
                    disabled={loading}
                  />
                </td>
                <td className="p-2 border">{task.task_id}</td>
                <td className="p-2 border">{task.task_description}</td>
                <td className="p-2 border">{task.approver_email}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {selectedTask && (
        <div className="mt-6">
          <h2 className="text-xl font-semibold mb-2">Submit Your Decision</h2>

          {!actionTaken ? (
            <div className="flex gap-4 mb-4">
              <button
                onClick={() => handleDecision("Approved")}
                disabled={loading}
                className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 disabled:opacity-50"
              >
                {loading ? "Processing..." : "Approve"}
              </button>
              <button
                onClick={() => handleDecision("Rejected")}
                disabled={loading}
                className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700 disabled:opacity-50"
              >
                {loading ? "Processing..." : "Reject"}
              </button>
            </div>
          ) : (
            <div className="mb-4">
              <button
                onClick={handleClose}
                className="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600"
              >
                Close
              </button>
            </div>
          )}

          {response && (
            <div className="mt-4 p-3 border rounded bg-gray-50">
              <strong>Agent Response:</strong>
              <pre className="whitespace-pre-wrap">{response}</pre>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default ApproverActionPage;
