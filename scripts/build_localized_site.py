from __future__ import annotations

import html
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
METADATA_DIR = ROOT / "metadata"
SECONDARY_PAGE_TRANSLATIONS = json.loads(
    (ROOT / "secondary-page-translations.json").read_text(encoding="utf-8")
)
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


def locale_text_direction(locale: str) -> str:
    return "rtl" if locale.split("-")[0] in {"ar", "fa", "he", "ur"} else "ltr"


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


def escape_html(value: object) -> str:
    return html.escape(str(value), quote=True)


def render_paragraph_block(paragraphs: list[str], indent: str) -> str:
    return "\n".join(f"{indent}<p>{escape_html(paragraph)}</p>" for paragraph in paragraphs)


def render_feature_list(features: list[str], indent: str) -> str:
    return "\n".join(f"{indent}<li>{escape_html(feature)}</li>" for feature in features)


def get_secondary_page_translation(locale: str) -> dict[str, object]:
    return SECONDARY_PAGE_TRANSLATIONS.get(locale, SECONDARY_PAGE_TRANSLATIONS[DEFAULT_LOCALE])


def render_paragraphs(paragraphs: list[str], indent: str) -> str:
    return "\n".join(f"{indent}<p>{escape_html(paragraph)}</p>" for paragraph in paragraphs)


def render_list_items(items: list[str], indent: str) -> str:
    return "\n".join(f"{indent}<li>{escape_html(item)}</li>" for item in items)


def render_support_main(locale: str) -> str:
    translation = get_secondary_page_translation(locale)
    support = translation["support"]
    email_link = '<a href="mailto:support@fruitstandsoftware.com">support@fruitstandsoftware.com</a>'
    body = escape_html(support["body"]).replace("{email}", email_link)
    subject = html.escape(str(support["subject"]).replace(" ", "%20"), quote=True)

    return f"""      <section class="secondary-header-card reveal">
        <p>{escape_html(support["eyebrow"])}</p>
        <h1 class="secondary-page-title">{escape_html(support["title"])}</h1>
      </section>

      <section class="support-grid">
        <div class="support-card reveal">
          <p>{body}</p>
          <div class="support-actions">
            <a class="support-button" href="mailto:support@fruitstandsoftware.com?subject={subject}">
              {escape_html(support["button"])}
            </a>
          </div>
        </div>
      </section>"""


def render_privacy_sections(sections: list[dict[str, object]]) -> str:
    rendered_sections = []
    for section in sections:
        parts = [
            '              <section class="policy-block">',
            f'                <h3>{escape_html(section["title"])}</h3>',
        ]
        if section.get("subtitle"):
            parts.append(f'                <h4>{escape_html(section["subtitle"])}</h4>')
        if section.get("paragraphs"):
            parts.append(render_paragraphs(section["paragraphs"], "                "))
        if section.get("list"):
            parts.append("                <ul>")
            parts.append(render_list_items(section["list"], "                  "))
            parts.append("                </ul>")
        if section.get("closing"):
            parts.append(f'                <p>{escape_html(section["closing"])}</p>')
        parts.append("              </section>")
        rendered_sections.append("\n".join(parts))

    return "\n\n".join(rendered_sections)


def render_privacy_aside(aside: dict[str, object]) -> str:
    rows = "\n".join(
        [
            "                <div class=\"nutrition-row\">"
            f"\n                  <span>{escape_html(row['label'])}</span>"
            f"\n                  <strong>{escape_html(row['value'])}</strong>"
            "\n                </div>"
            for row in aside["rows"]
        ]
    )

    return f"""            <aside class="policy-aside-card reveal" aria-label="{escape_html(aside["aria_label"])}">
              <section class="nutrition-label">
                <p class="nutrition-heading">{escape_html(aside["heading"])}</p>
                <p class="nutrition-subhead">{escape_html(aside["subhead"])}</p>
                <p class="nutrition-serving">{escape_html(aside["serving"])}</p>
                <p class="nutrition-rule thick"></p>
                <p class="nutrition-big">{escape_html(aside["big_label"])} <span>{escape_html(aside["big_value"])}</span></p>
                <p class="nutrition-rule"></p>
{rows}
                <p class="nutrition-footnote">
                  {escape_html(aside["footnote"])}
                </p>
              </section>
            </aside>"""


def render_privacy_main(locale: str) -> str:
    translation = get_secondary_page_translation(locale)
    privacy = translation["privacy"]
    intro_html = render_paragraphs(privacy["intro"], "                ")
    sections_html = render_privacy_sections(privacy["sections"])
    aside_html = render_privacy_aside(privacy["aside"])

    return f"""      <section class="secondary-header-card reveal">
        <p>{escape_html(privacy["eyebrow"])}</p>
        <h1 class="secondary-page-title">{escape_html(privacy["title"])}</h1>
        <p class="policy-updated"><strong>{escape_html(privacy["updated_label"])}</strong> {escape_html(privacy["updated_value"])}</p>
      </section>

      <div class="policy-page-grid">
            <article class="policy-main-card reveal">
{intro_html}

{sections_html}
            </article>

{aside_html}
      </div>"""


