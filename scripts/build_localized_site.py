from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
METADATA_DIR = ROOT / "metadata"
DEFAULT_LOCALE = "en-US"
SITE_URL = "https://fruitstandsoftware.com"
COPYRIGHT = "2026 © Fruit Stand Software, LLC"
APP_STORE_URL = "https://apps.apple.com/app/id6758684366"

LOCALES = sorted(
    path.name
    for path in METADATA_DIR.iterdir()
    if path.is_dir() and path.name != "review_information"
)


def read_metadata(locale: str, name: str) -> str:
    return (METADATA_DIR / locale / name).read_text(encoding="utf-8").strip()


def parse_description(locale: str) -> dict[str, object]:
    raw_description = read_metadata(locale, "description.txt")
    blocks = [block.strip() for block in re.split(r"\n\s*\n", raw_description) if block.strip()]
    description_paragraphs = blocks[:2]

    feature_lines = blocks[2].splitlines()
    feature_heading = feature_lines[0].strip()
    features = [line.removeprefix("- ").strip() for line in feature_lines[1:] if line.strip()]
    location_text = blocks[3]

    return {
        "description_paragraphs": description_paragraphs,
        "feature_heading": feature_heading,
        "features": features,
        "location_text": location_text,
    }


def locale_path(locale: str, page_kind: str) -> str:
    if page_kind == "home":
        return f"/{locale}/"
    if page_kind == "support":
        return f"/{locale}/support.html"
    if page_kind == "privacy":
        return f"/{locale}/privacy-policy.html"
    raise ValueError(f"Unsupported page kind: {page_kind}")


def canonical_url(locale: str, page_kind: str) -> str:
    return f"{SITE_URL}{locale_path(locale, page_kind)}"


def render_hreflang_links(page_kind: str) -> str:
    links = [
        f'    <link rel="alternate" hreflang="{locale}" href="{canonical_url(locale, page_kind)}" />'
        for locale in LOCALES
    ]
    links.append(f'    <link rel="alternate" hreflang="x-default" href="{SITE_URL}/" />')
    return "\n".join(links)


def locale_switcher_label(locale: str) -> str:
    overrides = {
        "en-GB": "UK",
        "zh-Hans": "CN",
        "zh-Hant": "TW",
    }
    if locale in overrides:
        return overrides[locale]

    if "-" in locale:
        return locale.split("-")[1].upper()

    return locale[:2].upper()


def render_locale_switcher(locale: str, indent: str = "          ", wrapper_class: str = "") -> str:
    options = []
    for candidate in LOCALES:
        selected = ' selected="selected"' if candidate == locale else ""
        label = locale_switcher_label(candidate)
        options.append(f'{indent}      <option value="{candidate}"{selected}>{label}</option>')

    classes = "locale-switcher-wrap"
    if wrapper_class:
        classes = f"{classes} {wrapper_class}"

    return "\n".join(
        [
            f'{indent}<label class="{classes}">',
            f'{indent}  <span class="visually-hidden">Choose language</span>',
            f'{indent}  <select class="locale-switcher" aria-label="Choose language">',
            *options,
            f"{indent}  </select>",
            f"{indent}</label>",
        ]
    )


def javascript_value(value: object) -> str:
    return json.dumps(value, ensure_ascii=False)


def render_site_data(locale: str) -> str:
    description = parse_description(locale)
    product_name = read_metadata(locale, "name.txt")
    subtitle = read_metadata(locale, "subtitle.txt")
    promotional_text = read_metadata(locale, "promotional_text.txt")
    keywords = read_metadata(locale, "keywords.txt")
    release_notes = read_metadata(locale, "release_notes.txt")

    return "\n".join(
        [
            "window.siteData = {",
            f"  locale: {javascript_value(locale)},",
            f"  availableLocales: {javascript_value(LOCALES)},",
            '  assetBasePath: "../",',
            "  seo: {",
            f"    title: {javascript_value(f'{product_name} | {subtitle}')},",
            f"    description: {javascript_value(promotional_text)},",
            f"    ogTitle: {javascript_value(product_name)},",
            f"    ogDescription: {javascript_value(promotional_text)},",
            f"    keywords: {javascript_value(keywords)},",
            "  },",
            "  product: {",
            f"    name: {javascript_value(product_name)},",
            f"    subtitle: {javascript_value(subtitle)},",
            f"    promotionalText: {javascript_value(promotional_text)},",
            f"    descriptionParagraphs: {javascript_value(description['description_paragraphs'])},",
            f"    featureHeading: {javascript_value(description['feature_heading'])},",
            f"    features: {javascript_value(description['features'])},",
            f"    locationText: {javascript_value(description['location_text'])},",
            f"    releaseNotes: {javascript_value(release_notes)},",
            "    screenshot: {",
            f"      alt: {javascript_value(f'{product_name} — {subtitle}')},",
            "    },",
            "  },",
            "  footer: {",
            f"    copyright: {javascript_value(COPYRIGHT)},",
            "  },",
            "};",
        ]
    )


