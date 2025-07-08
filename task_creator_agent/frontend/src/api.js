export async function runAgent(userPrompt) {
  const response = await fetch("http://localhost:8000/run-agent", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ user_prompt: userPrompt })
  });

  if (!response.ok) {
    throw new Error("Agent call failed");
  }

  return await response.json();
}