def render_homepage(locale: str) -> str:
    description = parse_description(locale)
    title = read_metadata(locale, "name.txt")
    subtitle = read_metadata(locale, "subtitle.txt")
    promotional_text = read_metadata(locale, "promotional_text.txt")
    keywords = read_metadata(locale, "keywords.txt")
    release_notes = read_metadata(locale, "release_notes.txt")
    hreflang_links = render_hreflang_links("home")
    text_direction = locale_text_direction(locale)
    footer_locale_switcher = render_locale_switcher(
        locale, indent="        ", wrapper_class="footer-locale-switcher"
    )
    description_html = render_paragraph_block(description["description_paragraphs"], "            ")
    features_html = render_feature_list(description["features"], "              ")
    screenshot_alt = escape_html(f"{title} — {subtitle}")

    return f"""<!doctype html>
<html lang="{locale}" dir="{text_direction}">
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
      content="{escape_html(keywords)}"
    />
    <meta property="og:title" content="{escape_html(title)}" />
    <meta
      property="og:description"
      content="{escape_html(promotional_text)}"
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
                alt="{escape_html(title)} app icon"
                width="144"
                height="144"
              />
            </picture>
            <div class="hero-heading-group">
              <h1>{escape_html(title)}</h1>
              <p class="hero-subtitle">{escape_html(subtitle)}</p>
            </div>
          </div>
          <p class="hero-promo">{escape_html(promotional_text)}</p>
          <div class="hero-description prose-block">
{description_html}
            <p class="feature-heading">{escape_html(description["feature_heading"])}</p>
            <ul class="feature-list">
{features_html}
            </ul>
            <p>{escape_html(description["location_text"])}</p>
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
              src="../Warm_Midday_Light.png"
              alt="{screenshot_alt}"
              width="500"
              height="1036"
            />
          </picture>
        </figure>
      </section>

      <section class="content-block release-block reveal">
        <p class="release-copy">{escape_html(release_notes)}</p>
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
        <p>{escape_html(COPYRIGHT)}</p>
        <a class="footer-link" href="/{locale}/privacy-policy.html">Privacy Policy</a>
{footer_locale_switcher}
      </div>
    </footer>

    <script src="../script.js"></script>
  </body>
</html>
"""


def render_secondary_page(locale: str, page_kind: str) -> str:
    translation = get_secondary_page_translation(locale)
    shell = translation["shell"]
    page = translation[page_kind]
    hreflang_links = render_hreflang_links(page_kind)
    text_direction = locale_text_direction(locale)
    footer_locale_switcher = render_locale_switcher(
        locale, indent="        ", wrapper_class="footer-locale-switcher"
    )
    footer_link = f"/{locale}/privacy-policy.html"
    main_content = render_support_main(locale) if page_kind == "support" else render_privacy_main(locale)

    return f"""<!doctype html>
<html lang="{locale}" dir="{text_direction}">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{escape_html(page["page_title"])}</title>
    <meta
      name="description"
      content="{escape_html(page["meta_description"])}"
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
          <a class="nav-link" href="/{locale}/support.html"{' aria-current="page"' if page_kind == "support" else ""}>{escape_html(shell["nav_support"])}</a>
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
{main_content}
    </main>

    <footer class="site-footer secondary-footer">
      <div class="footer-stack">
        <p>© <span id="year"></span> Fruit Stand Software</p>
        <a class="footer-link" href="{footer_link}">{escape_html(shell["footer_privacy"])}</a>
{footer_locale_switcher}
      </div>
    </footer>

    <script src="../script.js"></script>
  </body>
</html>
"""


def render_root_redirect() -> str:
    available_locales = javascript_value(LOCALES)
    title = read_metadata(DEFAULT_LOCALE, "name.txt")
    promotional_text = read_metadata(DEFAULT_LOCALE, "promotional_text.txt")
    social_image_url = f"{SITE_URL}/SocialImage.png"
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{escape_html(title)}</title>
    <meta
      name="description"
      content="{escape_html(promotional_text)}"
    />
    <meta property="og:title" content="{escape_html(title)}" />
    <meta
      property="og:description"
      content="{escape_html(promotional_text)}"
    />
    <meta property="og:type" content="website" />
    <meta property="og:url" content="{SITE_URL}/" />
    <meta property="og:image" content="{social_image_url}" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="{escape_html(title)}" />
    <meta
      name="twitter:description"
      content="{escape_html(promotional_text)}"
    />
    <meta name="twitter:image" content="{social_image_url}" />
    <link rel="canonical" href="{SITE_URL}/" />
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
    for locale in LOCALES:
        locale_dir = ROOT / locale
        locale_dir.mkdir(exist_ok=True)
        (locale_dir / "index.html").write_text(render_homepage(locale), encoding="utf-8")
        site_data_path = locale_dir / "site-data.js"
        if site_data_path.exists():
            site_data_path.unlink()
        (locale_dir / "support.html").write_text(render_secondary_page(locale, "support"), encoding="utf-8")
        (locale_dir / "privacy-policy.html").write_text(render_secondary_page(locale, "privacy"), encoding="utf-8")

    (ROOT / "index.html").write_text(render_root_redirect(), encoding="utf-8")


if __name__ == "__main__":
    build()
