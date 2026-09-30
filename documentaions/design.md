# IP-SAKTI Sahayak — Design System Specification (DESIGN.md)

> **Standard:** Inspired by `getdesign.md`, `vibecurb.pages.dev`, `tasteskill.dev`, `sitepeel.dev`, and `duply.ai/library`.
> **Theme:** Luminous White & Herbal Light Green (Modern Ayurvedic Intellectual Property Tech).

---

## 1. Brand & Aesthetic Vision

**IP-SAKTI Sahayak** is a premier legal and regulatory intelligence platform for the Ministry of Ayush, Government of India. The visual aesthetic embodies:
- **Luminous Clarity:** Pristine white canvases paired with soothing sage, mint, and emerald botanicals.
- **Human-Crafted Elegance:** Thoughtful negative space, subtle organic micro-animations, glassmorphism cards, and refined badge typography.
- **Cultural Respect & Legal Authority:** Ancient Ayurvedic herbals meeting contemporary high-precision IP jurisprudence.

---

## 2. Color Palette & Tokens (White & Light Green System)

```css
:root {
  /* Surfaces */
  --bg-page: #FFFFFF;
  --bg-surface-tint: #F7FCF9;
  --surface-card: #FFFFFF;
  --surface-card-translucent: rgba(255, 255, 255, 0.92);
  --surface-hover: #F0FDF4;

  /* Borders */
  --border-light: #E2E8F0;
  --border-emerald-soft: #D1FAE5;
  --border-emerald-active: #10B981;

  /* Herbal & Primary Green Accents */
  --primary-emerald: #059669;
  --primary-emerald-hover: #047857;
  --mint-light: #ECFDF5;
  --mint-badge: #D1FAE5;
  --sage-accent: #34D399;
  --emerald-shadow: rgba(16, 185, 129, 0.12);

  /* Warm Ayurvedic Accents */
  --saffron-gold: #D97706;
  --amber-light: #FEF3C7;

  /* Text & Ink */
  --text-main: #0F172A;        /* Slate-900 / Deep ink */
  --text-body: #334155;        /* Slate-700 */
  --text-muted: #64748B;       /* Slate-500 */
  --text-emerald-dark: #065F46; /* Deep forest green */
}
```

---

## 3. Typography & Styling Rules

- **Font Family:** `Plus Jakarta Sans` or `Inter`, system fallback.
- **Hierarchy:** High-contrast headings in slate-900 with subtle emerald gradient accents.
- **Borders & Shadows:** 1px soft emerald-tinted borders with diffused ambient blur (`0 10px 30px -5px rgba(16, 185, 129, 0.08)`).
- **Interactive States:** Soft scale (`scale-[1.01]`), smooth 200ms transitions, subtle green glow outlines.
