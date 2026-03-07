import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parent.parent


class SiteVariantsTest(unittest.TestCase):
    def test_index_page_matches_current_contract(self):
        removed_strings = (
            "Compare all 5 variants",
            "Canonical product copy is derived from the English metadata in this repository.",
            "Five complete directions built on the same product story",
            "A cleaner, sharper direction built like a product card",
            "A structured weather-board approach with bigger data language",
            "A dark-first presentation centered on glow and atmosphere",
            "A more independent, personality-forward composition",
            "Why it exists",
            "Feature set",
            "Location and privacy",
            "Launch note",
            "Variant Picker",
        )
        page_path = ROOT / "index.html"
        self.assertTrue(page_path.exists(), "Missing homepage index.html")

        for removed_page in ("variant-2.html", "variant-3.html", "variant-4.html", "variant-5.html"):
            self.assertFalse((ROOT / removed_page).exists(), f"Unexpected leftover page: {removed_page}")

        html = page_path.read_text(encoding="utf-8")

        self.assertIn('<main id="main"', html)
        self.assertNotIn("Skip to content", html)
        self.assertIn('src="site-data.js"', html)
        self.assertIn('src="script.js"', html)
        self.assertNotIn('gallery.html', html)
        self.assertIn('src="Warm_Midday_Light.png"', html)
        self.assertIn('id="hero-screenshot-dark-source"', html)
        self.assertIn('width="500"', html)
        self.assertIn('height="1036"', html)
        self.assertIn('class="hero-title-lockup"', html)
        self.assertIn('class="hero-heading-group"', html)
        self.assertIn('Download-on-the-App-Store/US/', html)
        self.assertIn("White_lockup", html)
        self.assertIn("prefers-color-scheme: dark", html)
        self.assertIn('href="support.html"', html)
        self.assertIn('class="nav-actions"', html)
        self.assertIn('class="nav-store-link"', html)
        self.assertIn('class="nav-brand-icon" src="favicon.png"', html)
        self.assertIn('href="privacy-policy.html"', html)
        self.assertIn('rel="icon" type="image/png" sizes="512x512" href="favicon.png"', html)
        self.assertIn('data-site="release-notes-rich"', html)
        self.assertIn('data-site="description-paragraphs"', html)
        self.assertIn('data-site="feature-list"', html)
        self.assertIn("gallery-block", html)
        self.assertIn('data-lightbox', html)
        self.assertIn("Cold_Morning_Dark_Forecast.png", html)
        self.assertIn("Cold_Night_Dark.png", html)
        self.assertIn("Hot_Afternoon_Light.png", html)
        self.assertIn("Cold_Morning_Dark.png", html)
        self.assertIn("Warm_Midday_Light.png", html)
        self.assertIn("Warm_Night_Dark.png", html)
        self.assertNotIn("variant-switcher", html)
        self.assertNotIn('class="app-store-link"', html)

        for text in removed_strings:
            self.assertNotIn(text, html)

        css = (ROOT / "styles" / "base.css").read_text(encoding="utf-8")
        self.assertIn('"SF Pro Display"', css)
        self.assertIn('"SF Pro Text"', css)
        self.assertIn("@media (prefers-color-scheme: dark)", css)
        self.assertIn("gap: 2rem", css)
        self.assertNotIn(".screen-frame {\n    background: linear-gradient", css)
        self.assertIn(".nav-brand-icon", css)
        self.assertIn(".gallery-grid", css)
        self.assertIn(".lightbox", css)
        self.assertIn("aspect-ratio: 1000 / 2072;", css)
        self.assertIn("object-fit: contain;", css)
        self.assertIn(".gallery-thumb {\n  appearance: none;\n  padding: 0;\n  border: 0;", css)

        variant_css = (ROOT / "styles" / "variant-1.css").read_text(encoding="utf-8")
        self.assertIn("@media (prefers-color-scheme: dark)", variant_css)
        self.assertIn(".page-1 .nav-shell", variant_css)
        self.assertIn("padding-inline: clamp(1.25rem, 3vw, 2rem)", variant_css)

        script = (ROOT / "script.js").read_text(encoding="utf-8")
        self.assertIn("https://apps.apple.com/app/id6759849820?action=write-review", script)
        self.assertIn("a nice 5-star review would sure be great.", script)
        self.assertNotIn('node.setAttribute("src", site.product.screenshot.src);', script)
        self.assertIn('currentHour < NOON_HOUR ? "Cold_Morning_Dark.png" : "Warm_Night_Dark.png"', script)
        self.assertIn('window.matchMedia("(prefers-color-scheme: dark)")', script)
        self.assertIn("const SWIPE_THRESHOLD = 48;", script)
        self.assertIn('"touchmove"', script)
        self.assertIn("--lightbox-drag-x", script)
        self.assertIn('event.key === "ArrowRight"', script)
        self.assertIn('event.key === "ArrowLeft"', script)
        self.assertIn("initGalleryLightbox();", script)

    def test_secondary_pages_match_homepage_shell(self):
        for page_name in ("support.html", "privacy-policy.html"):
            html = (ROOT / page_name).read_text(encoding="utf-8")

            self.assertIn('href="styles/base.css"', html)
            self.assertIn('href="styles/secondary-pages.css"', html)
            self.assertIn('class="top-nav"', html)
            self.assertIn('class="nav-actions"', html)
            self.assertIn('class="nav-store-link"', html)
            self.assertIn('class="nav-brand-icon" src="favicon.png"', html)
            self.assertIn('rel="icon" type="image/png" sizes="512x512" href="favicon.png"', html)
            self.assertIn("site-footer", html)
            self.assertNotIn("fonts.googleapis.com", html)
            self.assertNotIn('href="styles.css"', html)

        support_html = (ROOT / "support.html").read_text(encoding="utf-8")
        self.assertIn('class="support-grid"', support_html)
        self.assertIn("support-card", support_html)

        privacy_html = (ROOT / "privacy-policy.html").read_text(encoding="utf-8")
        self.assertIn('class="policy-page-grid"', privacy_html)
        self.assertIn("policy-main-card", privacy_html)
        self.assertIn("policy-aside-card", privacy_html)

if __name__ == "__main__":
    unittest.main()
