# Design System Specification: The Sentinel Aesthetic

## 1. Overview & Creative North Star
**Creative North Star: "The Digital Forensic Lab"**

To combat the chaos of misinformation, this design system must feel like a precision instrument. We are moving away from the "generic SaaS dashboard" look. Instead, we embrace an **Editorial Intelligence**—a high-end, forensic environment where data is treated with the reverence of a printed broadsheet, but powered by the engine of a supercomputer.

We break the "template" look through:
*   **Intentional Asymmetry:** Heavy-weighted sidebars juxtaposed with airy, expansive data canvases.
*   **Micro-Depth:** Using light itself, rather than borders, to define the UI.
*   **High-Contrast Scale:** Using massive `display-lg` typography against microscopic, high-density `label-sm` metadata to create an authoritative hierarchy.

---

## 2. Colors: The Chromatic Architecture
The palette is rooted in the deep void of `surface` (#060e20), using light not as a decoration, but as a functional highlight for AI-detected insights. *Note: The system's color mode has been set to `light` in the underlying tokens for broader adaptability, though the narrative describes a dark theme. Developers should use the `surface` token as the baseline.*

### The "No-Line" Rule
**Borders are a failure of hierarchy.** Except for accessibility-mandated "Ghost Borders," you are prohibited from using 1px solid lines to section the UI. 
*   **Transition by Tone:** Define sections by shifting from `surface` to `surface-container-low`.
*   **Transition by Space:** Use the Spacing Scale (specifically `8` or `12`) to create a cognitive break between content blocks.

### Surface Hierarchy & Nesting
Treat the UI as a physical stack of semi-transparent materials:
1.  **Base Layer:** `surface` (#060e20) – The primary canvas.
2.  **Section Layer:** `surface-container-low` (#091328) – For secondary content areas.
3.  **Elevated Cards:** `surface-container` (#0f1930) – The standard container for news analysis.
4.  **Floating Elements:** `surface-bright` (#1f2b49) – For active modals or popovers.

### The "Glass & Gradient" Rule
To signify "AI Activity," use Glassmorphism on sidebars and floating panels:
*   **Background:** `surface-variant` at 60% opacity.
*   **Effect:** `backdrop-blur: 20px`.
*   **Signature Textures:** Main CTAs or AI "Risk Scores" should utilize a linear gradient from `primary` (#a3a6ff) to `primary-dim` (#6063ee) at a 135-degree angle. This adds "soul" to the data.

---

## 3. Typography: Editorial Authority
We pair **Manrope** (Display/Headline) for a high-tech, geometric authority with **Inter** (Body/Labels) for clinical legibility.

*   **The Power Gap:** Use `display-lg` (3.5rem) for critical truth-scores, then immediately drop to `body-md` (0.875rem) for the supporting evidence. This contrast mimics high-end news magazines.
*   **Functional Metadata:** Use `label-sm` in `on-surface-variant` (#a3aac4) for timestamps and source URLs. All-caps with 0.05em tracking is encouraged for these forensic details.

---

## 4. Elevation & Depth: Tonal Layering
We do not use shadows to create "pop"; we use them to simulate **Ambient Light.**

*   **The Layering Principle:** A `surface-container-highest` card sitting on a `surface` background creates a natural lift. This is our default "elevation."
*   **Ambient Shadows:** For floating tooltips or AI floating action buttons, use:
    *   `box-shadow: 0 24px 48px -12px rgba(6, 14, 32, 0.5);` 
    *   The shadow color is derived from the `surface` token, never pure black.
*   **The Ghost Border:** If a component (like an input field) risks disappearing, use `outline-variant` (#40485d) at **15% opacity**. It should be felt, not seen.

---

## 5. Components: Forensic Primitives

### Buttons (The "Signal" Components)
*   **Primary:** Gradient fill (`primary` to `primary-dim`), `on-primary` text, `xl` (1.5rem) rounded corners.
*   **Secondary:** `surface-container-highest` fill with a `primary` "Ghost Border" at 20% opacity.
*   **States:** On hover, increase the `backdrop-blur` of the button or shift the gradient intensity.

### The "Analysis" Card
*   **Style:** No borders. Background: `surface-container`. Corner radius: `lg` (1rem).
*   **Spacing:** Use `padding: 6` (1.5rem) to give data room to breathe.
*   **Content Separation:** Forbid divider lines. Use a 2px vertical accent bar of `secondary` (#34b5fa) on the left of "High Confidence" insights to create grouping.

### Input Fields
*   **Style:** `surface-container-lowest` fill. 
*   **Focus State:** Transition the "Ghost Border" from 15% to 60% opacity using the `tertiary` (#a1ffef) token.

### Data Visualization (The "Forensic" Charts)
*   **Truth Gradients:** Use a gradient from `tertiary` (True) to `error` (Fake). 
*   **Interaction:** Tooltips must use the Glassmorphism rule (60% opacity `surface-bright` + blur).

---

## 6. Do’s and Don’ts

### Do
*   **Do** use `surface-container-high` to highlight "breaking news" within a list of `surface-container-low` items.
*   **Do** use `secondary` (#34b5fa) for AI-suggested actions; it is our "Human-AI Synergy" color.
*   **Do** respect the `xl` (1.5rem) roundedness for large containers to soften the "high-tech" coldness.

### Don’t
*   **Don’t** use pure white (#ffffff) for text. Always use `on-surface` (#dee5ff) to reduce eye strain in dark environments.
*   **Don’t** use 1px dividers between list items. Use a `1.5` (0.375rem) vertical gap instead.
*   **Don’t** use standard drop shadows. If it doesn't look like it's glowing or floating in a thick atmosphere, the shadow is too harsh.