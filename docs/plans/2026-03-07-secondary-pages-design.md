# 40 Below Secondary Pages Design

## Summary

Rebuild `support.html` and `privacy-policy.html` so they feel like direct siblings of the homepage while preserving their existing text exactly. The pages should use the same top nav, typography, card surfaces, spacing, footer, and dark-mode behavior as `index.html`.

## Constraints

- Keep the existing support page copy unchanged.
- Keep the existing privacy policy copy unchanged.
- Reuse the homepage design language instead of the legacy `styles.css` system.
- Keep support and privacy links available in navigation/footer where appropriate.
- Preserve dark mode behavior consistent with the homepage.

## Structure

### Support

- Homepage-style top nav
- One primary hero/card introducing support
- One secondary card for the email action
- Homepage-style footer

### Privacy

- Homepage-style top nav
- One page header card for the title and updated date
- One main policy card for the full policy body
- One companion card for the nutrition/privacy summary
- Homepage-style footer

## Styling

- Use `styles/base.css` plus a dedicated shared secondary-page stylesheet
- Reuse the current token system and dark-mode palette
- Match the homepage card radii, panel treatment, and content width
