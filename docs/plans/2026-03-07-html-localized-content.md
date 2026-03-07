# HTML Localized Content Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Render localized content directly into generated HTML files and remove `site-data.js` as the content source.

**Architecture:** Keep `metadata/` as the source of truth and `scripts/build_localized_site.py` as the site generator. Emit complete localized HTML at build time, then simplify `script.js` so it only handles interactive behavior that reads from the DOM.

**Tech Stack:** Python site generator, static HTML/CSS/JavaScript, pytest

---

### Task 1: Add failing coverage for HTML-rendered localized content

**Files:**
- Modify: `tests/site_variants_test.py`

**Step 1: Write the failing test**

Add assertions that generated locale pages contain localized content directly in HTML and no longer include `site-data.js`.

**Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/site_variants_test.py -q`
Expected: FAIL because generated pages still reference `site-data.js` and rely on placeholders for content.

**Step 3: Write minimal implementation**

No implementation in this task.

**Step 4: Run test to verify it still fails for the expected reason**

Run: `python3 -m pytest tests/site_variants_test.py -q`
Expected: FAIL with assertions tied to old generated output.

### Task 2: Render localized content directly into generated HTML

**Files:**
- Modify: `scripts/build_localized_site.py`

**Step 1: Write the minimal generator changes**

Update homepage, support, and privacy templates so localized strings are emitted directly into HTML instead of placeholder nodes.

**Step 2: Stop emitting `site-data.js` references**

Remove `site-data.js` script tags from generated pages and stop generating per-locale content payload files.

**Step 3: Rebuild localized output**

Run: `python3 scripts/build_localized_site.py`

**Step 4: Re-run the targeted tests**

Run: `python3 -m pytest tests/site_variants_test.py -q`
Expected: PASS

### Task 3: Simplify runtime JavaScript to behavior-only usage

**Files:**
- Modify: `script.js`

**Step 1: Remove `window.siteData` content dependencies**

Replace content/asset resolution logic with DOM-driven behavior.

**Step 2: Keep interactive behavior working**

Preserve locale switching, gallery lightbox behavior, and time/theme-based screenshot behavior.

**Step 3: Re-run targeted tests and rebuild**

Run: `python3 scripts/build_localized_site.py`
Run: `python3 -m pytest tests/site_variants_test.py -q`
Expected: PASS

### Task 4: Clean up generated artifacts and verify output

**Files:**
- Modify: generated locale HTML files
- Delete: generated locale `site-data.js` files if unused

**Step 1: Rebuild the site**

Run: `python3 scripts/build_localized_site.py`

**Step 2: Verify generated output**

Inspect representative files such as `en-US/index.html`, `ja/index.html`, and `en-US/support.html` for direct localized HTML content and no `site-data.js` references.

**Step 3: Run the full relevant verification**

Run: `python3 -m pytest tests/site_variants_test.py -q`
Expected: PASS
