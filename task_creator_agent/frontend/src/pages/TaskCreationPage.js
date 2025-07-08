import React, { useState } from "react";

const TaskCreationPage = () => {
  const [prompt, setPrompt] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async () => {
    if (!prompt.trim()) {
      setError("Please enter a task prompt.");
      return;
    }

    setLoading(true);
    setResponse("");
    setError("");

    try {
      const res = await fetch("http://localhost:8000/api/agent/process", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ prompt }),
      });

      const data = await res.json();
      setResponse(data.response || "No response received.");
      setPrompt(""); // reset prompt
    } catch (error) {
      console.error("Error calling agent:", error);
      setResponse("Error calling the backend.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mx-auto mt-10 p-4 border rounded shadow-md bg-white w-[1000px]">
      <h1 className="text-2xl font-semibold mb-4">Task Creation</h1>

      <textarea
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        rows={10}
        style={{ width: "1000px" }}
        className="w-[1000px] border p-2 rounded mb-2"
        placeholder="Enter your task prompt (e.g., request a laptop for John)..."
      />

      {error && <p className="text-red-600 text-sm mb-2">{error}</p>}

      <button
        onClick={handleSubmit}
        disabled={loading}
        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50"
      >
        {loading ? "Submitting..." : "Submit Task"}
      </button>

      {response && (
        <div className="mt-4 p-3 border rounded bg-gray-50">
          <strong>Agent Response:</strong>
          <pre className="whitespace-pre-wrap">{response}</pre>
        </div>
          )}
    </div>
  );
};

export default TaskCreationPage;
