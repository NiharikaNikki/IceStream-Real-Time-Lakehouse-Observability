const API_URL = "http://127.0.0.1:8000";


export async function getMetrics() {
  const response = await fetch(`${API_URL}/metrics`);

  if (!response.ok) {
    throw new Error("Failed to fetch metrics");
  }

  return await response.json();
}