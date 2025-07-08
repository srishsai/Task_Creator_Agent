import React, { useEffect, useState } from "react";
import axios from "axios";

const CompletedTasksPage = () => {
  const [completedTasks, setCompletedTasks] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios
      .get("http://localhost:8000/api/tasks/completed")
      .then((response) => {
        setCompletedTasks(response.data.completed_tasks);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching completed tasks:", error);
        setLoading(false);
      });
  }, []);

  return (
    <div className="max-w-6xl mx-auto py-8 px-4">
      <h1 className="text-3xl font-bold mb-6 text-gray-800">
        Completed Tasks (Approved / Rejected)
      </h1>

      {loading ? (
        <div className="text-gray-500">Loading...</div>
      ) : completedTasks.length === 0 ? (
        <p className="text-gray-600">No completed tasks found.</p>
      ) : (
        <div className="overflow-x-auto">
          <table className="min-w-full border border-gray-200 divide-y divide-gray-200">
            <thead className="bg-gray-100">
              <tr>
                <th className="px-4 py-3 text-left text-sm font-semibold text-gray-700">Task ID</th>
                <th className="px-4 py-3 text-left text-sm font-semibold text-gray-700">Task Description</th>
                <th className="px-4 py-3 text-left text-sm font-semibold text-gray-700">Approver Email</th>
                <th className="px-4 py-3 text-left text-sm font-semibold text-gray-700">Status</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-100">
              {completedTasks.map((task) => (
                <tr key={`${task.task_id}-${task.approver_email}`}>
                  <td className="px-4 py-2 text-sm text-gray-800">{task.task_id}</td>
                  <td className="px-4 py-2 text-sm text-gray-700">{task.task_description}</td>
                  <td className="px-4 py-2 text-sm text-gray-600">{task.approver_email}</td>
                  <td
                    className={`px-4 py-2 text-sm font-medium ${
                      task.approver_status === "Approved"
                        ? "text-green-600"
                        : "text-red-600"
                    }`}
                  >
                    {task.approver_status}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default CompletedTasksPage;
