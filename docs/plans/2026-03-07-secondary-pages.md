# 40 Below Secondary Pages Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Redesign `support.html` and `privacy-policy.html` so they share the homepage shell and visual language while preserving their exact content.

**Architecture:** Move both pages onto `styles/base.css` plus a shared secondary-page stylesheet. Keep their copy unchanged, but replace the legacy header/footer/layout structure with the homepage navigation shell, card system, and dark-mode tokens.

**Tech Stack:** Static HTML, CSS, and vanilla JavaScript

---

### Task 1: Add regression checks for secondary-page shell structure

**Files:**
- Modify: `tests/site_variants_test.py`
- Test: `tests/site_variants_test.py`

**Step 1: Write the failing test**

Require:
- `support.html` and `privacy-policy.html` use `styles/base.css`
- both pages use the homepage-style `top-nav`
- neither page references `styles.css` or Google Fonts

**Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests/site_variants_test.py`
Expected: FAIL because both pages still use the legacy structure.

**Step 3: Write minimal implementation**

Update both pages to the new shared shell until the test passes.

**Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests/site_variants_test.py`
Expected: PASS

### Task 2: Add shared secondary-page styles and rebuild support/privacy structure

**Files:**
- Modify: `support.html`
- Modify: `privacy-policy.html`
- Create: `styles/secondary-pages.css`
- Test: `tests/site_variants_test.py`

**Step 1: Write the failing test**

Require:
- support page has card-based main sections
- privacy page has card-based header/article/sidebar sections
- homepage footer treatment is present on both pages

**Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests/site_variants_test.py`
Expected: FAIL because the old markup is still present.

**Step 3: Write minimal implementation**

Rebuild both pages with:
- shared `top-nav`
- shared page shell
- secondary-page cards
- existing text unchanged

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
