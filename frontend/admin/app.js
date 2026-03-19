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
    this._isRegisterMode = false;

    if (this.token && this.user) {
      this._showDashboard();
    }
    this._bindNav();
    this._bindDragDrop();
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

  toggleAuthMode() {
    this._isRegisterMode = !this._isRegisterMode;
    const nameGroup = document.getElementById("registerNameGroup");
    const authBtn = document.getElementById("authBtn");
    const authToggle = document.getElementById("authToggle");
    const authTitle = document.getElementById("authTitle");
    const errEl = document.getElementById("loginError");
    errEl.classList.add("hidden");

    if (this._isRegisterMode) {
      nameGroup.classList.remove("hidden");
      authBtn.textContent = "Sign Up";
      authBtn.setAttribute("onclick", "app.register()");
      authToggle.textContent = "Already have an account? Sign In";
      authTitle.textContent = "Create Admin Account";
      document.getElementById("loginEmail").value = "";
      document.getElementById("loginPassword").value = "";
    } else {
      nameGroup.classList.add("hidden");
      authBtn.textContent = "Sign In";
      authBtn.setAttribute("onclick", "app.login()");
      authToggle.textContent = "Don't have an account? Sign Up";
      authTitle.textContent = "ClinicDesk Admin";
      document.getElementById("loginEmail").value = "admin@clinicdesk.com";
      document.getElementById("loginPassword").value = "demo123";
    }
  }

  async register() {
    const name = document.getElementById("registerName").value.trim();
    const email = document.getElementById("loginEmail").value.trim();
    const password = document.getElementById("loginPassword").value;
    const errEl = document.getElementById("loginError");
    errEl.classList.add("hidden");

    if (!name || !email || !password) {
      errEl.textContent = "All fields are required";
      errEl.classList.remove("hidden");
      return;
    }

    try {
      const res = await fetch(`${API}/api/auth/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, name, password }),
      });
      if (!res.ok) {
        const data = await res.json().catch(() => ({}));
        errEl.textContent = data.detail || "Registration failed";
        errEl.classList.remove("hidden");
        return;
      }
      const data = await res.json();
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
    this._startNotificationPolling();
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

  async _loadKB(search = "", category = "", page = 1) {
    const perPage = 20;
    const params = new URLSearchParams({ per_page: String(perPage), page: String(page) });
    if (category) params.set("category", category);
    const data = await this._api(`/api/admin/articles?${params}`);
    if (!data) return;

    let articles = data.articles;
    if (search) {
      const q = search.toLowerCase();
      articles = articles.filter(a => a.title.toLowerCase().includes(q));
    }

    this._kbPage = page;
    this._kbSearch = search;
    this._kbCategory = category;

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
      ${this._renderPagination(page, perPage, data.total, "app._kbGoToPage")}
    `;

    document.getElementById("kbSearch").addEventListener("input", (e) => {
      clearTimeout(this._kbDebounce);
      this._kbDebounce = setTimeout(() => {
        this._loadKB(e.target.value, document.getElementById("kbCatFilter").value, 1);
      }, 300);
    });
    document.getElementById("kbCatFilter").addEventListener("change", (e) => {
      this._loadKB(document.getElementById("kbSearch").value, e.target.value, 1);
    });
  }

  _kbGoToPage(page) {
    this._loadKB(this._kbSearch || "", this._kbCategory || "", page);
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

  // ── Document Drag & Drop ─────────────────────────────

  _bindDragDrop() {
    this._dragCounter = 0;
    const overlay = document.getElementById("dropOverlay");
    const dashboard = document.getElementById("dashboard");

    dashboard.addEventListener("dragenter", (e) => {
      e.preventDefault();
      this._dragCounter++;
      if (this._dragCounter === 1) overlay.classList.remove("hidden");
    });

    dashboard.addEventListener("dragover", (e) => {
      e.preventDefault();
    });

    dashboard.addEventListener("dragleave", (e) => {
      e.preventDefault();
      this._dragCounter--;
      if (this._dragCounter <= 0) {
        this._dragCounter = 0;
        overlay.classList.add("hidden");
      }
    });

    dashboard.addEventListener("drop", (e) => {
      e.preventDefault();
      this._dragCounter = 0;
      overlay.classList.add("hidden");

      const file = e.dataTransfer?.files?.[0];
      if (file) this._ingestDocument(file);
    });
  }

  async _ingestDocument(file) {
    const ext = file.name.split(".").pop().toLowerCase();
    if (!["pdf", "docx", "txt"].includes(ext)) {
      alert("Unsupported file type. Please use PDF, DOCX, or TXT.");
      return;
    }
    if (file.size > 10 * 1024 * 1024) {
      alert("File too large. Maximum 10MB.");
      return;
    }

    // Open article modal in loading state
    this.editingArticleId = null;
    document.getElementById("articleModalTitle").textContent = "Importing Document...";
    document.getElementById("articleTitle").value = "";
    document.getElementById("articleCategory").value = "scheduling";
    document.getElementById("articleContent").value = "Extracting and structuring content...";
    document.getElementById("articleTitle").disabled = true;
    document.getElementById("articleCategory").disabled = true;
    document.getElementById("articleContent").disabled = true;
    document.getElementById("articleSaveBtn").disabled = true;
    document.getElementById("articleModal").classList.remove("hidden");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch(`${API}/api/admin/ingest`, {
        method: "POST",
        headers: { Authorization: `Bearer ${this.token}` },
        body: formData,
      });

      if (res.status === 401) { this.logout(); return; }
      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail || "Failed to process document");
      }

      const data = await res.json();
      document.getElementById("articleModalTitle").textContent = "Review Imported Article";
      document.getElementById("articleTitle").value = data.title || "";
      document.getElementById("articleCategory").value = data.category || "scheduling";
      document.getElementById("articleContent").value = data.content || "";
    } catch (err) {
      alert("Failed to import document: " + err.message);
      this.closeArticleModal();
    } finally {
      document.getElementById("articleTitle").disabled = false;
      document.getElementById("articleCategory").disabled = false;
      document.getElementById("articleContent").disabled = false;
      document.getElementById("articleSaveBtn").disabled = false;
    }
  }

  // ── Sessions ──────────────────────────────────────────

  async _loadSessions(page = 1) {
    const perPage = 20;
    const data = await this._api(`/api/admin/sessions?per_page=${perPage}&page=${page}`);
    if (!data) return;

    document.getElementById("headerActions").innerHTML = "";
    const content = document.getElementById("mainContent");

    if (data.sessions.length === 0 && page === 1) {
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
      ${this._renderPagination(page, perPage, data.total, "app._loadSessions")}
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
                <div class="metric-sub">Sonnet 4.6 pricing: $3/M in · $15/M out</div>
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

  async _loadEscalations(page = 1) {
    const perPage = 20;
    const data = await this._api(`/api/admin/escalations?per_page=${perPage}&page=${page}`);
    if (!data) return;

    document.getElementById("headerActions").innerHTML = "";
    const content = document.getElementById("mainContent");

    if (data.escalations.length === 0 && page === 1) {
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
                <tr class="clickable" onclick="app._loadEscalationDetail(${e.id}, '${e.session_id}')">
                  <td><span class="badge badge-warning">${REASON_LABELS[e.reason] || e.reason}</span></td>
                  <td style="max-width:300px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">${this._esc(e.summary)}</td>
                  <td>${this._statusBadge(e.status)}</td>
                  <td class="text-sm text-muted">${e.assigned_to || "—"}</td>
                  <td class="text-sm text-muted">${this._fmtDate(e.created_at)}</td>
                  <td><button class="btn btn-ghost btn-sm">View →</button></td>
                </tr>
              `).join("")}
            </tbody>
          </table>
        </div>
      </div>
      ${this._renderPagination(page, perPage, data.total, "app._loadEscalations")}
    `;
  }

  async _updateEscalation(id, status) {
    await this._api(`/api/admin/escalations/${id}`, {
      method: "PUT",
      body: JSON.stringify({ status }),
    });
    // Reload detail if we're on a detail view, otherwise reload list
    if (this._currentEscalationId === id) {
      this._loadEscalationDetail(id, this._currentEscalationSessionId);
    } else {
      this._loadEscalations();
    }
  }

  async _loadEscalationDetail(escalationId, sessionId) {
    this._currentEscalationId = escalationId;
    this._currentEscalationSessionId = sessionId;

    // Fetch escalation list to get this one's data (no single-get endpoint)
    const escData = await this._api("/api/admin/escalations?per_page=100");
    const esc = escData?.escalations?.find(e => e.id === escalationId);
    if (!esc) return;

    // Fetch the linked session
    const session = await this._api(`/api/admin/sessions/${sessionId}`);

    document.getElementById("pageTitle").textContent = "Escalation Detail";
    document.getElementById("headerActions").innerHTML = "";
    const content = document.getElementById("mainContent");

    content.innerHTML = `
      <button class="back-btn" onclick="app._currentEscalationId=null;app._switchTab('escalations')">← Back to Escalations</button>

      <div class="detail-panel">
        <!-- Transcript -->
        <div class="detail-left">
          <div class="card" style="flex:1;display:flex;flex-direction:column;overflow:hidden">
            <div class="card-header"><span class="card-title">Conversation Transcript</span></div>
            <div class="transcript">
              ${session && session.messages ? session.messages.map(msg => `
                <div class="transcript-msg ${msg.role}">
                  <div class="transcript-bubble">${msg.role === "assistant" ? this._renderMd(msg.content) : this._esc(msg.content)}</div>
                  <div class="transcript-time">${this._fmtTime(msg.timestamp)}</div>
                  ${msg.tool_calls ? `<div style="margin-top:4px">${msg.tool_calls.map(t => `<span class="tool-tag">⚡ ${t}</span>`).join("")}</div>` : ""}
                </div>
              `).join("") : '<div class="text-muted" style="text-align:center;padding:32px">Session not found</div>'}
            </div>
          </div>
        </div>

        <!-- Escalation Info -->
        <div class="detail-right">
          <div class="card">
            <div class="card-header"><span class="card-title">Escalation Info</span></div>
            <div class="card-content">
              <div style="display:grid;grid-template-columns:auto minmax(0,1fr);gap:8px 12px;font-size:14px">
                <span class="text-muted">Reason</span>
                <span><span class="badge badge-warning">${REASON_LABELS[esc.reason] || esc.reason}</span></span>

                <span class="text-muted">Status</span>
                <span>${this._statusBadge(esc.status)}</span>

                <span class="text-muted">Assigned To</span>
                <span style="overflow-wrap:anywhere">${esc.assigned_to || "—"}</span>

                <span class="text-muted">Created</span>
                <span>${this._fmtDate(esc.created_at)}</span>

                <span class="text-muted">Resolved</span>
                <span>${esc.resolved_at ? this._fmtDate(esc.resolved_at) : "—"}</span>

                ${esc.calendar_event_id ? `
                  <span class="text-muted">Calendar Event</span>
                  <span class="font-mono text-sm" style="overflow-wrap:anywhere">${this._esc(esc.calendar_event_id)}</span>
                ` : ""}

                ${esc.email_sent_at ? `
                  <span class="text-muted">Email Sent</span>
                  <span>${this._fmtDate(esc.email_sent_at)}</span>
                ` : ""}
              </div>
            </div>
          </div>

          <div class="card">
            <div class="card-header"><span class="card-title">Summary</span></div>
            <div class="card-content">
              <p style="font-size:14px;line-height:1.6">${this._esc(esc.summary)}</p>
            </div>
          </div>

          <div class="card">
            <div class="card-header"><span class="card-title">Update Status</span></div>
            <div class="card-content">
              <select id="escStatusSelect" style="margin-bottom:8px">
                <option value="pending" ${esc.status === "pending" ? "selected" : ""}>Pending</option>
                <option value="in_progress" ${esc.status === "in_progress" ? "selected" : ""}>In Progress</option>
                <option value="resolved" ${esc.status === "resolved" ? "selected" : ""}>Resolved</option>
              </select>
              <button class="btn btn-primary btn-sm" onclick="app._updateEscalation(${esc.id}, document.getElementById('escStatusSelect').value)">Update</button>
            </div>
          </div>

          ${session ? `
          <div class="card">
            <div class="card-header"><span class="card-title">Session</span></div>
            <div class="card-content text-sm">
              <div style="display:grid;grid-template-columns:auto 1fr;gap:6px 12px">
                <span class="text-muted">ID</span><span class="font-mono">${session.id.slice(0, 12)}…</span>
                <span class="text-muted">Messages</span><span>${session.messages.length}</span>
                <span class="text-muted">Started</span><span>${this._fmtDate(session.created_at)}</span>
              </div>
              <button class="btn btn-secondary btn-sm mt-4" onclick="app._loadSessionDetail('${session.id}')">View Full Session →</button>
            </div>
          </div>
          ` : ""}
        </div>
      </div>
    `;
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

      <div style="display:grid;grid-template-columns:1fr 1fr;gap:24px;margin-bottom:24px">
        <div class="card">
          <div class="card-header"><span class="card-title">Cost Overview</span></div>
          <div class="card-content">
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">
              <div>
                <div class="metric-label">Total Spend</div>
                <div class="metric-value" style="font-size:22px">$${data.total_cost_usd.toFixed(4)}</div>
              </div>
              <div>
                <div class="metric-label">Avg Cost/Session</div>
                <div class="metric-value" style="font-size:22px">$${data.avg_cost_per_session.toFixed(4)}</div>
              </div>
            </div>
            <div class="metric-sub" style="margin-top:8px">Sonnet 4.6 pricing: $3/M in · $15/M out</div>
          </div>
        </div>
        <div class="card">
          <div class="card-header"><span class="card-title">Token Usage</span></div>
          <div class="card-content">
            <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px">
              <div>
                <div class="metric-label">Input Tokens</div>
                <div class="metric-value" style="font-size:18px">${data.total_input_tokens.toLocaleString()}</div>
              </div>
              <div>
                <div class="metric-label">Output Tokens</div>
                <div class="metric-value" style="font-size:18px">${data.total_output_tokens.toLocaleString()}</div>
              </div>
              <div>
                <div class="metric-label">Avg/Session</div>
                <div class="metric-value" style="font-size:18px">${data.avg_tokens_per_session.toLocaleString()}</div>
              </div>
            </div>
          </div>
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

  _renderPagination(page, perPage, total, onPageChange) {
    const totalPages = Math.ceil(total / perPage);
    if (totalPages <= 1) return "";
    const pages = [];
    for (let i = 1; i <= totalPages; i++) {
      pages.push(`<button class="btn btn-sm ${i === page ? "btn-primary" : "btn-ghost"}" onclick="${onPageChange}(${i})">${i}</button>`);
    }
    return `
      <div style="display:flex;align-items:center;justify-content:space-between;padding:12px 0">
        <span class="text-sm text-muted">Showing ${(page - 1) * perPage + 1}–${Math.min(page * perPage, total)} of ${total}</span>
        <div style="display:flex;gap:4px">${pages.join("")}</div>
      </div>
    `;
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

  // ── Notifications ─────────────────────────────────────

  _startNotificationPolling() {
    this._pollNotifications();
    this._connectAdminWS();
  }

  _connectAdminWS() {
    const wsProtocol = window.location.protocol === "https:" ? "wss:" : "ws:";
    const wsUrl = `${wsProtocol}//${window.location.host}/ws/admin`;
    this._adminWs = new WebSocket(wsUrl);

    this._adminWs.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === "notification") {
        this._pollNotifications();
        // If currently on escalations tab, refresh the list
        if (this.currentTab === "escalations") {
          this._loadEscalations();
        }
      }
    };

    this._adminWs.onclose = () => {
      // Reconnect after 3 seconds
      setTimeout(() => {
        if (this.token) this._connectAdminWS();
      }, 3000);
    };

    this._adminWs.onerror = () => {};

    // Keep alive with pings every 30 seconds
    this._adminPingInterval = setInterval(() => {
      if (this._adminWs?.readyState === WebSocket.OPEN) {
        this._adminWs.send("ping");
      }
    }, 30000);
  }

  async _pollNotifications() {
    const data = await this._api("/api/admin/notifications/count");
    if (!data) return;
    const badge = document.getElementById("notifBadge");
    if (data.unread > 0) {
      badge.textContent = data.unread > 99 ? "99+" : data.unread;
      badge.classList.remove("hidden");
    } else {
      badge.classList.add("hidden");
    }
  }

  async toggleNotifications() {
    const dropdown = document.getElementById("notifDropdown");
    const isOpen = !dropdown.classList.contains("hidden");
    if (isOpen) {
      dropdown.classList.add("hidden");
      return;
    }

    // Load notifications
    const data = await this._api("/api/admin/notifications?limit=20");
    if (!data) return;

    const list = document.getElementById("notifList");
    if (data.notifications.length === 0) {
      list.innerHTML = '<div class="text-muted text-sm" style="padding:24px;text-align:center">No notifications</div>';
    } else {
      list.innerHTML = data.notifications.map(n => `
        <div class="notif-item ${n.is_read ? "" : "unread"}" onclick="app._handleNotifClick(${n.id}, '${n.reference_type}', ${n.reference_id})">
          <div class="notif-dot ${n.is_read ? "read" : ""}"></div>
          <div class="notif-item-content">
            <div class="notif-item-title">${this._esc(n.title)}</div>
            <div class="notif-item-msg">${this._esc(n.message)}</div>
            <div class="notif-item-time">${this._fmtTimeAgo(n.created_at)}</div>
          </div>
        </div>
      `).join("");
    }

    dropdown.classList.remove("hidden");

    // Close on outside click
    const closeHandler = (e) => {
      if (!document.getElementById("notifWrapper")?.contains(e.target)) {
        dropdown.classList.add("hidden");
        document.removeEventListener("click", closeHandler);
      }
    };
    setTimeout(() => document.addEventListener("click", closeHandler), 0);
  }

  async _handleNotifClick(notifId, refType, refId) {
    // Mark as read
    await this._api(`/api/admin/notifications/${notifId}/read`, { method: "POST" });
    document.getElementById("notifDropdown").classList.add("hidden");
    this._pollNotifications();

    // Navigate to the referenced item
    if (refType === "escalation" && refId) {
      // Find the escalation's session_id
      const escData = await this._api("/api/admin/escalations?per_page=100");
      const esc = escData?.escalations?.find(e => e.id === refId);
      if (esc) {
        this._switchTab("escalations");
        setTimeout(() => this._loadEscalationDetail(refId, esc.session_id), 100);
      } else {
        this._switchTab("escalations");
      }
    }
  }

  async markAllRead() {
    await this._api("/api/admin/notifications/read-all", { method: "POST" });
    this._pollNotifications();
    this.toggleNotifications(); // close and reopen to refresh
    this.toggleNotifications();
  }

  _fmtTimeAgo(iso) {
    const now = new Date();
    const date = new Date(iso);
    const seconds = Math.floor((now - date) / 1000);
    if (seconds < 60) return "just now";
    const minutes = Math.floor(seconds / 60);
    if (minutes < 60) return `${minutes}m ago`;
    const hours = Math.floor(minutes / 60);
    if (hours < 24) return `${hours}h ago`;
    const days = Math.floor(hours / 24);
    if (days < 7) return `${days}d ago`;
    return this._fmtDate(iso);
  }
}

const app = new App();