def render_homepage(locale: str) -> str:
    title = read_metadata(locale, "name.txt")
    subtitle = read_metadata(locale, "subtitle.txt")
    promotional_text = read_metadata(locale, "promotional_text.txt")
    hreflang_links = render_hreflang_links("home")
    footer_locale_switcher = render_locale_switcher(
        locale, indent="        ", wrapper_class="footer-locale-switcher"
    )

    return f"""<!doctype html>
<html lang="{locale}">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{title} | {subtitle}</title>
    <meta
      name="description"
      content="{promotional_text}"
    />
    <meta
      name="keywords"
      content="{read_metadata(locale, "keywords.txt")}"
    />
    <meta property="og:title" content="{title}" />
    <meta
      property="og:description"
      content="{promotional_text}"
    />
    <meta property="og:type" content="website" />
    <link rel="canonical" href="{canonical_url(locale, "home")}" />
{hreflang_links}
    <link rel="icon" type="image/png" sizes="512x512" href="../favicon.png" />
    <link rel="stylesheet" href="../styles/base.css" />
    <link rel="stylesheet" href="../styles/variant-1.css" />
  </head>
  <body class="page page-1">
    <header class="top-nav">
      <div class="nav-shell">
        <a class="nav-brand" href="/{locale}/" aria-label="40 Below home">
          <img class="nav-brand-icon" src="../favicon.png" alt="" width="32" height="32" />
          <span>40 Below</span>
        </a>
        <nav class="nav-actions" aria-label="Primary">
          <a class="nav-link" href="/{locale}/support.html">Support</a>
          <a
            class="nav-store-link"
            href="{APP_STORE_URL}"
            target="_blank"
            rel="noopener noreferrer"
            aria-label="Download 40 Below on the App Store"
          >
            <img
              class="badge-light"
              src="../Download-on-the-App-Store/US/Download_on_App_Store/Black_lockup/SVG/Download_on_the_App_Store_Badge_US-UK_RGB_blk_092917.svg"
              alt="Download on the App Store"
              width="152"
              height="52"
            />
            <img
              class="badge-dark"
              src="../Download-on-the-App-Store/US/Download_on_App_Store/White_lockup/SVG/Download_on_the_App_Store_Badge_US-UK_RGB_wht_092917.svg"
              alt="Download on the App Store"
              width="152"
              height="52"
            />
          </a>
        </nav>
      </div>
    </header>

    <main id="main" class="page-shell">
      <section class="hero hero-editorial reveal">
        <div class="hero-copy">
          <div class="hero-title-lockup">
            <picture class="hero-icon">
              <source
                srcset="../40BelowRetro Exports/40BelowRetro-iOS-Dark-68x68@2x.png"
                media="(prefers-color-scheme: dark)"
              />
              <img
                src="../40BelowRetro Exports/40BelowRetro-iOS-Default-68x68@2x.png"
                alt="40 Below app icon"
                width="144"
                height="144"
              />
            </picture>
            <div class="hero-heading-group">
              <h1 data-site="product-name"></h1>
              <p class="hero-subtitle" data-site="product-subtitle"></p>
            </div>
          </div>
          <p class="hero-promo" data-site="product-promo"></p>
          <div class="hero-description prose-block">
            <div data-site="description-paragraphs"></div>
            <p class="feature-heading" data-site="feature-heading"></p>
            <ul class="feature-list" data-site="feature-list"></ul>
            <p data-site="location-text"></p>
          </div>
        </div>
        <figure class="screen-frame">
          <picture>
            <source
              id="hero-screenshot-dark-source"
              srcset="../Cold_Morning_Dark.png"
              media="(prefers-color-scheme: dark)"
            />
            <img
              data-site="screenshot"
              src="../Warm_Midday_Light.png"
              alt="40 Below app screen"
              width="500"
              height="1036"
            />
          </picture>
        </figure>
      </section>

      <section class="content-block release-block reveal">
        <p class="release-copy" data-site="release-notes-rich"></p>
      </section>

      <section class="content-block gallery-block reveal" aria-labelledby="gallery-heading">
        <div class="gallery-head">
          <h2 id="gallery-heading">Gallery</h2>
        </div>
        <div class="gallery-grid">
          <button class="gallery-thumb" type="button" data-gallery-index="0" aria-label="Open Cold Morning Dark screenshot">
            <img src="../Cold_Morning_Dark.png" alt="Cold Morning Dark screenshot" width="250" height="518" loading="lazy" />
          </button>
          <button class="gallery-thumb" type="button" data-gallery-index="1" aria-label="Open Cold Morning Dark Forecast screenshot">
            <img src="../Cold_Morning_Dark_Forecast.png" alt="Cold Morning Dark Forecast screenshot" width="250" height="518" loading="lazy" />
          </button>
          <button class="gallery-thumb" type="button" data-gallery-index="2" aria-label="Open Warm Midday Light screenshot">
            <img src="../Warm_Midday_Light.png" alt="Open Warm Midday Light screenshot" width="250" height="518" loading="lazy" />
          </button>
          <button class="gallery-thumb" type="button" data-gallery-index="3" aria-label="Open Hot Afternoon Light screenshot">
            <img src="../Hot_Afternoon_Light.png" alt="Hot Afternoon Light screenshot" width="250" height="518" loading="lazy" />
          </button>
          <button class="gallery-thumb" type="button" data-gallery-index="4" aria-label="Open Cold Night Dark screenshot">
            <img src="../Cold_Night_Dark.png" alt="Cold Night Dark screenshot" width="250" height="518" loading="lazy" />
          </button>
          <button class="gallery-thumb" type="button" data-gallery-index="5" aria-label="Open Warm Night Dark screenshot">
            <img src="../Warm_Night_Dark.png" alt="Warm Night Dark screenshot" width="250" height="518" loading="lazy" />
          </button>
        </div>
      </section>
    </main>

    <div
      class="lightbox"
      data-lightbox
      role="dialog"
      aria-modal="true"
      aria-labelledby="lightbox-title"
      hidden
    >
      <div class="lightbox-backdrop" data-lightbox-close></div>
      <div class="lightbox-shell">
        <div class="lightbox-bar">
          <p id="lightbox-title" class="lightbox-status" aria-live="polite"></p>
          <button class="lightbox-close" type="button" data-lightbox-close aria-label="Close gallery">
            Close
          </button>
        </div>
        <div class="lightbox-stage" data-lightbox-stage>
          <button class="lightbox-arrow" type="button" data-gallery-prev aria-label="Previous image">
            &#8592;
          </button>
          <div class="lightbox-viewport" data-lightbox-viewport>
            <div class="lightbox-track" data-lightbox-track>
              <div class="lightbox-slide">
                <img
                  class="lightbox-image"
                  data-lightbox-prev-image
                  src="../Cold_Morning_Dark.png"
                  alt=""
                  width="500"
                  height="1036"
                />
              </div>
              <div class="lightbox-slide">
                <img
                  class="lightbox-image"
                  data-lightbox-image
                  src="../Warm_Midday_Light.png"
                  alt=""
                  width="500"
                  height="1036"
                />
              </div>
              <div class="lightbox-slide">
                <img
                  class="lightbox-image"
                  data-lightbox-next-image
                  src="../Hot_Afternoon_Light.png"
                  alt=""
                  width="500"
                  height="1036"
                />
              </div>
            </div>
          </div>
          <button class="lightbox-arrow" type="button" data-gallery-next aria-label="Next image">
            &#8594;
          </button>
        </div>
      </div>
    </div>

    <footer class="site-footer">
      <div class="footer-stack">
        <p data-site="footer-copyright"></p>
        <a class="footer-link" href="/{locale}/privacy-policy.html">Privacy Policy</a>
{footer_locale_switcher}
      </div>
    </footer>

    <script src="site-data.js"></script>
    <script src="../script.js"></script>
  </body>
</html>
"""


