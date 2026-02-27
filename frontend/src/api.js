const API_URL = import.meta.env.VITE_API_URL || "http://localhost:5001";

export async function getCompanies() {
  try {
    const res = await fetch(`${API_URL}/api/companies`);
    const data = await res.json();
    return data;
  } catch (error) {
    console.error("Error fetching companies:", error);
    return [];
  }
}

export async function uploadResume(file) {
  try {
    const form = new FormData();
    form.append("file", file);
    const res = await fetch(`${API_URL}/api/resume`, { method: "POST", body: form });
    const data = await res.json();
    console.log("Upload response:", data);
    return data;
  } catch (error) {
    console.error("Error uploading resume:", error);
    return { ok: false, error: error.message };
  }
}

export async function sendToCompany(id) {
  try {
    const res = await fetch(`${API_URL}/api/send/${id}`, { method: "POST" });
    return await res.json();
  } catch (error) {
    console.error("Error sending to company:", error);
    return { status: "FAILED", error: error.message };
  }
}

export async function getLogs() {
  try {
    const res = await fetch(`${API_URL}/api/applications`);
    const data = await res.json();
    return data;
  } catch (error) {
    console.error("Error fetching logs:", error);
    return [];
  }
}

export async function getResume() {
  try {
    const res = await fetch(`${API_URL}/api/resume`);
    return await res.json();
  } catch (error) {
    console.error("Error fetching resume:", error);
    return { ok: false, error: error.message };
  }
}