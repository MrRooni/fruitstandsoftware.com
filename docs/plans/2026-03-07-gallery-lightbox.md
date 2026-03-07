# Gallery Lightbox Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add a screenshot gallery below the release notes on the homepage with a full-screen lightbox, swipe navigation, keyboard support, and minimalist arrow controls.

**Architecture:** Keep the gallery markup on `index.html` so the six screenshots are directly addressable and fast to load. Add shared gallery/lightbox styling in `styles/base.css`, then extend `script.js` with a small gallery controller that opens the modal, updates the active image, handles swipe gestures, and preserves accessible dialog behavior.

**Tech Stack:** Static HTML, CSS, vanilla JavaScript, Python `unittest`

---

### Task 1: Add gallery and lightbox markup

**Files:**
- Modify: `index.html`

**Step 1: Add the gallery section**

Insert a new section below the release notes with:
- a simple heading
- six thumbnail buttons in the requested order
- `data-gallery-index` attributes for selection

**Step 2: Add the lightbox shell**

Append a hidden dialog-like overlay with:
- close button
- previous and next buttons
- active image element
- active image counter/status text

**Step 3: Keep accessibility explicit**

Use:
- button elements for thumbnails and controls
- `aria-label` text for close/next/previous actions
- `role="dialog"` and `aria-modal="true"` on the overlay

### Task 2: Add gallery and modal styling

**Files:**
- Modify: `styles/base.css`

**Step 1: Add gallery card styles**

Create a responsive grid with portrait thumbnail tiles and consistent spacing below the release notes section.

**Step 2: Add lightbox styles**

Create a fixed overlay, centered image stage, minimal arrow controls, close control, and darkened backdrop that works in light and dark mode.

**Step 3: Add responsive behavior**

Ensure controls and layout scale down on narrower screens without clipping the screenshots.

### Task 3: Implement lightbox behavior

**Files:**
- Modify: `script.js`

**Step 1: Define the gallery image model**

Add the six screenshot paths and human-readable labels in one ordered array.

**Step 2: Wire gallery interactions**

Implement:
- thumbnail click to open modal
- next/previous navigation
- close action
- Escape key to close
- left/right arrow navigation

**Step 3: Add swipe support**

Track touch start/end positions and move to previous/next image using a small threshold.

### Task 4: Add regression coverage

**Files:**
- Modify: `tests/site_variants_test.py`

**Step 1: Assert gallery markup exists**

Check for:
- gallery section
- six expected image filenames
- lightbox shell hooks

**Step 2: Assert script logic exists**

Check for:
- swipe threshold handling
- keyboard navigation
- modal open/close wiring

### Task 5: Verify

**Files:**
- Modify: none

**Step 1: Run tests**

Run: `python3 -m unittest tests/site_variants_test.py`

**Step 2: Run formatter**

Run: `swiftformat .`
