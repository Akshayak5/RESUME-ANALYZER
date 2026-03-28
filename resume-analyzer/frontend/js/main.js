// ── API Configuration ──────────────────────────────────
const API_BASE = "http://localhost:5000/api";

// ── Token Management ───────────────────────────────────
const Auth = {
  getToken: () => localStorage.getItem("token"),
  setToken: (t) => localStorage.setItem("token", t),
  removeToken: () => localStorage.removeItem("token"),
  isLoggedIn: () => !!localStorage.getItem("token"),
  setUser: (u) => localStorage.setItem("user", JSON.stringify(u)),
  getUser: () => { try { return JSON.parse(localStorage.getItem("user")); } catch { return null; } },
  logout: () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    window.location.href = "/pages/login.html";
  }
};

// ── HTTP Client ────────────────────────────────────────
async function api(path, options = {}) {
  const token = Auth.getToken();
  const headers = { "Content-Type": "application/json", ...(options.headers || {}) };
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const res = await fetch(`${API_BASE}${path}`, { ...options, headers });
  const data = await res.json().catch(() => ({}));

  if (res.status === 401) { Auth.logout(); return; }
  return { ok: res.ok, status: res.status, data };
}

async function apiUpload(path, formData) {
  const token = Auth.getToken();
  const headers = {};
  if (token) headers["Authorization"] = `Bearer ${token}`;
  const res = await fetch(`${API_BASE}${path}`, { method: "POST", headers, body: formData });
  const data = await res.json().catch(() => ({}));
  if (res.status === 401) { Auth.logout(); return; }
  return { ok: res.ok, status: res.status, data };
}

// ── Toast Notifications ────────────────────────────────
function toast(msg, type = "info") {
  let el = document.getElementById("toast");
  if (!el) {
    el = document.createElement("div");
    el.id = "toast";
    el.className = "toast";
    document.body.appendChild(el);
  }
  el.textContent = msg;
  el.className = `toast ${type} show`;
  setTimeout(() => el.classList.remove("show"), 3000);
}

// ── Score Color Helper ─────────────────────────────────
function scoreColor(score) {
  if (score >= 75) return "#22c55e";
  if (score >= 50) return "#f59e0b";
  return "#ef4444";
}
function scoreLabel(score) {
  if (score >= 75) return "Excellent";
  if (score >= 50) return "Good";
  if (score >= 30) return "Needs Work";
  return "Poor";
}

// ── Redirect if not logged in ──────────────────────────
function requireAuth() {
  if (!Auth.isLoggedIn()) {
    window.location.href = "/pages/login.html";
    return false;
  }
  return true;
}

// ── Format Date ────────────────────────────────────────
function formatDate(dateStr) {
  if (!dateStr) return "—";
  const d = new Date(dateStr);
  return d.toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" });
}

window.Auth = Auth;
window.api = api;
window.apiUpload = apiUpload;
window.toast = toast;
window.scoreColor = scoreColor;
window.scoreLabel = scoreLabel;
window.requireAuth = requireAuth;
window.formatDate = formatDate;
