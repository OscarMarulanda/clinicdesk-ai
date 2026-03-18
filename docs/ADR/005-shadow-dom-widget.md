# ADR-005: Shadow DOM for Chat Widget Encapsulation

## Status
Accepted

## Context
The chat widget must be embeddable on any website via a single `<script>` tag. Need style isolation to prevent conflicts with host page CSS.

Options considered:
1. **Shadow DOM** — native browser encapsulation, styles don't leak in or out
2. **iframe** — full isolation but harder to communicate with, accessibility challenges
3. **CSS scoping with prefixes** — manual namespacing, fragile, can still be overridden by host styles

## Decision
Use Shadow DOM for style isolation.

## Rationale
- **True style isolation**: Host page CSS cannot affect widget, widget CSS cannot affect host page
- **Native browser feature**: No library needed, supported in all modern browsers
- **Single script embed**: Widget creates its own shadow root, no iframe complexities
- **Event handling works naturally**: Unlike iframes, Shadow DOM elements participate in the same document's event system
- **Lightweight**: No extra network requests (unlike iframe which loads a separate page)

## Trade-offs
- Slightly more complex initial setup than plain DOM
- Some older CSS frameworks may need adaptation inside shadow root
- Slots and custom elements add minor complexity

## Implementation
```javascript
class ClinicDeskWidget extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
    // All styles and DOM go inside shadow root
  }
}
customElements.define('clinicdesk-widget', ClinicDeskWidget);
```
