/**
 * ClinicDesk AI Chat Widget
 * Embeddable, draggable chat widget with Shadow DOM encapsulation.
 *
 * Usage:
 *   <script src="/static/widget/chat-widget.js"
 *           data-server="ws://localhost:8000"
 *           data-color="#2563eb"
 *           data-title="ClinicDesk Support"
 *           data-greeting="Hi! How can I help you today?">
 *   </script>
 */

(function () {
  const scriptTag = document.currentScript;
  const config = {
    server: scriptTag?.getAttribute("data-server") || `ws://${location.host}`,
    color: scriptTag?.getAttribute("data-color") || "#2563eb",
    title: scriptTag?.getAttribute("data-title") || "ClinicDesk Support",
    greeting:
      scriptTag?.getAttribute("data-greeting") ||
      "Hi! How can I help you today?",
    position: scriptTag?.getAttribute("data-position") || "bottom-right",
  };

  class ClinicDeskWidget extends HTMLElement {
    constructor() {
      super();
      this.attachShadow({ mode: "open" });
      this._ws = null;
      this._sessionId = null;
      this._isOpen = false;
      this._isDragging = false;
      this._dragOffset = { x: 0, y: 0 };
      this._reconnectAttempts = 0;
      this._maxReconnectAttempts = 5;
    }

    connectedCallback() {
      this._render();
      this._bindEvents();
      this._restoreSession();
    }

    disconnectedCallback() {
      if (this._ws) this._ws.close();
    }

    _render() {
      this.shadowRoot.innerHTML = `
        <style>${this._getStyles()}</style>
        <div class="widget-container" id="container">
          <button class="fab" id="fab" aria-label="Open chat">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
            </svg>
          </button>
          <div class="chat-window" id="chatWindow">
            <div class="resize-handle" id="resizeHandle"></div>
            <div class="chat-header" id="chatHeader">
              <div class="header-left">
                <div class="header-dot"></div>
                <span class="header-title">${config.title}</span>
              </div>
              <div class="header-actions">
                <button class="header-btn" id="refreshBtn" aria-label="New conversation" title="New conversation">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polyline points="23 4 23 10 17 10"/>
                    <path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/>
                  </svg>
                </button>
                <button class="header-btn" id="closeBtn" aria-label="Close chat">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <line x1="18" y1="6" x2="6" y2="18"/>
                    <line x1="6" y1="6" x2="18" y2="18"/>
                  </svg>
                </button>
              </div>
            </div>
            <div class="chat-messages" id="messages">
              <div class="message assistant">
                <div class="message-content">${config.greeting}</div>
              </div>
            </div>
            <div class="typing-indicator" id="typing" style="display:none">
              <div class="typing-dots">
                <span></span><span></span><span></span>
              </div>
            </div>
            <div class="chat-input-area">
              <textarea id="input" placeholder="Type your message..." rows="1"></textarea>
              <button id="sendBtn" aria-label="Send message">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <line x1="22" y1="2" x2="11" y2="13"/>
                  <polygon points="22 2 15 22 11 13 2 9 22 2"/>
                </svg>
              </button>
            </div>
          </div>
        </div>
      `;
    }

    _getStyles() {
      const c = config.color;
      return `
        :host {
          position: fixed;
          bottom: 24px;
          right: 24px;
          z-index: 999999;
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
          font-size: 14px;
          line-height: 1.5;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }

        .widget-container { position: relative; }

        /* FAB */
        .fab {
          width: 56px; height: 56px; border-radius: 50%;
          background: ${c}; color: white; border: none; cursor: grab;
          display: flex; align-items: center; justify-content: center;
          box-shadow: 0 4px 12px rgba(0,0,0,0.15);
          transition: transform 0.2s, box-shadow 0.2s;
        }
        .fab:active { cursor: grabbing; }
        .fab:hover { transform: scale(1.05); box-shadow: 0 6px 20px rgba(0,0,0,0.2); }

        /* Chat Window */
        .chat-window {
          display: none; flex-direction: column;
          width: 380px; height: 520px;
          min-width: 300px; min-height: 350px;
          max-width: 90vw; max-height: 90vh;
          background: #fff; border-radius: 12px;
          box-shadow: 0 8px 32px rgba(0,0,0,0.15);
          overflow: hidden;
          position: absolute; bottom: 0; right: 0;
        }
        .chat-window.open { display: flex; }

        /* Top-left resize handle */
        .resize-handle {
          position: absolute; top: 0; left: 0;
          width: 18px; height: 18px;
          cursor: nw-resize; z-index: 10;
        }
        .resize-handle::after {
          content: '';
          position: absolute; top: 4px; left: 4px;
          width: 8px; height: 8px;
          border-top: 2px solid rgba(255,255,255,0.5);
          border-left: 2px solid rgba(255,255,255,0.5);
          border-radius: 2px 0 0 0;
        }

        /* Header */
        .chat-header {
          background: ${c}; color: white;
          padding: 14px 16px; display: flex;
          align-items: center; justify-content: space-between;
          cursor: grab; user-select: none;
          flex-shrink: 0;
        }
        .chat-header:active { cursor: grabbing; }
        .header-left { display: flex; align-items: center; gap: 8px; }
        .header-dot {
          width: 8px; height: 8px; border-radius: 50%;
          background: #4ade80; flex-shrink: 0;
        }
        .header-title { font-weight: 600; font-size: 15px; }
        .header-actions { display: flex; gap: 4px; }
        .header-btn {
          background: rgba(255,255,255,0.15); border: none; color: white;
          width: 28px; height: 28px; border-radius: 6px;
          display: flex; align-items: center; justify-content: center;
          cursor: pointer; transition: background 0.15s;
        }
        .header-btn:hover { background: rgba(255,255,255,0.3); }

        /* Messages */
        .chat-messages {
          flex: 1; overflow-y: auto; padding: 16px;
          display: flex; flex-direction: column; gap: 12px;
        }
        .message { display: flex; flex-direction: column; max-width: 85%; }
        .message.user { align-self: flex-end; }
        .message.assistant { align-self: flex-start; }
        .message-content {
          padding: 10px 14px; border-radius: 12px;
          word-wrap: break-word; white-space: pre-wrap; overflow: hidden;
        }
        .message-content ul, .message-content ol,
        .message-content li { white-space: normal; }
        .message.user .message-content {
          background: ${c}; color: white;
          border-bottom-right-radius: 4px;
        }
        .message.assistant .message-content {
          background: #f1f5f9; color: #1e293b;
          border-bottom-left-radius: 4px;
        }
        .message-content p { margin: 0 0 8px 0; }
        .message-content p:last-child { margin-bottom: 0; }
        .message-content strong { font-weight: 600; }
        .message-content code {
          background: rgba(0,0,0,0.06); padding: 1px 4px;
          border-radius: 3px; font-size: 13px;
          font-family: 'SF Mono', Monaco, monospace;
        }
        .message-content ul, .message-content ol {
          margin: 4px 0; padding-left: 1.5em; list-style-position: outside;
        }
        .message-content li { margin: 2px 0; padding-left: 0.25em; }
        .message-content h2 { font-size: 15px; font-weight: 600; margin: 8px 0 4px; }
        .message-content h3 { font-size: 14px; font-weight: 600; margin: 6px 0 4px; }
        .message-content table {
          border-collapse: collapse; margin: 8px 0; font-size: 13px; width: 100%;
        }
        .message-content th, .message-content td {
          border: 1px solid #ddd; padding: 4px 8px; text-align: left;
        }
        .message-content th { background: #f8fafc; font-weight: 600; }

        /* Typing indicator */
        .typing-indicator {
          padding: 8px 16px; flex-shrink: 0;
        }
        .typing-dots {
          display: inline-flex; gap: 4px; padding: 8px 14px;
          background: #f1f5f9; border-radius: 12px;
        }
        .typing-dots span {
          width: 6px; height: 6px; border-radius: 50%;
          background: #94a3b8; animation: bounce 1.4s infinite ease-in-out;
        }
        .typing-dots span:nth-child(1) { animation-delay: -0.32s; }
        .typing-dots span:nth-child(2) { animation-delay: -0.16s; }
        @keyframes bounce {
          0%, 80%, 100% { transform: scale(0); }
          40% { transform: scale(1); }
        }

        /* Input area */
        .chat-input-area {
          display: flex; align-items: flex-end; gap: 8px;
          padding: 12px 16px; border-top: 1px solid #e2e8f0;
          flex-shrink: 0;
        }
        textarea {
          flex: 1; border: 1px solid #e2e8f0; border-radius: 8px;
          padding: 8px 12px; font-size: 14px; font-family: inherit;
          resize: none; outline: none; max-height: 100px;
          line-height: 1.4; transition: border-color 0.15s;
        }
        textarea:focus { border-color: ${c}; }
        #sendBtn {
          width: 36px; height: 36px; border-radius: 8px;
          background: ${c}; color: white; border: none;
          display: flex; align-items: center; justify-content: center;
          cursor: pointer; flex-shrink: 0; transition: opacity 0.15s;
        }
        #sendBtn:hover { opacity: 0.9; }
        #sendBtn:disabled { opacity: 0.5; cursor: not-allowed; }

        /* Mobile */
        @media (max-width: 440px) {
          :host { bottom: 0; right: 0; left: 0; }
          .chat-window {
            width: 100vw; height: 100vh; height: 100dvh;
            border-radius: 0; bottom: 0; right: 0;
            position: fixed;
          }
        }
      `;
    }

    _bindEvents() {
      const $ = (id) => this.shadowRoot.getElementById(id);

      // Toggle chat (only if FAB wasn't dragged)
      $("fab").addEventListener("click", () => {
        if (this._fabDragged) { this._fabDragged = false; return; }
        this._toggle();
      });
      $("closeBtn").addEventListener("click", () => this._toggle());

      // Refresh / new conversation
      $("refreshBtn").addEventListener("click", () => this._newConversation());

      // Send message
      $("sendBtn").addEventListener("click", () => this._send());
      $("input").addEventListener("keydown", (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
          e.preventDefault();
          this._send();
        }
      });

      // Auto-resize textarea
      $("input").addEventListener("input", (e) => {
        e.target.style.height = "auto";
        e.target.style.height = Math.min(e.target.scrollHeight, 100) + "px";
      });

      // Drag
      this._initDrag();

      // Resize from top-left
      this._initResize();
    }

    _initDrag() {
      const header = this.shadowRoot.getElementById("chatHeader");
      const fab = this.shadowRoot.getElementById("fab");
      const host = this;

      // Track whether it was a drag or a click on the FAB
      this._fabDragged = false;

      const startDrag = (clientX, clientY) => {
        this._isDragging = true;
        const rect = host.getBoundingClientRect();
        this._dragOffset = { x: clientX - rect.left, y: clientY - rect.top };
      };

      const moveDrag = (clientX, clientY) => {
        if (!this._isDragging) return;
        this._fabDragged = true;
        const x = clientX - this._dragOffset.x;
        const y = clientY - this._dragOffset.y;
        host.style.left = Math.max(0, Math.min(x, window.innerWidth - 60)) + "px";
        host.style.top = Math.max(0, Math.min(y, window.innerHeight - 60)) + "px";
        host.style.right = "auto";
        host.style.bottom = "auto";
      };

      const endDrag = () => {
        this._isDragging = false;
      };

      // Chat header drag
      header.addEventListener("mousedown", (e) => {
        if (e.target.closest(".header-btn")) return;
        startDrag(e.clientX, e.clientY);
        e.preventDefault();
      });

      // FAB drag
      fab.addEventListener("mousedown", (e) => {
        this._fabDragged = false;
        startDrag(e.clientX, e.clientY);
        e.preventDefault();
      });

      document.addEventListener("mousemove", (e) => moveDrag(e.clientX, e.clientY));
      document.addEventListener("mouseup", endDrag);

      // Touch: header
      header.addEventListener("touchstart", (e) => {
        if (e.target.closest(".header-btn")) return;
        const t = e.touches[0];
        startDrag(t.clientX, t.clientY);
      }, { passive: true });

      // Touch: FAB
      fab.addEventListener("touchstart", (e) => {
        this._fabDragged = false;
        const t = e.touches[0];
        startDrag(t.clientX, t.clientY);
      }, { passive: true });

      document.addEventListener("touchmove", (e) => {
        if (!this._isDragging) return;
        const t = e.touches[0];
        moveDrag(t.clientX, t.clientY);
      }, { passive: true });

      document.addEventListener("touchend", endDrag);
    }

    _initResize() {
      const handle = this.shadowRoot.getElementById("resizeHandle");
      const chatWindow = this.shadowRoot.getElementById("chatWindow");
      let isResizing = false;
      let startX, startY, startW, startH;

      handle.addEventListener("mousedown", (e) => {
        isResizing = true;
        startX = e.clientX;
        startY = e.clientY;
        startW = chatWindow.offsetWidth;
        startH = chatWindow.offsetHeight;
        e.preventDefault();
        e.stopPropagation();
      });

      document.addEventListener("mousemove", (e) => {
        if (!isResizing) return;
        // Top-left: dragging left increases width, dragging up increases height
        const dw = startX - e.clientX;
        const dh = startY - e.clientY;
        const newW = Math.max(300, Math.min(startW + dw, window.innerWidth * 0.9));
        const newH = Math.max(350, Math.min(startH + dh, window.innerHeight * 0.9));
        chatWindow.style.width = newW + "px";
        chatWindow.style.height = newH + "px";
      });

      document.addEventListener("mouseup", () => {
        isResizing = false;
      });

      // Touch support
      handle.addEventListener("touchstart", (e) => {
        isResizing = true;
        const t = e.touches[0];
        startX = t.clientX;
        startY = t.clientY;
        startW = chatWindow.offsetWidth;
        startH = chatWindow.offsetHeight;
        e.stopPropagation();
      }, { passive: true });

      document.addEventListener("touchmove", (e) => {
        if (!isResizing) return;
        const t = e.touches[0];
        const dw = startX - t.clientX;
        const dh = startY - t.clientY;
        const newW = Math.max(300, Math.min(startW + dw, window.innerWidth * 0.9));
        const newH = Math.max(350, Math.min(startH + dh, window.innerHeight * 0.9));
        chatWindow.style.width = newW + "px";
        chatWindow.style.height = newH + "px";
      }, { passive: true });

      document.addEventListener("touchend", () => {
        isResizing = false;
      });
    }

    _toggle() {
      this._isOpen = !this._isOpen;
      const chatWindow = this.shadowRoot.getElementById("chatWindow");
      const fab = this.shadowRoot.getElementById("fab");
      chatWindow.classList.toggle("open", this._isOpen);
      fab.style.display = this._isOpen ? "none" : "flex";

      if (this._isOpen && !this._ws) {
        this._connect();
      }
      if (this._isOpen) {
        setTimeout(() => this.shadowRoot.getElementById("input")?.focus(), 100);
      }
    }

    _connect() {
      const resuming = !!this._sessionId;
      const wsUrl = `${config.server}/ws/chat${this._sessionId ? "?session_id=" + this._sessionId : ""}`;
      this._ws = new WebSocket(wsUrl);

      this._ws.onopen = () => {
        this._reconnectAttempts = 0;
      };

      this._ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        switch (data.type) {
          case "session":
            this._sessionId = data.session_id;
            sessionStorage.setItem("clinicdesk_session_id", data.session_id);
            if (resuming) this._loadPreviousMessages(data.session_id);
            break;
          case "typing":
            this.shadowRoot.getElementById("typing").style.display = data.status
              ? "block"
              : "none";
            if (data.status) this._scrollToBottom();
            break;
          case "message":
            this._addMessage("assistant", data.content);
            this.shadowRoot.getElementById("typing").style.display = "none";
            this._enableInput();
            break;
          case "error":
            this._addMessage("assistant", "Sorry, something went wrong. Please try again.");
            this.shadowRoot.getElementById("typing").style.display = "none";
            this._enableInput();
            break;
        }
      };

      this._ws.onclose = () => {
        if (this._isOpen && this._reconnectAttempts < this._maxReconnectAttempts) {
          this._reconnectAttempts++;
          setTimeout(() => this._connect(), 1000 * this._reconnectAttempts);
        }
      };

      this._ws.onerror = () => {};
    }

    async _loadPreviousMessages(sessionId) {
      try {
        const httpBase = config.server.replace(/^ws/, "http");
        const url = `${httpBase}/api/sessions/${sessionId}/messages`;
        const res = await fetch(url);
        if (!res.ok) return;
        const data = await res.json();
        if (!data.messages || data.messages.length === 0) return;

        // Clear the greeting and show actual conversation history
        const messages = this.shadowRoot.getElementById("messages");
        messages.innerHTML = "";

        for (const msg of data.messages) {
          this._addMessage(msg.role, msg.content);
        }
      } catch (e) {
        // Silently fail — user just sees the greeting instead
      }
    }

    _send() {
      const input = this.shadowRoot.getElementById("input");
      const text = input.value.trim();
      if (!text || !this._ws || this._ws.readyState !== WebSocket.OPEN) return;

      this._addMessage("user", text);
      this._ws.send(JSON.stringify({ type: "message", content: text }));
      input.value = "";
      input.style.height = "auto";
      this._disableInput();
    }

    _addMessage(role, content) {
      const messages = this.shadowRoot.getElementById("messages");
      const div = document.createElement("div");
      div.className = `message ${role}`;
      const contentDiv = document.createElement("div");
      contentDiv.className = "message-content";
      contentDiv.innerHTML = role === "assistant" ? this._renderMarkdown(content) : this._escapeHtml(content);
      div.appendChild(contentDiv);
      messages.appendChild(div);
      this._scrollToBottom();
    }

    _renderMarkdown(text) {
      if (!text) return "";
      let html = this._escapeHtml(text);

      // Tables
      html = html.replace(
        /^(\|.+\|)\n(\|[\s\-:|]+\|)\n((?:\|.+\|\n?)+)/gm,
        (match, header, sep, body) => {
          const headers = header.split("|").filter(c => c.trim());
          const rows = body.trim().split("\n").map(r => r.split("|").filter(c => c.trim()));
          let table = "<table><thead><tr>";
          headers.forEach(h => (table += `<th>${h.trim()}</th>`));
          table += "</tr></thead><tbody>";
          rows.forEach(r => {
            table += "<tr>";
            r.forEach(c => (table += `<td>${c.trim()}</td>`));
            table += "</tr>";
          });
          return table + "</tbody></table>";
        }
      );

      // Headers
      html = html.replace(/^### (.+)$/gm, "<h3>$1</h3>");
      html = html.replace(/^## (.+)$/gm, "<h2>$1</h2>");

      // Bold and italic
      html = html.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
      html = html.replace(/\*(.+?)\*/g, "<em>$1</em>");

      // Inline code
      html = html.replace(/`([^`]+)`/g, "<code>$1</code>");

      // Unordered lists
      html = html.replace(/^[\-\*] (.+)$/gm, "<li>$1</li>");
      html = html.replace(/((?:<li>.*<\/li>\n?)+)/g, "<ul>$1</ul>");

      // Ordered lists
      html = html.replace(/^\d+\. (.+)$/gm, "<li>$1</li>");

      // Paragraphs (double newlines)
      html = html.replace(/\n\n/g, "</p><p>");
      html = `<p>${html}</p>`;
      html = html.replace(/<p><\/p>/g, "");

      // Clean up
      html = html.replace(/<p>(<h[23]>)/g, "$1");
      html = html.replace(/(<\/h[23]>)<\/p>/g, "$1");
      html = html.replace(/<p>(<ul>)/g, "$1");
      html = html.replace(/(<\/ul>)<\/p>/g, "$1");
      html = html.replace(/<p>(<table>)/g, "$1");
      html = html.replace(/(<\/table>)<\/p>/g, "$1");

      return html;
    }

    _escapeHtml(text) {
      const div = document.createElement("div");
      div.textContent = text;
      return div.innerHTML;
    }

    _scrollToBottom() {
      const messages = this.shadowRoot.getElementById("messages");
      requestAnimationFrame(() => {
        messages.scrollTop = messages.scrollHeight;
      });
    }

    _disableInput() {
      this.shadowRoot.getElementById("input").disabled = true;
      this.shadowRoot.getElementById("sendBtn").disabled = true;
    }

    _enableInput() {
      this.shadowRoot.getElementById("input").disabled = false;
      this.shadowRoot.getElementById("sendBtn").disabled = false;
      this.shadowRoot.getElementById("input").focus();
    }

    _newConversation() {
      // Close existing WebSocket
      if (this._ws) {
        this._ws.close();
        this._ws = null;
      }

      // Clear session
      this._sessionId = null;
      sessionStorage.removeItem("clinicdesk_session_id");

      // Clear messages and add greeting
      const messages = this.shadowRoot.getElementById("messages");
      messages.innerHTML = `
        <div class="message assistant">
          <div class="message-content">${config.greeting}</div>
        </div>
      `;

      // Hide typing indicator
      this.shadowRoot.getElementById("typing").style.display = "none";

      // Re-enable input
      this._enableInput();

      // Reconnect
      this._reconnectAttempts = 0;
      this._connect();
    }

    _restoreSession() {
      const saved = sessionStorage.getItem("clinicdesk_session_id");
      if (saved) this._sessionId = saved;
    }
  }

  customElements.define("clinicdesk-widget", ClinicDeskWidget);

  // Auto-insert into page
  if (!document.querySelector("clinicdesk-widget")) {
    document.body.appendChild(document.createElement("clinicdesk-widget"));
  }
})();
