# HTML Localized Content Design

## Summary

Move localized strings out of per-locale `site-data.js` files and render them directly into generated HTML files at build time. Keep `metadata/` as the source of truth and preserve JavaScript only for interactive behavior such as locale switching, gallery lightbox behavior, and theme/time-based screenshot swapping.

## Goals

- Keep `scripts/build_localized_site.py` as the generator for localized pages.
- Render user-visible copy and SEO metadata directly into generated HTML.
- Remove the need for `window.siteData` as the source of page content.
- Keep the existing locale structure and metadata workflow intact.

## Non-Goals

- Replacing the metadata source format.
- Removing all JavaScript from the site.
- Redesigning page layouts or changing localized copy.

## Architecture

The generator remains the canonical renderer for all locale variants. Instead of emitting placeholder nodes that client-side JavaScript fills after load, it will emit fully rendered HTML for homepage, support, and privacy pages using values read from `metadata/`.

The runtime script becomes behavior-only. Locale switching will continue to derive available locales from the locale switcher markup already present in the page. Gallery and lightbox logic remain unchanged except for any dependency on the old `window.siteData` object. Asset paths needed by runtime behavior should come from the current page structure rather than a generated JS payload.

## Approach Options

### Option 1: Build-time rendered HTML with behavior-only JavaScript

Render localized strings directly into generated HTML and remove `site-data.js` from generated pages.

Pros:
- Removes unnecessary client-side content injection.
- Improves no-JS resilience for core page copy.
- Keeps one metadata source and one generator.

Cons:
- Requires updating generator templates and tests.

### Option 2: Hybrid HTML plus embedded JSON config

Render visible content into HTML but keep a tiny JSON/config blob for runtime.

Pros:
- Slightly simpler runtime migration.

Cons:
- Preserves a pattern the site no longer needs.
- Adds maintenance overhead without meaningful benefit.

### Option 3: Fully hand-authored localized HTML

Stop generating pages and maintain localized HTML directly.

Pros:
- Simplest runtime.

Cons:
- Duplicates markup across locales and pages.
- Makes localization maintenance much harder.

## Recommendation

Choose Option 1. It removes the unnecessary content layer while preserving the current source-of-truth model and minimizing migration risk.

## Implementation Outline

1. Update generator templates to emit final localized copy directly in HTML.
2. Remove `site-data.js` references from generated pages.
3. Simplify `script.js` to stop reading localized content from `window.siteData`.
4. Stop generating per-locale `site-data.js` files.
5. Update tests to assert HTML-rendered content and absence of `site-data.js`.

## Verification

- Rebuild the site and inspect generated pages in multiple locales.
- Run the existing site test suite.
- Confirm localized copy is present in HTML source.
- Confirm interactive JavaScript still works with the new DOM-only data sources.
