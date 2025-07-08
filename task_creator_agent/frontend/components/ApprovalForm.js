import React, { useState } from "react";
import { runAgent } from "../api";

export default function ApprovalForm() {
  const [prompt, setPrompt] = useState("");
  const [response, setResponse] = useState("");

  const handleSubmit = async () => {
    try {
      const data = await runAgent(prompt);
      setResponse(data.message);
    } catch (err) {
      setResponse("Error submitting approval.");
    }
  };

  return (
    <div className="p-4 border rounded shadow mt-6">
      <h2 className="text-xl mb-2">Approve/Reject Task</h2>
      <textarea
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        className="w-full p-2 border rounded"
        rows={3}
        placeholder='e.g., "Approve task 2" or "Reject task 4"...'
      />
      <button
        onClick={handleSubmit}
        className="mt-2 px-4 py-2 bg-green-600 text-white rounded"
      >
        Submit
      </button>
      {response && <div className="mt-4 p-2 bg-gray-100 rounded">{response}</div>}
    </div>
  );
}
