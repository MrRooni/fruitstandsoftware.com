import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parent.parent
LOCALES = sorted(
    path.name
    for path in (ROOT / "metadata").iterdir()
    if path.is_dir() and path.name != "review_information"
)
DEFAULT_LOCALE = "en-US"


class SiteVariantsTest(unittest.TestCase):
    def test_root_index_is_a_redirect_shell(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")

        self.assertIn('<html lang="en">', html)
        self.assertIn("Redirecting to the best language for your browser", html)
        self.assertIn('http-equiv="refresh"', html)
        self.assertIn('content="0; url=/en-US/"', html)
        self.assertIn("const DEFAULT_LOCALE = \"en-US\";", html)
        self.assertIn("window.localStorage.getItem", html)
        self.assertIn("navigator.languages", html)
        self.assertIn("window.location.replace", html)
        self.assertIn("resolveLocale", html)
        self.assertNotIn('src="site-data.js"', html)
        self.assertNotIn('data-site="product-name"', html)

    def test_all_locales_have_generated_pages(self):
        self.assertGreater(len(LOCALES), 1)

        for locale in LOCALES:
            locale_dir = ROOT / locale
            self.assertTrue(locale_dir.is_dir(), f"Missing locale directory: {locale}")

            homepage = (locale_dir / "index.html").read_text(encoding="utf-8")
            support = (locale_dir / "support.html").read_text(encoding="utf-8")
            privacy = (locale_dir / "privacy-policy.html").read_text(encoding="utf-8")
            site_data = (locale_dir / "site-data.js").read_text(encoding="utf-8")

            self.assertIn(f'<html lang="{locale}">', homepage)
            self.assertIn(f'rel="canonical" href="https://fruitstandsoftware.com/{locale}/"', homepage)
            self.assertIn("rel=\"alternate\" hreflang=\"x-default\" href=\"https://fruitstandsoftware.com/\"", homepage)
            self.assertIn('src="site-data.js"', homepage)
            self.assertIn('src="../script.js"', homepage)
            self.assertIn('class="locale-switcher"', homepage)
            self.assertIn("footer-locale-switcher", homepage)
            self.assertNotIn('class="nav-actions" aria-label="Primary">\n          <a class="nav-link" href="/' + locale + '/support.html">Support</a>\n          <label class="locale-switcher-wrap">', homepage)
            self.assertIn(f'href="/{locale}/support.html"', homepage)
            self.assertIn(f'href="/{locale}/privacy-policy.html"', homepage)
            self.assertIn(f"window.siteData = {{", site_data)
            self.assertIn(f'locale: "{locale}"', site_data)

            self.assertIn(f'<html lang="{locale}">', support)
            self.assertIn(f'<html lang="{locale}">', privacy)
            self.assertIn('class="locale-switcher"', support)
            self.assertIn('class="locale-switcher"', privacy)
            self.assertIn("footer-locale-switcher", support)
            self.assertIn("footer-locale-switcher", privacy)
            self.assertIn("Need help with 40 Below?", support)
            self.assertIn("Privacy Policy", privacy)

            for alternate_locale in LOCALES:
                homepage_link = (
                    f'rel="alternate" hreflang="{alternate_locale}" '
                    f'href="https://fruitstandsoftware.com/{alternate_locale}/"'
                )
                support_link = (
                    f'rel="alternate" hreflang="{alternate_locale}" '
                    f'href="https://fruitstandsoftware.com/{alternate_locale}/support.html"'
                )
                privacy_link = (
                    f'rel="alternate" hreflang="{alternate_locale}" '
                    f'href="https://fruitstandsoftware.com/{alternate_locale}/privacy-policy.html"'
                )
                self.assertIn(homepage_link, homepage)
                self.assertIn(support_link, support)
                self.assertIn(privacy_link, privacy)

    def test_english_and_non_english_locales_use_expected_copy(self):
        english_homepage = (ROOT / "en-US" / "index.html").read_text(encoding="utf-8")
        spanish_homepage = (ROOT / "es-ES" / "index.html").read_text(encoding="utf-8")
        british_site_data = (ROOT / "en-GB" / "site-data.js").read_text(encoding="utf-8")

        self.assertIn("Local Temperature in °F & °C", english_homepage)
        self.assertIn("Temperatura local en °F y °C", spanish_homepage)
        self.assertIn("Consulta la temperatura donde estás en Fahrenheit y Celsius", spanish_homepage)
        self.assertIn("colleagues", british_site_data)
        self.assertIn("centre", british_site_data)
        self.assertIn('option value="en-US" selected="selected">US</option>', english_homepage)
        self.assertIn('option value="en-GB">UK</option>', english_homepage)
        self.assertIn('option value="nl-NL">NL</option>', english_homepage)
        self.assertIn('option value="it">IT</option>', english_homepage)

    def test_script_contains_locale_switcher_and_matching_logic(self):
        script = (ROOT / "script.js").read_text(encoding="utf-8")
        styles = (ROOT / "styles" / "base.css").read_text(encoding="utf-8")

        self.assertIn("const DEFAULT_LOCALE = \"en-US\";", script)
        self.assertIn("const LOCALE_STORAGE_KEY = \"fruitstandsoftware.locale\";", script)
        self.assertIn("function normalizeLocale", script)
        self.assertIn("function resolveLocale", script)
        self.assertIn("navigator.languages", script)
        self.assertIn("window.localStorage.setItem", script)
        self.assertIn("function buildLocalePath", script)
        self.assertIn("function initLocaleSwitcher", script)
        self.assertIn('currentPath.endsWith("/support.html")', script)
        self.assertIn('currentPath.endsWith("/privacy-policy.html")', script)
        self.assertIn("sameLanguageLocale", script)
        self.assertIn("initLocaleSwitcher();", script)
        self.assertIn("initGalleryLightbox();", script)
        self.assertIn('"touchend"', script)
        self.assertIn("handledTouch", script)
        self.assertIn("touch-action: manipulation;", styles)

    def test_generator_and_docs_exist(self):
        generator = ROOT / "scripts" / "build_localized_site.py"
        self.assertTrue(generator.exists(), "Missing localization generator")

        generator_source = generator.read_text(encoding="utf-8")
        self.assertIn("metadata", generator_source)
        self.assertIn("description.txt", generator_source)
        self.assertIn("release_notes.txt", generator_source)
        self.assertIn("support.html", generator_source)
        self.assertIn("privacy-policy.html", generator_source)

        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("python3 scripts/build_localized_site.py", readme)
        self.assertIn("/en-US/", readme)

    def test_base_css_has_cjk_font_fallbacks(self):
        css = (ROOT / "styles" / "base.css").read_text(encoding="utf-8")

        self.assertIn('html:lang(ja)', css)
        self.assertIn('html:lang(ko)', css)
        self.assertIn('"Hiragino Sans"', css)
        self.assertIn('"Yu Gothic"', css)
        self.assertIn('"Apple SD Gothic Neo"', css)


if __name__ == "__main__":
    unittest.main()