def extract_main_content(filename: str) -> str:
    source = (ROOT / filename).read_text(encoding="utf-8")
    match = re.search(r'<main id="main" class="secondary-shell">(.*?)</main>', source, re.S)
    if not match:
        raise RuntimeError(f"Could not extract main content from {filename}")
    return match.group(1).strip()


def render_secondary_page(locale: str, page_kind: str, title: str, description: str, body: str) -> str:
    hreflang_links = render_hreflang_links(page_kind)
    footer_locale_switcher = render_locale_switcher(
        locale, indent="        ", wrapper_class="footer-locale-switcher"
    )
    footer_link = f"/{locale}/privacy-policy.html"

    return f"""<!doctype html>
<html lang="{locale}">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{title}</title>
    <meta
      name="description"
      content="{description}"
    />
    <link rel="canonical" href="{canonical_url(locale, page_kind)}" />
{hreflang_links}
    <link rel="icon" type="image/png" sizes="512x512" href="../favicon.png" />
    <link rel="stylesheet" href="../styles/base.css" />
    <link rel="stylesheet" href="../styles/secondary-pages.css" />
    <link rel="stylesheet" href="../styles/variant-1.css" />
  </head>
  <body class="page page-1">
    <header class="top-nav">
      <div class="nav-shell">
        <a class="nav-brand" href="/{locale}/" aria-label="40 Below home">
          <img class="nav-brand-icon" src="../favicon.png" alt="" width="32" height="32" />
          <span>40 Below</span>
        </a>
        <nav class="nav-actions" aria-label="Primary">
          <a class="nav-link" href="/{locale}/support.html"{' aria-current="page"' if page_kind == "support" else ""}>Support</a>
          <a
            class="nav-store-link"
            href="{APP_STORE_URL}"
            target="_blank"
            rel="noopener noreferrer"
            aria-label="Download 40 Below on the App Store"
          >
            <img
              class="badge-light"
              src="../Download-on-the-App-Store/US/Download_on_App_Store/Black_lockup/SVG/Download_on_the_App_Store_Badge_US-UK_RGB_blk_092917.svg"
              alt="Download on the App Store"
              width="152"
              height="52"
            />
            <img
              class="badge-dark"
              src="../Download-on-the-App-Store/US/Download_on_App_Store/White_lockup/SVG/Download_on_the_App_Store_Badge_US-UK_RGB_wht_092917.svg"
              alt="Download on the App Store"
              width="152"
              height="52"
            />
          </a>
        </nav>
      </div>
    </header>

    <main id="main" class="secondary-shell">
{body}
    </main>

    <footer class="site-footer secondary-footer">
      <div class="footer-stack">
        <p>© <span id="year"></span> Fruit Stand Software</p>
        <a class="footer-link" href="{footer_link}">Privacy Policy</a>
{footer_locale_switcher}
      </div>
    </footer>

    <script src="../script.js"></script>
  </body>
</html>
"""


