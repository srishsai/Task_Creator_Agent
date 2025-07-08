import React, { useState } from "react";
import { runAgent } from "../api";

export default function TaskForm() {
  const [prompt, setPrompt] = useState("");
  const [response, setResponse] = useState("");

  const handleSubmit = async () => {
    try {
      const data = await runAgent(prompt);
      setResponse(data.message);
    } catch (err) {
      setResponse("Error submitting task.");
    }
  };

  return (
    <div className="p-4 border rounded shadow">
      <h2 className="text-xl mb-2">Create Task</h2>
      <textarea
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        className="w-full p-2 border rounded"
        rows={4}
        placeholder="e.g., Request a new laptop for John..."
      />
      <button
        onClick={handleSubmit}
        className="mt-2 px-4 py-2 bg-blue-600 text-white rounded"
      >
        Submit
      </button>
      {response && <div className="mt-4 p-2 bg-gray-100 rounded">{response}</div>}
    </div>
  );
}
