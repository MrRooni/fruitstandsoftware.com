# 40 Below Homepage Iteration Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Refine the chosen homepage direction by collapsing the metadata description into the hero, adding a support nav link, and deleting the unused variant files.

**Architecture:** Keep the shared data and rendering model, but simplify the tests and file surface to a single homepage. Move the descriptive content block into the hero markup and introduce a minimal header/nav above the main content.

**Tech Stack:** Static HTML, CSS, and vanilla JavaScript

---

### Task 1: Update regression coverage for the single-page direction

**Files:**
- Modify: `tests/site_variants_test.py`
- Test: `tests/site_variants_test.py`

**Step 1: Write the failing test**

Require:
- only `index.html` remains as the marketing page under test
- `variant-2.html` through `variant-5.html` do not exist
- `index.html` contains a support nav link
- the hero contains the description and feature list block

**Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests/site_variants_test.py`
Expected: FAIL because the variant files still exist and the support nav is missing.

**Step 3: Write minimal implementation**

Delete the variant files and update `index.html` to match the new structure.

**Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests/site_variants_test.py`
Expected: PASS

### Task 2: Move the descriptive content into the hero and add support nav

**Files:**
- Modify: `index.html`
- Modify: `styles/base.css`
- Modify: `styles/variant-1.css`
- Test: `tests/site_variants_test.py`

**Step 1: Write the failing test**

Require:
- hero contains `data-site="description-paragraphs"`
- hero contains `data-site="feature-list"`
- top nav contains `href="support.html"`

**Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests/site_variants_test.py`
Expected: FAIL because those elements are not yet in the hero/nav structure.

**Step 3: Write minimal implementation**

Add a small header nav, move the description and features into the hero content column, and top-align the hero columns.

**Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests/site_variants_test.py`
Expected: PASS

### Task 3: Verify formatting and final constraints

**Files:**
- Modify: none
- Test: all changed files

**Step 1: Run formatting**

Run: `swiftformat .`
Expected: formatting completes successfully

**Step 2: Run regression tests**

Run: `python3 -m unittest tests/site_variants_test.py`
Expected: PASS