def render_root_redirect() -> str:
    available_locales = javascript_value(LOCALES)
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>40 Below</title>
    <meta http-equiv="refresh" content="0; url=/{DEFAULT_LOCALE}/" />
    <script>
      const DEFAULT_LOCALE = "{DEFAULT_LOCALE}";
      const LOCALE_STORAGE_KEY = "fruitstandsoftware.locale";
      const AVAILABLE_LOCALES = {available_locales};

      function normalizeLocale(locale) {{
        return (locale || "").trim();
      }}

      function sameLanguageLocale(requestedLocale, availableLocales) {{
        const requestedBase = normalizeLocale(requestedLocale).split("-")[0].toLowerCase();
        if (!requestedBase) {{
          return "";
        }}

        return (
          availableLocales.find((candidate) => candidate.split("-")[0].toLowerCase() === requestedBase) || ""
        );
      }}

      function resolveLocale(requestedLocales) {{
        for (const candidate of requestedLocales) {{
          const normalized = normalizeLocale(candidate);
          if (!normalized) {{
            continue;
          }}

          const exactLocale = AVAILABLE_LOCALES.find(
            (availableLocale) => availableLocale.toLowerCase() === normalized.toLowerCase()
          );
          if (exactLocale) {{
            return exactLocale;
          }}

          const languageMatch = sameLanguageLocale(normalized, AVAILABLE_LOCALES);
          if (languageMatch) {{
            return languageMatch;
          }}
        }}

        return DEFAULT_LOCALE;
      }}

      let savedLocale = "";

      try {{
        savedLocale = window.localStorage.getItem(LOCALE_STORAGE_KEY) || "";
      }} catch (error) {{
        savedLocale = "";
      }}

      const requestedLocales = savedLocale ? [savedLocale, ...(navigator.languages || [])] : navigator.languages || [];
      const targetLocale = resolveLocale(requestedLocales);
      window.location.replace(`/${{targetLocale}}/`);
    </script>
  </head>
  <body>
    <main>
      <p>Redirecting to the best language for your browser.</p>
      <p><a href="/{DEFAULT_LOCALE}/">Continue to English</a></p>
    </main>
  </body>
</html>
"""


def build() -> None:
    support_body = extract_main_content("support.html")
    privacy_body = extract_main_content("privacy-policy.html")

    for locale in LOCALES:
        locale_dir = ROOT / locale
        locale_dir.mkdir(exist_ok=True)
        (locale_dir / "index.html").write_text(render_homepage(locale), encoding="utf-8")
        (locale_dir / "site-data.js").write_text(render_site_data(locale), encoding="utf-8")
        (locale_dir / "support.html").write_text(
            render_secondary_page(
                locale,
                "support",
                "Support | Fruit Stand Software",
                "Support for 40 Below. Email support@fruitstandsoftware.com if you need help or run into trouble.",
                support_body,
            ),
            encoding="utf-8",
        )
        (locale_dir / "privacy-policy.html").write_text(
            render_secondary_page(
                locale,
                "privacy",
                "Privacy Policy | Fruit Stand Software",
                "Privacy policy for 40 Below by Fruit Stand Software.",
                privacy_body,
            ),
            encoding="utf-8",
        )

    (ROOT / "index.html").write_text(render_root_redirect(), encoding="utf-8")


if __name__ == "__main__":
    build()
