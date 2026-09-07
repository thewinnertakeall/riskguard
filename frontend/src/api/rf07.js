const API_BASE = "";

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

export async function getRF07Analysis() {
  return request("/api/rf07/analysis");
}
