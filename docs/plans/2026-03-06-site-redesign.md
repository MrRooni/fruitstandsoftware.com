# 40 Below Site Redesign Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Rebuild the five standalone marketing pages so they use only metadata copy, the official Apple App Store badge assets, and the simplified four-color palette.

**Architecture:** Keep a shared `site-data.js` file, but reduce it to exact metadata-derived strings and arrays only. Use one shared base stylesheet for accessibility and structure, then let the five variant stylesheets create meaningful visual differences without adding comparison UI or extra copy.

**Tech Stack:** Static HTML, CSS, and vanilla JavaScript

---

### Task 1: Add regression checks for the stricter content rules

**Files:**
- Modify: `tests/site_variants_test.py`
- Test: `tests/site_variants_test.py`

**Step 1: Write the failing test**

Extend the regression test to require:
- official App Store badge assets from `Download-on-the-App-Store/US`
- no `variant` or comparison UI text in the page body
- no known invented copy strings from the earlier redesign
- no `support.html` or `privacy-policy.html` links in the standalone variants

**Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests/site_variants_test.py`
Expected: FAIL because the current pages still include comparison language and secondary links.

**Step 3: Write minimal implementation**

Remove the comparison UI and update the CTA structure and copy sources until the test passes.

**Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests/site_variants_test.py`
Expected: PASS

### Task 2: Replace the shared content layer with metadata-only copy

**Files:**
- Modify: `site-data.js`
- Modify: `script.js`
- Test: `tests/site_variants_test.py`

**Step 1: Write the failing test**

Extend the regression test to require:
- metadata-based body sections only
- the release note text from metadata
- the exact screenshot dimensions already enforced

**Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests/site_variants_test.py`
Expected: FAIL because `site-data.js` still contains invented structure and copy.

**Step 3: Write minimal implementation**

Reduce `site-data.js` to:
- metadata-derived hero strings
- description paragraphs
- feature bullets extracted from `description.txt`
- location/privacy sentence
- release notes
- badge asset paths

Update `script.js` to render only those strings and lists.

**Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests/site_variants_test.py`
Expected: PASS

### Task 3: Rebuild the five standalone pages around the stricter copy model

**Files:**
- Modify: `index.html`
- Modify: `variant-2.html`
- Modify: `variant-3.html`
- Modify: `variant-4.html`
- Modify: `variant-5.html`
- Modify: `styles/base.css`
- Modify: `styles/variant-1.css`
- Modify: `styles/variant-2.css`
- Modify: `styles/variant-3.css`
- Modify: `styles/variant-4.css`
- Modify: `styles/variant-5.css`
- Test: `tests/site_variants_test.py`

**Step 1: Write the failing test**

Extend the regression test to require:
- no variant switcher markup
- no footer comparison links
- metadata-only section scaffolding
- App Store badge imagery in each page

**Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests/site_variants_test.py`
Expected: FAIL because the current markup still contains comparison UI.

**Step 3: Write minimal implementation**

Rebuild each page to:
- keep the icon beside the product name and subtitle
- link the App Store badge image to the App Store URL
- present the description and release notes without added body copy
- use only the approved palette tokens
- remain visually distinct by layout and framing

**Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests/site_variants_test.py`
Expected: PASS

### Task 4: Verify formatting and constraints

**Files:**
- Modify: none
- Test: all redesigned site files

**Step 1: Run formatting**

Run: `swiftformat .`
Expected: formatting completes successfully

**Step 2: Run regression tests**

Run: `python3 -m unittest tests/site_variants_test.py`
Expected: PASS

**Step 3: Run targeted grep checks**

Run: `rg -n "variant|Compare all 5 variants|Canonical product copy|Why it exists|Feature set|Location and privacy|Launch note" index.html variant-2.html variant-3.html variant-4.html variant-5.html`
Expected: no matches for the removed filler/comparison language
