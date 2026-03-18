/**
 * ClinicDesk Admin Dashboard — Single-page app
 */

const API = window.location.origin;

const CATEGORY_LABELS = {
  scheduling: "Scheduling",
  billing_coding: "Billing & Coding",
  insurance_claims: "Insurance & Claims",
  patient_records: "Patient Records",
  reporting_analytics: "Reporting & Analytics",
  technical_troubleshooting: "Troubleshooting",
  account_plans: "Account & Plans",
};

const REASON_LABELS = {
  knowledge_gap: "Knowledge Gap",
  user_frustration: "User Frustration",
  out_of_scope: "Out of Scope",
  billing_dispute: "Billing Dispute",
  account_change: "Account Change",
};

class App {
  constructor() {
    this.token = sessionStorage.getItem("admin_token");
    this.user = JSON.parse(sessionStorage.getItem("admin_user") || "null");
    this.currentTab = "kb";
    this.editingArticleId = null;

    if (this.token && this.user) {
      this._showDashboard();
    }
    this._bindNav();
  }

  // ── Auth ──────────────────────────────────────────────

  async login() {
    const email = document.getElementById("loginEmail").value;
    const password = document.getElementById("loginPassword").value;
    const errEl = document.getElementById("loginError");
    errEl.classList.add("hidden");

    try {
      const res = await fetch(`${API}/api/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });
      if (!res.ok) {
        errEl.textContent = "Invalid credentials";
        errEl.classList.remove("hidden");
        return;
      }
      const data = await res.json();
      if (data.user.role !== "admin") {
        errEl.textContent = "Admin access required";
        errEl.classList.remove("hidden");
        return;
      }
      this.token = data.token;
      this.user = data.user;
      sessionStorage.setItem("admin_token", data.token);
      sessionStorage.setItem("admin_user", JSON.stringify(data.user));
      this._showDashboard();
    } catch {
      errEl.textContent = "Connection error";
      errEl.classList.remove("hidden");
    }
  }

  logout() {
    this.token = null;
    this.user = null;
    sessionStorage.removeItem("admin_token");
    sessionStorage.removeItem("admin_user");
    document.getElementById("dashboard").classList.add("hidden");
    document.getElementById("loginScreen").classList.remove("hidden");
  }

  _showDashboard() {
    document.getElementById("loginScreen").classList.add("hidden");
    document.getElementById("dashboard").classList.remove("hidden");
    document.getElementById("userName").textContent = this.user.name;
    this._switchTab("kb");
  }

  async _api(path, opts = {}) {
    const res = await fetch(`${API}${path}`, {
      ...opts,
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${this.token}`,
        ...(opts.headers || {}),
      },
    });
    if (res.status === 401) { this.logout(); return null; }
    if (res.status === 204) return null;
    return res.json();
  }

  // ── Navigation ────────────────────────────────────────

  _bindNav() {
    document.querySelectorAll(".nav-item[data-tab]").forEach((btn) => {
      btn.addEventListener("click", () => this._switchTab(btn.dataset.tab));
    });
  }

  _switchTab(tab) {
    this.currentTab = tab;
    document.querySelectorAll(".nav-item").forEach((b) => b.classList.remove("active"));
    document.querySelector(`.nav-item[data-tab="${tab}"]`)?.classList.add("active");

    const titles = { kb: "Knowledge Base", sessions: "Sessions", escalations: "Escalations", analytics: "Analytics" };
    document.getElementById("pageTitle").textContent = titles[tab];

    const content = document.getElementById("mainContent");
    content.innerHTML = '<div class="spinner"></div>';
    document.getElementById("headerActions").innerHTML = "";

    if (tab === "kb") this._loadKB();
    else if (tab === "sessions") this._loadSessions();
    else if (tab === "escalations") this._loadEscalations();
    else if (tab === "analytics") this._loadAnalytics();
  }

  // ── Knowledge Base ────────────────────────────────────

  async _loadKB(search = "", category = "") {
    const params = new URLSearchParams({ per_page: "100" });
    if (category) params.set("category", category);
    const data = await this._api(`/api/admin/articles?${params}`);
    if (!data) return;

    let articles = data.articles;
    if (search) {
      const q = search.toLowerCase();
      articles = articles.filter(a => a.title.toLowerCase().includes(q));
    }

    document.getElementById("headerActions").innerHTML =
      `<button class="btn btn-primary" onclick="app.openArticleModal()">+ New Article</button>`;

    const content = document.getElementById("mainContent");
    content.innerHTML = `
      <div class="toolbar">
        <div class="toolbar-left">
          <input type="search" id="kbSearch" placeholder="Search articles..." value="${this._esc(search)}" style="max-width:280px">
          <select id="kbCatFilter" style="max-width:200px">
            <option value="">All Categories</option>
            ${Object.entries(CATEGORY_LABELS).map(([v, l]) => `<option value="${v}" ${v === category ? "selected" : ""}>${l}</option>`).join("")}
          </select>
        </div>
        <div class="toolbar-right text-sm text-muted">${data.total} articles</div>
      </div>
      <div class="card">
        <div class="table-wrap">
          <table>
            <thead><tr><th>Title</th><th>Category</th><th>Updated</th><th style="width:100px"></th></tr></thead>
            <tbody>
              ${articles.length === 0 ? '<tr><td colspan="4" class="text-muted" style="text-align:center;padding:32px">No articles found</td></tr>' : ""}
              ${articles.map(a => `
                <tr>
                  <td style="font-weight:500">${this._esc(a.title)}</td>
                  <td><span class="badge cat-${a.category}">${CATEGORY_LABELS[a.category] || a.category}</span></td>
                  <td class="text-muted text-sm">${this._fmtDate(a.updated_at)}</td>
                  <td>
                    <button class="btn btn-ghost btn-sm" onclick="app.editArticle(${a.id})">Edit</button>
                    <button class="btn btn-ghost btn-sm" style="color:var(--destructive)" onclick="app.deleteArticle(${a.id})">Delete</button>
                  </td>
                </tr>
              `).join("")}
            </tbody>
          </table>
        </div>
      </div>
    `;

    document.getElementById("kbSearch").addEventListener("input", (e) => {
      clearTimeout(this._kbDebounce);
      this._kbDebounce = setTimeout(() => {
        this._loadKB(e.target.value, document.getElementById("kbCatFilter").value);
      }, 300);
    });
    document.getElementById("kbCatFilter").addEventListener("change", (e) => {
      this._loadKB(document.getElementById("kbSearch").value, e.target.value);
    });
  }

  openArticleModal(article = null) {
    this.editingArticleId = article?.id || null;
    document.getElementById("articleModalTitle").textContent = article ? "Edit Article" : "New Article";
    document.getElementById("articleTitle").value = article?.title || "";
    document.getElementById("articleCategory").value = article?.category || "scheduling";
    document.getElementById("articleContent").value = article?.content || "";
    document.getElementById("articleModal").classList.remove("hidden");
  }

  closeArticleModal() {
    document.getElementById("articleModal").classList.add("hidden");
    this.editingArticleId = null;
  }

  async editArticle(id) {
    const data = await this._api(`/api/admin/articles/${id}`);
    if (data) this.openArticleModal(data);
  }

  async saveArticle() {
    const title = document.getElementById("articleTitle").value.trim();
    const category = document.getElementById("articleCategory").value;
    const contentVal = document.getElementById("articleContent").value.trim();
    if (!title || !contentVal) return;

    const body = { title, category, content: contentVal };
    if (this.editingArticleId) {
      await this._api(`/api/admin/articles/${this.editingArticleId}`, { method: "PUT", body: JSON.stringify(body) });
    } else {
      await this._api("/api/admin/articles", { method: "POST", body: JSON.stringify(body) });
    }
    this.closeArticleModal();
    this._loadKB();
  }

  async deleteArticle(id) {
    if (!confirm("Delete this article? This cannot be undone.")) return;
    await this._api(`/api/admin/articles/${id}`, { method: "DELETE" });
    this._loadKB();
  }

  // ── Sessions ──────────────────────────────────────────

  async _loadSessions() {
    const data = await this._api("/api/admin/sessions?per_page=100");
    if (!data) return;

    document.getElementById("headerActions").innerHTML = "";
    const content = document.getElementById("mainContent");

    if (data.sessions.length === 0) {
      content.innerHTML = `<div class="empty-state"><p>No sessions yet. Start a conversation in the chat widget to see sessions here.</p></div>`;
      return;
    }

    content.innerHTML = `
      <div class="card">
        <div class="table-wrap">
          <table>
            <thead><tr><th>Session</th><th>Status</th><th>Messages</th><th>Started</th><th></th></tr></thead>
            <tbody>
              ${data.sessions.map(s => `
                <tr class="clickable" onclick="app._loadSessionDetail('${s.id}')">
                  <td class="font-mono text-sm">${s.id.slice(0, 8)}…</td>
                  <td>${s.status === "active"
                    ? '<span class="badge badge-active">Active</span>'
                    : '<span class="badge badge-default">Closed</span>'}</td>
                  <td>${s.message_count}</td>
                  <td class="text-muted text-sm">${this._fmtDate(s.created_at)}</td>
                  <td><button class="btn btn-ghost btn-sm">View →</button></td>
                </tr>
              `).join("")}
            </tbody>
          </table>
        </div>
      </div>
    `;
  }

  async _loadSessionDetail(id) {
    const data = await this._api(`/api/admin/sessions/${id}`);
    if (!data) return;

    document.getElementById("pageTitle").textContent = "Session Detail";
    const m = data.metadata || {};
    const turns = m.turns || [];
    const toolCounts = m.tool_call_counts || {};
    const totalCost = m.total_cost_usd ?? 0;
    const totalInput = m.total_input_tokens ?? 0;
    const totalOutput = m.total_output_tokens ?? 0;

    const content = document.getElementById("mainContent");
    content.innerHTML = `
      <button class="back-btn" onclick="app._switchTab('sessions')">← Back to Sessions</button>

      <div class="detail-panel">
        <!-- Transcript -->
        <div class="detail-left">
          <div class="card" style="flex:1;display:flex;flex-direction:column;overflow:hidden">
            <div class="card-header"><span class="card-title">Conversation Transcript</span></div>
            <div class="transcript">
              ${data.messages.map(msg => `
                <div class="transcript-msg ${msg.role}">
                  <div class="transcript-bubble">${msg.role === "assistant" ? this._renderMd(msg.content) : this._esc(msg.content)}</div>
                  <div class="transcript-time">${this._fmtTime(msg.timestamp)}</div>
                  ${msg.tool_calls ? `<div style="margin-top:4px">${msg.tool_calls.map(t => `<span class="tool-tag">⚡ ${t}</span>`).join("")}</div>` : ""}
                </div>
              `).join("")}
              ${data.messages.length === 0 ? '<div class="text-muted" style="text-align:center;padding:32px">No messages</div>' : ""}
            </div>
          </div>
        </div>

        <!-- Metrics -->
        <div class="detail-right">
          <!-- Cost & Tokens -->
          <div class="card">
            <div class="card-header"><span class="card-title">Usage & Cost</span></div>
            <div class="card-content">
              <div class="metrics-grid" style="grid-template-columns:1fr 1fr">
                <div>
                  <div class="metric-label">Input Tokens</div>
                  <div class="metric-value" style="font-size:20px">${totalInput.toLocaleString()}</div>
                </div>
                <div>
                  <div class="metric-label">Output Tokens</div>
                  <div class="metric-value" style="font-size:20px">${totalOutput.toLocaleString()}</div>
                </div>
              </div>
              <div style="margin-top:12px;padding-top:12px;border-top:1px solid var(--border)">
                <div class="metric-label">Total Cost</div>
                <div class="metric-value" style="font-size:22px">$${totalCost.toFixed(4)}</div>
                <div class="metric-sub">Sonnet 4 pricing: $3/M in · $15/M out</div>
              </div>
            </div>
          </div>

          <!-- Tool Calls -->
          <div class="card">
            <div class="card-header"><span class="card-title">Tool Calls</span></div>
            <div class="card-content">
              ${Object.keys(toolCounts).length === 0
                ? '<div class="text-muted text-sm">No tools called</div>'
                : `<table style="font-size:13px">
                    <thead><tr><th>Tool</th><th style="text-align:right">Count</th></tr></thead>
                    <tbody>
                      ${Object.entries(toolCounts).sort((a, b) => b[1] - a[1]).map(([name, count]) => `
                        <tr><td class="font-mono">${name}</td><td style="text-align:right;font-weight:600">${count}</td></tr>
                      `).join("")}
                    </tbody>
                  </table>`}
            </div>
          </div>

          <!-- Per-Turn Breakdown -->
          <div class="card">
            <div class="card-header"><span class="card-title">Per-Turn Breakdown</span></div>
            <div class="card-content">
              ${turns.length === 0
                ? '<div class="text-muted text-sm">No turn data</div>'
                : `<div class="table-wrap"><table style="font-size:12px">
                    <thead><tr><th>#</th><th>In</th><th>Out</th><th>Cost</th><th>Tools</th></tr></thead>
                    <tbody>
                      ${turns.map(t => `
                        <tr>
                          <td>${t.turn}</td>
                          <td>${t.input_tokens.toLocaleString()}</td>
                          <td>${t.output_tokens.toLocaleString()}</td>
                          <td>$${t.cost_usd.toFixed(4)}</td>
                          <td>${(t.tool_calls || []).length > 0 ? t.tool_calls.map(tc => `<span class="tool-tag">${tc}</span>`).join("") : '<span class="text-muted">—</span>'}</td>
                        </tr>
                      `).join("")}
                    </tbody>
                  </table></div>`}
            </div>
          </div>

          <!-- Session Info -->
          <div class="card">
            <div class="card-header"><span class="card-title">Session Info</span></div>
            <div class="card-content text-sm">
              <div style="display:grid;grid-template-columns:auto 1fr;gap:6px 12px">
                <span class="text-muted">ID</span><span class="font-mono">${data.id.slice(0, 12)}…</span>
                <span class="text-muted">Status</span><span>${data.status === "active" ? '<span class="badge badge-active">Active</span>' : '<span class="badge badge-default">Closed</span>'}</span>
                <span class="text-muted">Messages</span><span>${data.messages.length}</span>
                <span class="text-muted">Started</span><span>${this._fmtDate(data.created_at)}</span>
                <span class="text-muted">Last Activity</span><span>${this._fmtDate(data.updated_at)}</span>
                ${data.context?.notes ? `<span class="text-muted">Agent Notes</span><span>${this._esc(data.context.notes)}</span>` : ""}
              </div>
            </div>
          </div>
        </div>
      </div>
    `;
  }

  // ── Escalations ───────────────────────────────────────

  async _loadEscalations() {
    const data = await this._api("/api/admin/escalations?per_page=100");
    if (!data) return;

    document.getElementById("headerActions").innerHTML = "";
    const content = document.getElementById("mainContent");

    if (data.escalations.length === 0) {
      content.innerHTML = `<div class="empty-state"><p>No escalations yet. Escalations appear when the agent hands off to a human.</p></div>`;
      return;
    }

    content.innerHTML = `
      <div class="card">
        <div class="table-wrap">
          <table>
            <thead><tr><th>Reason</th><th>Summary</th><th>Status</th><th>Assigned To</th><th>Created</th><th></th></tr></thead>
            <tbody>
              ${data.escalations.map(e => `
                <tr>
                  <td><span class="badge badge-warning">${REASON_LABELS[e.reason] || e.reason}</span></td>
                  <td style="max-width:300px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">${this._esc(e.summary)}</td>
                  <td>${this._statusBadge(e.status)}</td>
                  <td class="text-sm text-muted">${e.assigned_to || "—"}</td>
                  <td class="text-sm text-muted">${this._fmtDate(e.created_at)}</td>
                  <td>
                    <select class="btn btn-secondary btn-sm" style="padding:4px 8px;font-size:12px" onchange="app._updateEscalation(${e.id}, this.value)">
                      <option value="pending" ${e.status === "pending" ? "selected" : ""}>Pending</option>
                      <option value="in_progress" ${e.status === "in_progress" ? "selected" : ""}>In Progress</option>
                      <option value="resolved" ${e.status === "resolved" ? "selected" : ""}>Resolved</option>
                    </select>
                  </td>
                </tr>
              `).join("")}
            </tbody>
          </table>
        </div>
      </div>
    `;
  }

  async _updateEscalation(id, status) {
    await this._api(`/api/admin/escalations/${id}`, {
      method: "PUT",
      body: JSON.stringify({ status }),
    });
    this._loadEscalations();
  }

  _statusBadge(status) {
    const map = {
      pending: "badge-warning",
      in_progress: "badge-primary",
      resolved: "badge-success",
    };
    const labels = { pending: "Pending", in_progress: "In Progress", resolved: "Resolved" };
    return `<span class="badge ${map[status] || "badge-default"}">${labels[status] || status}</span>`;
  }

  // ── Analytics ─────────────────────────────────────────

  async _loadAnalytics(days = 30) {
    const data = await this._api(`/api/admin/analytics?days=${days}`);
    if (!data) return;

    document.getElementById("headerActions").innerHTML = `
      <div class="tab-group">
        <button class="tab-btn ${days === 7 ? "active" : ""}" onclick="app._loadAnalytics(7)">7d</button>
        <button class="tab-btn ${days === 30 ? "active" : ""}" onclick="app._loadAnalytics(30)">30d</button>
        <button class="tab-btn ${days === 90 ? "active" : ""}" onclick="app._loadAnalytics(90)">90d</button>
      </div>
    `;

    const content = document.getElementById("mainContent");
    content.innerHTML = `
      <div class="metrics-grid">
        <div class="metric-card">
          <div class="metric-label">Total Sessions</div>
          <div class="metric-value">${data.total_sessions}</div>
        </div>
        <div class="metric-card">
          <div class="metric-label">Active Sessions</div>
          <div class="metric-value">${data.active_sessions}</div>
        </div>
        <div class="metric-card">
          <div class="metric-label">Total Escalations</div>
          <div class="metric-value">${data.total_escalations}</div>
        </div>
        <div class="metric-card">
          <div class="metric-label">Escalation Rate</div>
          <div class="metric-value">${(data.escalation_rate * 100).toFixed(1)}%</div>
        </div>
        <div class="metric-card">
          <div class="metric-label">Resolution Rate</div>
          <div class="metric-value">${(data.resolution_rate * 100).toFixed(1)}%</div>
        </div>
        <div class="metric-card">
          <div class="metric-label">Avg Messages/Session</div>
          <div class="metric-value">${data.avg_messages_per_session.toFixed(1)}</div>
        </div>
      </div>

      <div style="display:grid;grid-template-columns:1fr 1fr;gap:24px">
        <div class="card">
          <div class="card-header"><span class="card-title">Top Categories</span></div>
          <div class="card-content">
            ${data.top_categories.length === 0 ? '<div class="text-muted text-sm">No data yet</div>' : `
              ${data.top_categories.map(c => `
                <div style="display:flex;align-items:center;justify-content:space-between;padding:8px 0;border-bottom:1px solid var(--border)">
                  <span class="badge cat-${c.category}">${CATEGORY_LABELS[c.category] || c.category}</span>
                  <span style="font-weight:600">${c.count}</span>
                </div>
              `).join("")}
            `}
          </div>
        </div>

        <div class="card">
          <div class="card-header"><span class="card-title">Escalation Reasons</span></div>
          <div class="card-content">
            ${data.escalation_reasons.length === 0 ? '<div class="text-muted text-sm">No escalations in this period</div>' : `
              ${data.escalation_reasons.map(r => `
                <div style="display:flex;align-items:center;justify-content:space-between;padding:8px 0;border-bottom:1px solid var(--border)">
                  <span class="badge badge-warning">${REASON_LABELS[r.reason] || r.reason}</span>
                  <span style="font-weight:600">${r.count}</span>
                </div>
              `).join("")}
            `}
          </div>
        </div>
      </div>
    `;
  }

  // ── Helpers ───────────────────────────────────────────

  _esc(str) {
    if (!str) return "";
    const d = document.createElement("div");
    d.textContent = str;
    return d.innerHTML;
  }

  _fmtDate(iso) {
    if (!iso) return "—";
    const d = new Date(iso);
    return d.toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" });
  }

  _fmtTime(iso) {
    if (!iso) return "";
    const d = new Date(iso);
    return d.toLocaleString("en-US", { month: "short", day: "numeric", hour: "numeric", minute: "2-digit" });
  }

  _renderMd(text) {
    if (!text) return "";
    let h = this._esc(text);
    h = h.replace(/^### (.+)$/gm, "<strong>$1</strong><br>");
    h = h.replace(/^## (.+)$/gm, "<strong>$1</strong><br>");
    h = h.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
    h = h.replace(/\*(.+?)\*/g, "<em>$1</em>");
    h = h.replace(/`([^`]+)`/g, '<code style="background:rgba(0,0,0,0.06);padding:1px 4px;border-radius:3px;font-size:12px">$1</code>');
    h = h.replace(/\n/g, "<br>");
    return h;
  }
}

const app = new App();
