# ClinicDesk AI — Demo Script

## Live URLs

- **Chat Widget:** https://clinicdesk-ai.fly.dev/static/widget/demo.html
- **Admin Dashboard:** https://clinicdesk-ai.fly.dev/static/admin/
- **Google Calendar:** https://calendar.google.com (login: `clinicdeskai@gmail.com` / `odmb7750`)

---

## Demo 1: Support Conversation + Escalation with Callback

> Shows: multi-step conversation, knowledge base search, escalation flow, calendar booking, email notifications

**Chat Widget** (https://clinicdesk-ai.fly.dev/static/widget/demo.html)

1. Open the chat widget
2. Type: **"How do I submit an insurance pre-authorization?"**
   - The agent searches the knowledge base and walks you through the steps
3. Type: **"What about connecting an X-ray machine to the system?"**
   - The agent won't find this in the KB — it offers to escalate
4. When asked, provide:
   - Email: your email
   - Preference: **callback**
   - Time: **tomorrow at 2pm**
5. The agent checks calendar availability, shows open slots
6. Pick a slot — the agent books the callback, sends confirmation emails

**Verify:**
- Check your email for the confirmation
- Check the Google Calendar (`clinicdeskai@gmail.com` / `odmb7750`) — the event is there
- Open the **Admin Dashboard** → Escalations tab — the escalation appears with full transcript

---

## Demo 2: Knowledge Base Feedback Loop + Document Ingestion

> Shows: the system improves over time without code changes, and AI-powered document ingestion

**Admin Dashboard** (https://clinicdesk-ai.fly.dev/static/admin/)

Login: `clinicdeskai@gmail.com` / `odmb7750` (or create your own account via Sign Up)

**Part A — Show the gap:**
1. Go to the **Chat Widget** and ask: **"What's the no-show fee?"** or **"What's our cancellation fee policy?"**
   - The KB has no article about cancellation/no-show fees — the agent won't find an answer and will offer to escalate

**Part B — Fill the gap with drag-and-drop:**
2. Open the **Admin Dashboard** → Knowledge Base tab
3. Drag `docs/demo_cancellation_policy.pdf` onto the dashboard — a blue drop overlay appears
4. Release it — the AI extracts the text, structures it as a KB article, and opens a review modal
5. Review the title, category, and content — edit if needed
6. Click **Save Article**

**Part C — Verify the loop is closed:**
7. Go back to the **Chat Widget** and ask the same question: **"What's the no-show fee?"**
   - The agent now answers from the article you just imported — no code changes, no restart

**Bonus:** Try the same flow with `docs/demo_billing_reconciliation.pdf` — ask **"How do I do end-of-day reconciliation?"** before and after importing it

---

## Demo 4: Real-Time Notifications

> Shows: admin is notified instantly when escalations happen

1. Open the **Admin Dashboard** in one browser tab
2. Open the **Chat Widget** in another tab
3. Trigger an escalation in the chat (ask something out of scope, request a callback)
4. Watch the admin dashboard — the notification bell updates in real time
5. Click the notification to jump directly to the escalation detail

---

## Demo 5: Analytics & Cost Tracking

> Shows: operational visibility for managing the support agent

1. In the Admin Dashboard, go to the **Analytics** tab
2. View metrics: total sessions, escalation rate, resolution rate
3. **Cost Overview** card shows total spend and average cost per session (Sonnet 4.6 pricing)
4. **Token Usage** card shows input/output token breakdown
5. Toggle between 7d / 30d / 90d views
6. Click into any **Session** to see per-turn token counts, cost breakdown, and tool call log

---

## Key Things to Notice

- **Double-booking prevention:** Try booking a callback at a time that's already taken — the agent will show alternative slots
- **No upfront forms:** The agent collects information conversationally, not through a form wall
- **Embeddable widget:** Single `<script>` tag deployment with Shadow DOM isolation
- **Clean Architecture:** Backend has 72 tests across all 4 layers, any component is swappable
- **Real integrations:** Google Calendar and SendGrid are live, not mocked
