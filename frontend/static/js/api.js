// api.js — ResumeIQ API client
const BASE = '';

const api = {
  async request(method, path, body = null, isForm = false) {
    try {
      const opts = {
        method,
        headers: isForm ? {} : { 'Content-Type': 'application/json' },
      };
      if (body) opts.body = isForm ? body : JSON.stringify(body);

      const res  = await fetch(BASE + path, opts);
      let data;
      try {
        data = await res.json();
      } catch(e) {
        throw new Error(`Server error ${res.status}: non-JSON response`);
      }
      if (!res.ok) throw new Error(data.error || `HTTP ${res.status}`);
      return data;
    } catch(err) {
      // Re-throw with the real message so UI can show it
      throw err;
    }
  },

  // Auth
  register: (name, email, password, role) =>
    api.request('POST', '/api/auth/register', { name, email, password, role }),
  login: (email, password) =>
    api.request('POST', '/api/auth/login', { email, password }),
  profile: (uid) =>
    api.request('GET', `/api/auth/profile/${uid}`),

  // Resume
  analyze: (file, userId) => {
    const fd = new FormData();
    fd.append('file', file);
    fd.append('user_id', String(userId || 'anonymous'));
    return api.request('POST', '/api/resume/analyze', fd, true);
  },
  getResume: (id) => api.request('GET', `/api/resume/${encodeURIComponent(id)}`),
  history:   (userId) => api.request('GET', `/api/resume/history?user_id=${encodeURIComponent(String(userId || ''))}`),
  trending:  () => api.request('GET', '/api/resume/skills/trending'),
  verifySkill: (payload) => api.request('POST', '/api/resume/verify-skill', payload),
  deleteResume: (id) => api.request('DELETE', `/api/resume/${encodeURIComponent(id)}`),
  updateResume: (id, data) => api.request('PATCH', `/api/resume/${encodeURIComponent(id)}`, data),

  // Employer
  candidates: (params = {}) => {
    const q = new URLSearchParams(params).toString();
    return api.request('GET', `/api/employer/candidates${q ? '?' + q : ''}`);
  },
};

// ── Session ───────────────────────────────────────────────────────────────────
const session = {
  set(user)  { localStorage.setItem('riq_user', JSON.stringify(user)); },
  get()      { try { return JSON.parse(localStorage.getItem('riq_user')); } catch { return null; } },
  clear()    { localStorage.removeItem('riq_user'); },
  require(role = null) {
    const u = session.get();
    if (!u) { window.location.href = '/'; return null; }
    if (role && u.role !== role) { window.location.href = '/dashboard'; return null; }
    return u;
  },
};

// ── Toast ─────────────────────────────────────────────────────────────────────
function showToast(msg, type = 'info') {
  let wrap = document.querySelector('.toast-wrap');
  if (!wrap) {
    wrap = document.createElement('div');
    wrap.className = 'toast-wrap';
    document.body.appendChild(wrap);
  }
  const icons = { success: '✓', error: '✕', info: 'ℹ' };
  const t = document.createElement('div');
  t.className = `toast toast-${type}`;
  t.innerHTML = `<span>${icons[type] || 'ℹ'}</span><span>${msg}</span>`;
  wrap.appendChild(t);
  setTimeout(() => {
    t.style.animation = 'toastIn .3s ease reverse';
    setTimeout(() => t.remove(), 300);
  }, 3500);
}

// ── Score helpers ─────────────────────────────────────────────────────────────
function scoreColor(score) {
  if (score >= 75) return '#00d9a3';
  if (score >= 50) return '#ffd32a';
  return '#ff4757';
}

function scoreLabel(score) {
  if (score >= 80) return 'Excellent';
  if (score >= 65) return 'Good';
  if (score >= 45) return 'Average';
  return 'Needs Work';
}