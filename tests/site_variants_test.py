import json
import pathlib
import unittest
import xml.etree.ElementTree as ET


ROOT = pathlib.Path(__file__).resolve().parent.parent
LOCALES = sorted(
    path.name
    for path in (ROOT / "metadata").iterdir()
    if path.is_dir() and path.name != "review_information"
)
DEFAULT_LOCALE = "en-US"
SECONDARY_TRANSLATIONS = json.loads(
    (ROOT / "secondary-page-translations.json").read_text(encoding="utf-8")
)
PROMO_TRANSLATIONS = json.loads(
    (ROOT / "promo-page-translations.json").read_text(encoding="utf-8")
)
NUMBER_ONE_TRANSLATIONS = json.loads(
    (ROOT / "number-one-page-translations.json").read_text(encoding="utf-8")
)
PRESS_PAGE_DATA = json.loads((ROOT / "press-page-data.json").read_text(encoding="utf-8"))


class SiteVariantsTest(unittest.TestCase):
    def test_root_index_is_a_redirect_shell(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")

        self.assertIn('<html lang="en">', html)
        self.assertIn('name="description"', html)
        self.assertIn(
            'content="See the temperature where you are in Fahrenheit and Celsius, check the hourly forecast, and share a clean temperature card in seconds."',
            html,
        )
        self.assertIn('<meta property="og:title" content="40 Below" />', html)
        self.assertIn('property="og:description"', html)
        self.assertIn('<meta property="og:type" content="website" />', html)
        self.assertIn('<meta property="og:url" content="https://fruitstandsoftware.com/" />', html)
        self.assertIn(
            '<meta property="og:image" content="https://fruitstandsoftware.com/SocialImage.png" />',
            html,
        )
        self.assertIn('<meta name="twitter:card" content="summary_large_image" />', html)
        self.assertIn(
            '<meta name="twitter:image" content="https://fruitstandsoftware.com/SocialImage.png" />',
            html,
        )
        self.assertIn('<link rel="canonical" href="https://fruitstandsoftware.com/" />', html)
        self.assertIn("Redirecting to the best language for your browser", html)
        self.assertIn('http-equiv="refresh"', html)
        self.assertIn('content="0; url=/en-US/"', html)
        self.assertIn("const DEFAULT_LOCALE = \"en-US\";", html)
        self.assertIn("window.localStorage.getItem", html)
        self.assertIn("navigator.languages", html)
        self.assertIn("window.location.replace", html)
        self.assertIn("resolveLocale", html)
        self.assertIn('id="fallback-locales-heading"', html)
        self.assertIn('href="/en-US/"', html)
        self.assertIn('href="/en-GB/"', html)
        self.assertIn('href="/es-ES/"', html)
        self.assertIn('href="/ja/"', html)
        self.assertIn('href="/zh-Hans/"', html)
        self.assertNotIn('src="site-data.js"', html)
        self.assertNotIn('data-site="product-name"', html)

    def test_robots_txt_and_sitemap_exist_with_expected_indexable_urls(self):
        robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
        sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")

        self.assertIn("User-agent: *", robots)
        self.assertIn("Allow: /", robots)
        self.assertIn("Sitemap: https://fruitstandsoftware.com/sitemap.xml", robots)

        root = ET.fromstring(sitemap)
        namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        urls = [node.text for node in root.findall("sm:url/sm:loc", namespace)]

        self.assertIn("https://fruitstandsoftware.com/", urls)
        self.assertIn("https://fruitstandsoftware.com/number-one.html", urls)
        self.assertIn("https://fruitstandsoftware.com/en-US/press.html", urls)
        self.assertNotIn("https://fruitstandsoftware.com/redeem.html", urls)

        for locale in LOCALES:
            self.assertIn(f"https://fruitstandsoftware.com/{locale}/", urls)
            self.assertIn(f"https://fruitstandsoftware.com/{locale}/support.html", urls)
            self.assertIn(f"https://fruitstandsoftware.com/{locale}/privacy-policy.html", urls)

    def test_root_redeem_page_exists_with_expected_promo_shell(self):
        html = (ROOT / "redeem.html").read_text(encoding="utf-8")
        promo = PROMO_TRANSLATIONS["en-US"]

        self.assertIn('<html lang="en-US" dir="ltr">', html)
        self.assertIn('<meta name="robots" content="noindex, nofollow" />', html)
        self.assertIn('<link rel="canonical" href="https://fruitstandsoftware.com/redeem.html" />', html)
        self.assertIn('<meta property="og:image" content="https://fruitstandsoftware.com/40BelowIcons/40BelowLight.png" />', html)
        self.assertIn('<meta name="twitter:image" content="https://fruitstandsoftware.com/40BelowIcons/40BelowLight.png" />', html)
        self.assertIn(promo["intro"], html)
        self.assertIn(promo["title"], html)
        self.assertIn('src="40BelowIcons/40BelowLight.png"', html)
        self.assertIn('srcset="40BelowIcons/40BelowDark.png"', html)
        self.assertIn('data-promo-button', html)
        self.assertIn('data-promo-intro', html)
        self.assertIn('data-promo-title', html)
        self.assertIn('data-promo-status', html)
        self.assertIn('"validPattern": "^[A-Z0-9]{12}$"', html)
        self.assertIn(f'"introTemplate": "{promo["intro"]}"', html)
        self.assertIn(promo["missing_message"], html)
        self.assertIn(promo["malformed_message"], html)
        self.assertIn(promo["fallback_cta"], html)
        self.assertIn('src="script.js"', html)

    def test_root_number_one_page_exists_with_expected_marketing_shell(self):
        html = (ROOT / "number-one.html").read_text(encoding="utf-8")
        page = NUMBER_ONE_TRANSLATIONS["en-US"]

        self.assertIn('<html lang="en-US" dir="ltr">', html)
        self.assertIn('<link rel="canonical" href="https://fruitstandsoftware.com/number-one.html" />', html)
        self.assertIn('<meta property="og:url" content="https://fruitstandsoftware.com/number-one.html" />', html)
        self.assertIn('<meta property="og:image" content="https://fruitstandsoftware.com/40BelowIcons/40BelowLight.png" />', html)
        self.assertIn('<meta name="twitter:image" content="https://fruitstandsoftware.com/40BelowIcons/40BelowLight.png" />', html)
        self.assertIn('<meta name="robots" content="index, follow" />', html)
        self.assertNotIn('noindex, nofollow', html)
        self.assertIn(page["title"], html)
        self.assertIn(page["footnote"], html)
        self.assertIn(page["cta"], html)
        self.assertIn('src="40BelowIcons/40BelowLight.png"', html)
        self.assertIn('srcset="40BelowIcons/40BelowDark.png"', html)
        self.assertIn('Download-on-the-App-Store/US/', html)
        self.assertIn('class="promo-store-link"', html)
        self.assertIn(page["badge_alt"], html)
        self.assertNotIn("window.siteData", html)
        self.assertNotIn('src="script.js"', html)

    def test_all_locales_have_generated_pages(self):
        self.assertGreater(len(LOCALES), 1)
        self.assertEqual(sorted(SECONDARY_TRANSLATIONS), LOCALES)
        press_link = 'href="/en-US/press.html"'

        for locale in LOCALES:
            locale_dir = ROOT / locale
            self.assertTrue(locale_dir.is_dir(), f"Missing locale directory: {locale}")

            homepage = (locale_dir / "index.html").read_text(encoding="utf-8")
            support = (locale_dir / "support.html").read_text(encoding="utf-8")
            privacy = (locale_dir / "privacy-policy.html").read_text(encoding="utf-8")
            translation = SECONDARY_TRANSLATIONS[locale]
            direction = "rtl" if locale.split("-")[0] in {"ar", "fa", "he", "ur"} else "ltr"

            self.assertIn(f'<html lang="{locale}" dir="{direction}">', homepage)
            self.assertIn(f'rel="canonical" href="https://fruitstandsoftware.com/{locale}/"', homepage)
            self.assertIn("rel=\"alternate\" hreflang=\"x-default\" href=\"https://fruitstandsoftware.com/\"", homepage)
            self.assertIn('<script type="application/ld+json">', homepage)
            self.assertIn('"@type": "SoftwareApplication"', homepage)
            self.assertIn(f'"url": "https://fruitstandsoftware.com/{locale}/"', homepage)
            self.assertNotIn('src="site-data.js"', homepage)
            self.assertIn('src="../script.js"', homepage)
            self.assertIn('class="locale-switcher"', homepage)
            self.assertIn("footer-locale-switcher", homepage)
            self.assertNotIn('class="nav-actions" aria-label="Primary">\n          <a class="nav-link" href="/' + locale + '/support.html">Support</a>\n          <label class="locale-switcher-wrap">', homepage)
            self.assertIn(f'href="/{locale}/support.html"', homepage)
            self.assertIn(f'href="/{locale}/privacy-policy.html"', homepage)
            self.assertNotIn('data-site="', homepage)
            self.assertNotIn("window.siteData", homepage)
            self.assertIn(press_link, homepage)
            self.assertIn(f'>{translation["shell"]["nav_support"]}</a>', homepage)
            self.assertIn(f'>{translation["shell"]["footer_privacy"]}</a>', homepage)

            self.assertIn(f'<html lang="{locale}" dir="{direction}">', support)
            self.assertIn(f'<html lang="{locale}" dir="{direction}">', privacy)
            self.assertIn('class="locale-switcher"', support)
            self.assertIn('class="locale-switcher"', privacy)
            self.assertIn("footer-locale-switcher", support)
            self.assertIn("footer-locale-switcher", privacy)
            self.assertIn("secondary-page-title", support)
            self.assertIn("policy-page-grid", privacy)
            self.assertIn(translation["support"]["title"], support)
            self.assertIn(translation["privacy"]["title"], privacy)
            self.assertIn(press_link, support)
            self.assertIn(press_link, privacy)
            self.assertIn(translation["shell"]["nav_support"], support)
            self.assertIn(translation["shell"]["footer_privacy"], privacy)

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

    def test_press_page_exists_with_expected_content_and_downloads(self):
        html = (ROOT / "en-US" / "press.html").read_text(encoding="utf-8")
        press = PRESS_PAGE_DATA["en-US"]
        assets = PRESS_PAGE_DATA["assets"]

        self.assertIn('<html lang="en-US" dir="ltr">', html)
        self.assertIn('<link rel="canonical" href="https://fruitstandsoftware.com/en-US/press.html" />', html)
        self.assertIn('href="/en-US/press.html" aria-current="page"', html)
        self.assertIn(press["title"], html)
        self.assertIn(press["download_button"], html)
        self.assertIn(press["technology_heading"], html)
        self.assertIn("press-hero-media", html)
        self.assertNotIn("Built for Apple platforms", html)
        self.assertIn("Uses Apple’s own WeatherKit framework", html)
        self.assertIn("connected to CarPlay", html)
        self.assertNotIn("press-tech-card", html)
        self.assertNotIn('id="press-gallery-heading"', html)
        self.assertIn("mailto:michael@fruitstandsoftware.com", html)
        self.assertIn("window.galleryGroups", html)
        self.assertIn('data-gallery-group="press-iphone"', html)
        self.assertIn('data-gallery-group="press-ipad"', html)
        self.assertIn('data-gallery-group="press-mac"', html)
        self.assertIn("40-Below-Press-Assets/Product Shots/iPad/", html)
        self.assertIn("40-Below-Press-Assets/Product Shots/Mac/", html)
        self.assertIn(assets["downloads"]["press_kit"]["href"], html)
        self.assertLess(html.index('id="press-mac-heading"'), html.index('id="press-contact-heading"'))

        self.assertTrue((ROOT / "40-Below-Press-Assets.zip").is_file())

    def test_english_and_non_english_locales_use_expected_copy(self):
        english_homepage = (ROOT / "en-US" / "index.html").read_text(encoding="utf-8")
        spanish_homepage = (ROOT / "es-ES" / "index.html").read_text(encoding="utf-8")
        british_homepage = (ROOT / "en-GB" / "index.html").read_text(encoding="utf-8")
        japanese_support = (ROOT / "ja" / "support.html").read_text(encoding="utf-8")
        korean_privacy = (ROOT / "ko" / "privacy-policy.html").read_text(encoding="utf-8")
        arabic_privacy = (ROOT / "ar-SA" / "privacy-policy.html").read_text(encoding="utf-8")
        spanish_support = (ROOT / "es-ES" / "support.html").read_text(encoding="utf-8")
        simplified_chinese_homepage = (ROOT / "zh-Hans" / "index.html").read_text(encoding="utf-8")

        self.assertIn("Local Temperature in °F & °C", english_homepage)
        self.assertIn("Temperatura local en °F y °C", spanish_homepage)
        self.assertIn("Consulta la temperatura donde estás en Fahrenheit y Celsius", spanish_homepage)
        self.assertIn("colleagues", british_homepage)
        self.assertIn("centre", british_homepage)
        self.assertIn('option value="en-US" selected="selected">US</option>', english_homepage)
        self.assertIn('option value="en-GB">UK</option>', english_homepage)
        self.assertIn('option value="nl-NL">NL</option>', english_homepage)
        self.assertIn('option value="it">IT</option>', english_homepage)
        self.assertIn("40 Belowのサポートが必要ですか？", japanese_support)
        self.assertIn("サポートにメールする", japanese_support)
        self.assertIn("개인정보 처리방침", korean_privacy)
        self.assertIn("위치 정보", korean_privacy)
        self.assertIn("سياسة الخصوصية", arabic_privacy)
        self.assertIn("الموقع", arabic_privacy)
        self.assertIn("¿Necesitas ayuda con 40 Below?", spanish_support)
        self.assertIn("Enviar un correo a soporte", spanish_support)
        self.assertIn("Elegir idioma", spanish_homepage)
        self.assertIn("/Download-on-the-App-Store/ES/", spanish_homepage)
        self.assertIn("言語を選択", (ROOT / "ja" / "index.html").read_text(encoding="utf-8"))
        self.assertIn("/Download-on-the-App-Store/JP/", (ROOT / "ja" / "index.html").read_text(encoding="utf-8"))
        self.assertIn("选择语言", simplified_chinese_homepage)
        self.assertNotIn("Need help with 40 Below?", japanese_support)
        self.assertNotIn("Privacy Policy", korean_privacy)

    def test_localized_homepage_content_is_present_in_html(self):
        english_homepage = (ROOT / "en-US" / "index.html").read_text(encoding="utf-8")
        japanese_homepage = (ROOT / "ja" / "index.html").read_text(encoding="utf-8")

        self.assertIn("<h1>40 Below</h1>", english_homepage)
        self.assertIn("Additional, thoughtful features:", english_homepage)
        self.assertIn("What&#x27;s New in Version 1.0", english_homepage)
        self.assertIn("Improved the formatting and clarity of the App Store release notes.", english_homepage)
        self.assertIn("現在地の気温を華氏と摂氏で確認", japanese_homepage)
        self.assertNotIn('data-site="product-name"', english_homepage)
        self.assertNotIn('data-site="release-notes-rich"', english_homepage)

    def test_localized_privacy_pages_follow_root_policy_structure(self):
        english_privacy = (ROOT / "en-US" / "privacy-policy.html").read_text(encoding="utf-8")

        self.assertIn('<section class="policy-block">', english_privacy)
        self.assertIn("Your privacy matters to us.", english_privacy)
        self.assertIn("40 Below uses your location on your device to show weather conditions where you are.", english_privacy)
        self.assertIn("Last viewed location information if available (coordinates and place names)", english_privacy)
        self.assertIn("If this changes, this policy will be updated.", english_privacy)
        self.assertIn(
            "The &quot;Last updated&quot; date at the top will always reflect the latest version.",
            english_privacy,
        )
        self.assertIn("Data collected: Location (used only to provide weather)", english_privacy)
        self.assertIn('aria-label="Privacy Nutrition Label"', english_privacy)
        self.assertIn("Per app usage", english_privacy)
        self.assertIn("See policy text for complete details.", english_privacy)

        for locale in LOCALES:
            privacy = (ROOT / locale / "privacy-policy.html").read_text(encoding="utf-8")
            self.assertEqual(
                privacy.count('<section class="policy-block">'),
                11,
                f"Expected intro plus 10 policy sections for {locale}",
            )

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
        self.assertIn("function initPromoRedeemPage", script)
        self.assertIn("window.promoPageConfig", script)
        self.assertIn('params.get("promo")', script)
        self.assertIn('params.get("name")', script)
        self.assertIn("new RegExp(config.validPattern)", script)
        self.assertIn('name || "Congratulations"', script)
        self.assertIn('config.introTemplate.replace("Congratulations", introLead)', script)
        self.assertIn("intro.hidden = true", script)
        self.assertIn("intro.hidden = false", script)
        self.assertIn("title.hidden = true", script)
        self.assertIn("title.hidden = false", script)
        self.assertIn("config.redeemBaseUrl", script)
        self.assertIn("initPromoRedeemPage();", script)
        self.assertIn('"touchend"', script)
        self.assertIn("handledTouch", script)
        self.assertNotIn("window.siteData", script)
        self.assertIn("touch-action: manipulation;", styles)

    def test_generator_and_docs_exist(self):
        generator = ROOT / "scripts" / "build_localized_site.py"
        self.assertTrue(generator.exists(), "Missing localization generator")
        translations = ROOT / "secondary-page-translations.json"
        self.assertTrue(translations.exists(), "Missing secondary page translation source")
        promo_translations = ROOT / "promo-page-translations.json"
        self.assertTrue(promo_translations.exists(), "Missing promo page translation source")
        number_one_translations = ROOT / "number-one-page-translations.json"
        self.assertTrue(number_one_translations.exists(), "Missing number one page translation source")

        generator_source = generator.read_text(encoding="utf-8")
        self.assertIn("metadata", generator_source)
        self.assertIn("description.txt", generator_source)
        self.assertIn("release_notes.txt", generator_source)
        self.assertIn("support.html", generator_source)
        self.assertIn("privacy-policy.html", generator_source)
        self.assertIn("secondary-page-translations.json", generator_source)
        self.assertIn("promo-page-translations.json", generator_source)
        self.assertIn("number-one-page-translations.json", generator_source)
        self.assertIn("number-one.html", generator_source)
        self.assertIn("redeem.html", generator_source)

        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("python3 scripts/build_localized_site.py", readme)
        self.assertIn("/en-US/", readme)

    def test_base_css_has_script_specific_font_fallbacks(self):
        css = (ROOT / "styles" / "base.css").read_text(encoding="utf-8")

        self.assertIn('html:lang(ja)', css)
        self.assertIn('html:lang(ko)', css)
        self.assertIn('html:lang(ar-SA)', css)
        self.assertIn('html:lang(hi)', css)
        self.assertIn('"Hiragino Sans"', css)
        self.assertIn('"Yu Gothic"', css)
        self.assertIn('"Apple SD Gothic Neo"', css)
        self.assertIn('"Geeza Pro"', css)
        self.assertIn('"Noto Naskh Arabic"', css)
        self.assertIn('"Devanagari Sangam MN"', css)
        self.assertIn('"Noto Sans Devanagari"', css)


if __name__ == "__main__":
    unittest.main()
