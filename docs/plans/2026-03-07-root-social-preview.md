# Root Social Preview Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Restore social previews for `https://fruitstandsoftware.com/` without slowing the existing locale redirect.

**Architecture:** Keep the current client-side redirect shell at the root URL and add static share metadata to its `<head>`. Generate the root social tags from the default locale's existing metadata so the preview stays consistent with the product copy while avoiding any runtime redirect changes.

**Tech Stack:** Static HTML generation via `scripts/build_localized_site.py`, Python `unittest`

---

### Task 1: Cover the root share card with a regression test

**Files:**
- Modify: `tests/site_variants_test.py`

**Step 1: Write the failing test**

Add assertions that the root redirect shell contains:
- `description`
- `og:title`
- `og:description`
- `og:type`
- `og:url`
- `og:image`
- `twitter:card`
- `twitter:image`
- root canonical URL

**Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.site_variants_test.SiteVariantsTest.test_root_index_is_a_redirect_shell`
Expected: FAIL because the redirect shell lacks social metadata.

**Step 3: Write minimal implementation**

Update `scripts/build_localized_site.py` so `render_root_redirect()` emits static share metadata using the default locale's title and promotional copy plus a single absolute preview image URL. Use `SocialImage.png` for the root share card.

**Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests.site_variants_test.SiteVariantsTest.test_root_index_is_a_redirect_shell`
Expected: PASS

### Task 2: Regenerate and verify generated output

**Files:**
- Modify: `scripts/build_localized_site.py`
- Modify: `index.html`

**Step 1: Rebuild generated files**

Run: `python3 scripts/build_localized_site.py`
Expected: `index.html` is regenerated with the new root metadata.

**Step 2: Run full verification**

Run: `python3 -m unittest tests.site_variants_test`
Expected: PASS

**Step 3: Run formatting required by repo instructions**

Run: `swiftformat .`
Expected: either no changes or formatter-applied changes with exit code 0
