const API_BASE = "http://127.0.0.1:8000";

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {})
    },
    ...options
  });

  const contentType = response.headers.get("content-type") || "";

  const data = contentType.includes("application/json")
    ? await response.json()
    : await response.text();

  if (!response.ok) {
    const message =
      typeof data === "object" && data?.detail
        ? data.detail
        : `API error ${response.status}`;

    throw new Error(message);
  }

  return data;
}

export async function getIncidents() {
  return request("/api/incidents");
}

export async function getIncident(id) {
  return request(`/api/incidents/${encodeURIComponent(id)}`);
}

export async function createIncident(data) {
  return request("/api/incidents", {
    method: "POST",
    body: JSON.stringify(data)
  });
}

export async function updateIncident(id, data) {
  return request(`/api/incidents/${encodeURIComponent(id)}`, {
    method: "PUT",
    body: JSON.stringify(data)
  });
}

export async function deleteIncident(id) {
  return request(`/api/incidents/${encodeURIComponent(id)}`, {
    method: "DELETE"
  });
}
