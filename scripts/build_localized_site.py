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
PROMO_PAGE_TRANSLATIONS = json.loads(
    (ROOT / "promo-page-translations.json").read_text(encoding="utf-8")
)
NUMBER_ONE_PAGE_TRANSLATIONS = json.loads(
    (ROOT / "number-one-page-translations.json").read_text(encoding="utf-8")
)
PRESS_PAGE_DATA = json.loads((ROOT / "press-page-data.json").read_text(encoding="utf-8"))
DEFAULT_LOCALE = "en-US"
PRESS_PAGE_LOCALE = "en-US"
SITE_URL = "https://fruitstandsoftware.com"
COPYRIGHT = "2026 © Fruit Stand Software, LLC"
APP_STORE_URL = "https://apps.apple.com/app/id6758684366"
APP_STORE_REDEEM_URL = "https://apps.apple.com/redeem?code="
SOCIAL_IMAGE_URL = f"{SITE_URL}/SocialImage.png"
PRESS_CONTACT_EMAIL = "michael@fruitstandsoftware.com"
FALLBACK_ROOT_LOCALES = ["en-US", "en-GB", "es-ES", "ja", "zh-Hans"]

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
    if page_kind == "press":
        return f"/{PRESS_PAGE_LOCALE}/press.html"
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


def render_press_hreflang_links() -> str:
    return "\n".join(
        [
            f'    <link rel="alternate" hreflang="{PRESS_PAGE_LOCALE}" href="{canonical_url(PRESS_PAGE_LOCALE, "press")}" />',
            f'    <link rel="alternate" hreflang="x-default" href="{canonical_url(PRESS_PAGE_LOCALE, "press")}" />',
        ]
    )


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


def localized_ui_strings(locale: str) -> dict[str, str]:
    strings = {
        "ar-SA": {
            "choose_language": "اختر اللغة",
            "home": "الصفحة الرئيسية لتطبيق 40 Below",
            "primary_nav": "التنقل الرئيسي",
            "app_store": "نزّل 40 Below من App Store",
        },
        "da": {
            "choose_language": "Vælg sprog",
            "home": "40 Below forside",
            "primary_nav": "Primær navigation",
            "app_store": "Hent 40 Below i App Store",
        },
        "de-DE": {
            "choose_language": "Sprache wählen",
            "home": "40 Below Startseite",
            "primary_nav": "Hauptnavigation",
            "app_store": "40 Below im App Store laden",
        },
        "en-CA": {
            "choose_language": "Choose language",
            "home": "40 Below home",
            "primary_nav": "Primary",
            "app_store": "Download 40 Below on the App Store",
        },
        "en-GB": {
            "choose_language": "Choose language",
            "home": "40 Below home",
            "primary_nav": "Primary",
            "app_store": "Download 40 Below on the App Store",
        },
        "en-US": {
            "choose_language": "Choose language",
            "home": "40 Below home",
            "primary_nav": "Primary",
            "app_store": "Download 40 Below on the App Store",
        },
        "es-ES": {
            "choose_language": "Elegir idioma",
            "home": "Inicio de 40 Below",
            "primary_nav": "Navegación principal",
            "app_store": "Descarga 40 Below en el App Store",
        },
        "fi": {
            "choose_language": "Valitse kieli",
            "home": "40 Below -etusivu",
            "primary_nav": "Ensisijainen navigointi",
            "app_store": "Lataa 40 Below App Storesta",
        },
        "fr-FR": {
            "choose_language": "Choisir la langue",
            "home": "Accueil de 40 Below",
            "primary_nav": "Navigation principale",
            "app_store": "Télécharger 40 Below sur l’App Store",
        },
        "hi": {
            "choose_language": "भाषा चुनें",
            "home": "40 Below होम",
            "primary_nav": "मुख्य नेविगेशन",
            "app_store": "App Store पर 40 Below डाउनलोड करें",
        },
        "it": {
            "choose_language": "Scegli la lingua",
            "home": "Home di 40 Below",
            "primary_nav": "Navigazione principale",
            "app_store": "Scarica 40 Below sull’App Store",
        },
        "ja": {
            "choose_language": "言語を選択",
            "home": "40 Belowのホーム",
            "primary_nav": "主要ナビゲーション",
            "app_store": "App Storeで40 Belowをダウンロード",
        },
        "ko": {
            "choose_language": "언어 선택",
            "home": "40 Below 홈",
            "primary_nav": "기본 탐색",
            "app_store": "App Store에서 40 Below 다운로드",
        },
        "nl-NL": {
            "choose_language": "Taal kiezen",
            "home": "40 Below-home",
            "primary_nav": "Hoofdnavigatie",
            "app_store": "Download 40 Below in de App Store",
        },
        "no": {
            "choose_language": "Velg språk",
            "home": "40 Below hjem",
            "primary_nav": "Hovednavigasjon",
            "app_store": "Last ned 40 Below i App Store",
        },
        "pl": {
            "choose_language": "Wybierz język",
            "home": "Strona główna 40 Below",
            "primary_nav": "Nawigacja główna",
            "app_store": "Pobierz 40 Below w App Store",
        },
        "pt-BR": {
            "choose_language": "Escolher idioma",
            "home": "Página inicial do 40 Below",
            "primary_nav": "Navegação principal",
            "app_store": "Baixe 40 Below na App Store",
        },
        "sv": {
            "choose_language": "Välj språk",
            "home": "40 Below startsida",
            "primary_nav": "Huvudnavigering",
            "app_store": "Hämta 40 Below i App Store",
        },
        "tr": {
            "choose_language": "Dil seçin",
            "home": "40 Below ana sayfası",
            "primary_nav": "Birincil gezinme",
            "app_store": "40 Below’u App Store’dan indirin",
        },
        "zh-Hans": {
            "choose_language": "选择语言",
            "home": "40 Below 首页",
            "primary_nav": "主导航",
            "app_store": "在 App Store 下载 40 Below",
        },
        "zh-Hant": {
            "choose_language": "選擇語言",
            "home": "40 Below 首頁",
            "primary_nav": "主要導覽",
            "app_store": "在 App Store 下載 40 Below",
        },
    }
    return strings[locale]


def app_store_badge_code(locale: str) -> str:
    return {
        "ar-SA": "AR",
        "da": "DK",
        "de-DE": "DE",
        "en-CA": "US",
        "en-GB": "US",
        "en-US": "US",
        "es-ES": "ES",
        "fi": "FI",
        "fr-FR": "FR",
        "hi": "IN",
        "it": "IT",
        "ja": "JP",
        "ko": "KR",
        "nl-NL": "NL",
        "no": "NO",
        "pl": "PL",
        "pt-BR": "PTBR",
        "sv": "SE",
        "tr": "TR",
        "zh-Hans": "US",
        "zh-Hant": "US",
    }[locale]


def locale_storefront_region(locale: str) -> str:
    overrides = {
        "da": "DK",
        "fi": "FI",
        "hi": "IN",
        "it": "IT",
        "ja": "JP",
        "ko": "KR",
        "no": "NO",
        "pl": "PL",
        "sv": "SE",
        "tr": "TR",
        "zh-Hans": "CN",
        "zh-Hant": "TW",
    }
    if locale in overrides:
        return overrides[locale]

    if "-" in locale:
        return locale.split("-")[1].upper()

    raise ValueError(f"Unsupported locale without storefront mapping: {locale}")


def storefront_chart_path(region: str) -> str:
    return f"https://apps.apple.com/{region.lower()}/iphone/charts/6001?chart=top-paid"


def charts_storefronts() -> list[dict[str, str]]:
    storefronts: list[dict[str, str]] = []

    for locale in LOCALES:
        region = locale_storefront_region(locale)
        storefronts.append(
            {
                "locale": locale,
                "region": region,
                "chart_url": storefront_chart_path(region),
                "region_name": region_display_name(region),
            }
        )

    return storefronts


def region_display_name(region: str) -> str:
    names = {
        "BR": "Brazil",
        "CA": "Canada",
        "CN": "China mainland",
        "DE": "Germany",
        "DK": "Denmark",
        "ES": "Spain",
        "FI": "Finland",
        "FR": "France",
        "GB": "United Kingdom",
        "IN": "India",
        "IT": "Italy",
        "JP": "Japan",
        "KR": "South Korea",
        "NL": "Netherlands",
        "NO": "Norway",
        "PL": "Poland",
        "SA": "Saudi Arabia",
        "SE": "Sweden",
        "TR": "Turkey",
        "TW": "Taiwan",
        "US": "United States",
    }
    return names.get(region, region)




def app_store_badge_paths(locale: str) -> dict[str, str]:
    badge_code = app_store_badge_code(locale)
    badge_dir = f"../Download-on-the-App-Store/{badge_code}/Download_on_App_Store"
    black_dir = ROOT / "Download-on-the-App-Store" / badge_code / "Download_on_App_Store" / "Black_lockup" / "SVG"
    white_dir = ROOT / "Download-on-the-App-Store" / badge_code / "Download_on_App_Store" / "White_lockup" / "SVG"
    black_file = sorted(black_dir.glob("*.svg"))[0].name
    white_file = sorted(white_dir.glob("*.svg"))[0].name
    return {
        "light": f"{badge_dir}/Black_lockup/SVG/{black_file}",
        "dark": f"{badge_dir}/White_lockup/SVG/{white_file}",
    }


def render_locale_switcher(locale: str, indent: str = "          ", wrapper_class: str = "") -> str:
    ui_strings = localized_ui_strings(locale)
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
            f'{indent}  <span class="visually-hidden">{escape_html(ui_strings["choose_language"])}</span>',
            f'{indent}  <select class="locale-switcher" aria-label="{escape_html(ui_strings["choose_language"])}">',
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


def software_application_schema(locale: str, url: str) -> str:
    title = read_metadata(locale, "name.txt")
    subtitle = read_metadata(locale, "subtitle.txt")
    promotional_text = read_metadata(locale, "promotional_text.txt")
    data = {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": title,
        "alternateName": subtitle,
        "applicationCategory": "WeatherApplication",
        "operatingSystem": "iOS",
        "description": promotional_text,
        "url": url,
        "image": SOCIAL_IMAGE_URL,
        "downloadUrl": APP_STORE_URL,
        "publisher": {
            "@type": "Organization",
            "name": "Fruit Stand Software, LLC",
            "url": SITE_URL,
        },
    }
    return json.dumps(data, ensure_ascii=False, indent=2)


def render_root_fallback_links() -> str:
    locale_labels = {
        "en-US": "English (US)",
        "en-GB": "English (UK)",
        "es-ES": "Español",
        "ja": "日本語",
        "zh-Hans": "简体中文",
    }
    links = "\n".join(
        f'        <li><a href="/{locale}/">{escape_html(locale_labels[locale])}</a></li>'
        for locale in FALLBACK_ROOT_LOCALES
    )
    return f"""      <section aria-labelledby="fallback-locales-heading">
        <h1 id="fallback-locales-heading">40 Below</h1>
        <p>Redirecting to the best language for your browser.</p>
        <p>If you are not redirected, choose a language below.</p>
        <ul>
{links}
        </ul>
        <p><a href="/{DEFAULT_LOCALE}/">Continue to English</a></p>
      </section>"""


def render_robots_txt() -> str:
    return f"""User-agent: *
Allow: /

Sitemap: {SITE_URL}/sitemap.xml
"""


def render_sitemap_xml() -> str:
    urls = [f"{SITE_URL}/", f"{SITE_URL}/number-one.html", canonical_url(PRESS_PAGE_LOCALE, "press")]
    for locale in LOCALES:
        for page_kind in ("home", "support", "privacy"):
            urls.append(canonical_url(locale, page_kind))

    url_entries = "\n".join(
        f"""  <url>
    <loc>{escape_html(url)}</loc>
  </url>"""
        for url in urls
    )
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{url_entries}
</urlset>
"""


def get_secondary_page_translation(locale: str) -> dict[str, object]:
    return SECONDARY_PAGE_TRANSLATIONS.get(locale, SECONDARY_PAGE_TRANSLATIONS[DEFAULT_LOCALE])


def get_promo_page_translation(locale: str = DEFAULT_LOCALE) -> dict[str, object]:
    return PROMO_PAGE_TRANSLATIONS.get(locale, PROMO_PAGE_TRANSLATIONS[DEFAULT_LOCALE])


def get_number_one_page_translation(locale: str = DEFAULT_LOCALE) -> dict[str, object]:
    return NUMBER_ONE_PAGE_TRANSLATIONS.get(locale, NUMBER_ONE_PAGE_TRANSLATIONS[DEFAULT_LOCALE])


def get_press_page(locale: str = PRESS_PAGE_LOCALE) -> dict[str, object]:
    return PRESS_PAGE_DATA.get(locale, PRESS_PAGE_DATA[PRESS_PAGE_LOCALE])


def get_press_assets() -> dict[str, object]:
    return PRESS_PAGE_DATA["assets"]


def press_asset_path(path: str) -> str:
    if path.startswith(("http://", "https://", "../")):
        return path

    return f"../{path.removeprefix('/')}"


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


def render_primary_nav(
    locale: str, ui_strings: dict[str, str], badge_paths: dict[str, str], shell: dict[str, object], current_page: str = ""
) -> str:
    press_current = ' aria-current="page"' if current_page == "press" else ""
    support_current = ' aria-current="page"' if current_page == "support" else ""

    return f"""        <nav class="nav-actions" aria-label="{escape_html(ui_strings["primary_nav"])}">
          <a class="nav-link" href="/{PRESS_PAGE_LOCALE}/press.html"{press_current}>Press</a>
          <a class="nav-link" href="/{locale}/support.html"{support_current}>{escape_html(shell["nav_support"])}</a>
          <a
            class="nav-store-link"
            href="{APP_STORE_URL}"
            target="_blank"
            rel="noopener noreferrer"
            aria-label="{escape_html(ui_strings["app_store"])}"
          >
            <img
              class="badge-light"
              src="{badge_paths["light"]}"
              alt="{escape_html(ui_strings["app_store"])}"
              width="152"
              height="52"
            />
            <img
              class="badge-dark"
              src="{badge_paths["dark"]}"
              alt="{escape_html(ui_strings["app_store"])}"
              width="152"
              height="52"
            />
          </a>
        </nav>"""


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
              <section class="policy-block">
{intro_html}
              </section>

{sections_html}
            </article>

{aside_html}
      </div>"""


def render_press_factsheet(title: str, subtitle: str) -> str:
    press = get_press_page(PRESS_PAGE_LOCALE)
    store = press["factsheet_store"]
    press_kit_download = get_press_assets()["downloads"]["press_kit"]
    stats = [
        {
            "icon": "⛅",
            "value": f'{store["category_value"]} Category',
            "detail": "",
        },
        {
            "icon": "🧑‍💻",
            "value": store["developer_value"],
            "detail": "",
        },
        {
            "icon": "🌍",
            "value": store["languages_value"],
            "detail": "",
        },
        {
            "icon": "♿",
            "value": store["accessibility_value"],
            "detail": "",
        },
        {
            "icon": "🔒",
            "value": store["privacy_value"],
            "detail": "",
        },
        {
            "icon": "🍎",
            "value": store["technology_value"],
            "detail": "",
        },
    ]
    stats_html = "\n".join(
        [
            f"""              <article class="press-stat-card">
                <div class="press-stat-icon" aria-hidden="true">{escape_html(item["icon"])}</div>
                <div class="press-stat-copy">
                  <p class="press-stat-value">{escape_html(item["value"])}</p>
                  {f'<p class="press-stat-detail">{escape_html(item["detail"])}</p>' if item["detail"] else ""}
                </div>
              </article>"""
            for item in stats
        ]
    )

    return f"""          <aside class="policy-aside-card reveal press-factsheet-card" aria-labelledby="press-factsheet-heading">
            <div class="press-card-stack">
              <h2 id="press-factsheet-heading" class="visually-hidden">{escape_html(press["factsheet_heading"])}</h2>
              <div class="press-store-summary">
                <picture class="press-store-icon">
                  <source srcset="{press_asset_path("40BelowIcons/40BelowDark.png")}" media="(prefers-color-scheme: dark)" />
                  <img src="{press_asset_path("40BelowIcons/40BelowLight.png")}" alt="" width="88" height="88" />
                </picture>
                <div class="press-store-copy">
                  <p class="press-store-name">{escape_html(title)}</p>
                  <p class="press-store-subtitle">{escape_html(subtitle)}</p>
                  <p class="press-store-price">{escape_html(store["price"])}</p>
                  <p class="press-store-rating" aria-label="Five star App Store rating">⭐ ⭐ ⭐ ⭐ ⭐</p>
                </div>
              </div>
              <div class="press-stats-grid">
{stats_html}
              </div>
              <div class="support-actions press-factsheet-download">
                <a class="support-button" href="{escape_html(press_asset_path(press_kit_download["href"]))}" download>
                  {escape_html(press["download_button"])}
                </a>
              </div>
            </div>
          </aside>"""


def render_press_gallery_sections(assets: dict[str, object], sections: dict[str, object], empty_title: str, empty_body: str) -> str:
    rendered_sections = []

    for key in ("iphone", "ipad", "mac"):
        section = sections[key]
        images = assets["galleries"][key]
        group_name = f"press-{key}"

        if images:
            thumbs = "\n".join(
                [
                    f"""              <button class="gallery-thumb press-gallery-thumb" type="button" data-gallery-group="{group_name}" data-gallery-index="{index}" aria-label="Open {escape_html(image["label"])} screenshot">
                <img src="{escape_html(press_asset_path(image["src"]))}" alt="{escape_html(image["alt"])}" width="250" height="518" loading="lazy" />
              </button>"""
                    for index, image in enumerate(images)
                ]
            )
            gallery_content = f"""            <div class="gallery-grid press-gallery-grid">
{thumbs}
            </div>"""
        else:
            gallery_content = f"""            <div class="press-empty-state" role="status" aria-live="polite">
              <h3>{escape_html(empty_title)}</h3>
              <p>{escape_html(empty_body)}</p>
            </div>"""

        rendered_sections.append(
            f"""        <section class="support-card reveal press-gallery-card" aria-labelledby="{group_name}-heading">
          <div class="press-card-stack">
            <h2 id="{group_name}-heading" class="press-card-title">{escape_html(section["title"])}</h2>
            {'<p>' + escape_html(section["description"]) + '</p>' if section.get("description") else ''}
          </div>
{gallery_content}
        </section>"""
        )

    return "\n".join(rendered_sections)


def render_press_technology_section() -> str:
    press = get_press_page(PRESS_PAGE_LOCALE)
    cards = []

    for card in press["technology_cards"]:
        if card["kind"] == "hero":
            cards.append(
                f"""        <article class="support-card reveal press-tech-hero-card" aria-labelledby="press-tech-hero-heading">
          <div class="press-tech-hero-media">
            <img src="{escape_html(press_asset_path(card["image"]))}" alt="" loading="lazy" />
          </div>
          <div class="press-tech-hero-copy">
            <p class="eyebrow">{escape_html(card["eyebrow"])}</p>
            <h3 id="press-tech-hero-heading" class="press-card-title">{escape_html(card["title"])}</h3>
            <p>{escape_html(card["body"])}</p>
          </div>
        </article>"""
            )
            continue

        body_html = "\n".join(f"              <li>{escape_html(item)}</li>" for item in card["body"])
        cards.append(
            f"""        <article class="support-card reveal press-tech-card">
          <div class="press-tech-card-art">
            <img class="press-tech-card-image" src="{escape_html(press_asset_path(card["image"]))}" alt="" loading="lazy" />
          </div>
          <div class="press-card-stack">
            <h3 class="press-card-title">{escape_html(card["title"])}</h3>
            <ul class="press-tech-list">
{body_html}
            </ul>
          </div>
        </article>"""
        )

    cards_html = "\n".join(cards)

    return f"""      <section class="press-technology-section" aria-labelledby="press-technology-heading">
        <div class="secondary-header-card reveal press-technology-header">
          <h2 id="press-technology-heading" class="press-card-title">{escape_html(press["technology_heading"])}</h2>
          <p class="secondary-page-lead">{escape_html(press["technology_intro"])}</p>
        </div>
        <div class="press-technology-grid">
{cards_html}
        </div>
      </section>"""


def render_press_main() -> str:
    press = get_press_page(PRESS_PAGE_LOCALE)
    assets = get_press_assets()
    title = read_metadata(PRESS_PAGE_LOCALE, "name.txt")
    subtitle = read_metadata(PRESS_PAGE_LOCALE, "subtitle.txt")
    promotional_text = read_metadata(PRESS_PAGE_LOCALE, "promotional_text.txt")
    description = parse_description(PRESS_PAGE_LOCALE)
    factsheet_html = render_press_factsheet(title, subtitle)
    gallery_sections = render_press_gallery_sections(
        assets,
        press["gallery_sections"],
        press["empty_state_title"],
        press["empty_state_body"],
    )
    technology_section = render_press_technology_section()
    contact_email_link = '<a href="mailto:michael@fruitstandsoftware.com">michael@fruitstandsoftware.com</a>'
    contact_body = escape_html(press["contact_body"]).replace("{email}", contact_email_link)
    subject = html.escape(str(press["contact_subject"]).replace(" ", "%20"), quote=True)
    body_prefill = html.escape(str(press["contact_body_prefill"]), quote=True)

    return f"""      <section class="secondary-header-card reveal press-hero">
        <div class="press-card-stack">
          <h1 class="secondary-page-title">{escape_html(press["title"])}</h1>
          <p class="secondary-page-lead">{escape_html(press["lead"])}</p>
        </div>
      </section>

      <div class="press-intro-grid">
        <article class="policy-main-card reveal press-overview-card" aria-labelledby="press-overview-heading">
          <div class="press-card-stack">
            <h2 id="press-overview-heading" class="press-card-title">{escape_html(press["overview_heading"])}</h2>
            <p>{escape_html(press["overview_intro"])}</p>
            <p>{escape_html(promotional_text)}</p>
            {render_paragraphs(description["description_paragraphs"], "            ")}
            <p>{escape_html(press["overview_outro"])}</p>
          </div>
        </article>

{factsheet_html}
      </div>

      <section class="press-gallery-stack" aria-labelledby="press-gallery-heading">
{technology_section}
{gallery_sections}
      </section>

      <section class="support-grid press-contact-grid" aria-labelledby="press-contact-heading">
        <article class="support-card reveal press-contact-card">
          <div class="press-card-stack">
            <h2 id="press-contact-heading" class="press-card-title">{escape_html(press["contact_heading"])}</h2>
            <p>{contact_body}</p>
            <div class="support-actions">
              <a class="support-button" href="mailto:{PRESS_CONTACT_EMAIL}?subject={subject}&body={body_prefill}">
                {escape_html(press["contact_button"])}
              </a>
            </div>
          </div>
        </article>
      </section>"""


def render_lightbox_markup(
    previous_image: dict[str, str],
    image: dict[str, str],
    next_image: dict[str, str],
    close_label: str,
    previous_label: str,
    next_label: str,
    use_root_paths: bool = False,
) -> str:
    def lightbox_src(src: str) -> str:
        return press_asset_path(src) if use_root_paths else f"../{src}"

    return f"""    <div
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
          <button class="lightbox-close" type="button" data-lightbox-close aria-label="{escape_html(close_label)}">
            Close
          </button>
        </div>
        <div class="lightbox-stage" data-lightbox-stage>
          <button class="lightbox-arrow" type="button" data-gallery-prev aria-label="{escape_html(previous_label)}">
            &#8592;
          </button>
          <div class="lightbox-viewport" data-lightbox-viewport>
            <div class="lightbox-track" data-lightbox-track>
              <div class="lightbox-slide">
                <img
                  class="lightbox-image"
                  data-lightbox-prev-image
                  src="{escape_html(lightbox_src(previous_image["src"]))}"
                  alt="{escape_html(previous_image["alt"])}"
                  width="500"
                  height="1036"
                />
              </div>
              <div class="lightbox-slide">
                <img
                  class="lightbox-image"
                  data-lightbox-image
                  src="{escape_html(lightbox_src(image["src"]))}"
                  alt="{escape_html(image["alt"])}"
                  width="500"
                  height="1036"
                />
              </div>
              <div class="lightbox-slide">
                <img
                  class="lightbox-image"
                  data-lightbox-next-image
                  src="{escape_html(lightbox_src(next_image["src"]))}"
                  alt="{escape_html(next_image["alt"])}"
                  width="500"
                  height="1036"
                />
              </div>
            </div>
          </div>
          <button class="lightbox-arrow" type="button" data-gallery-next aria-label="{escape_html(next_label)}">
            &#8594;
          </button>
        </div>
      </div>
    </div>"""


def render_press_page() -> str:
    press = get_press_page(PRESS_PAGE_LOCALE)
    shell = get_secondary_page_translation(PRESS_PAGE_LOCALE)["shell"]
    ui_strings = localized_ui_strings(PRESS_PAGE_LOCALE)
    badge_paths = {key: press_asset_path(path) for key, path in app_store_badge_paths(PRESS_PAGE_LOCALE).items()}
    text_direction = locale_text_direction(PRESS_PAGE_LOCALE)
    hreflang_links = render_press_hreflang_links()
    footer_locale_switcher = render_locale_switcher(
        PRESS_PAGE_LOCALE, indent="        ", wrapper_class="footer-locale-switcher"
    )
    assets = get_press_assets()
    homepage_gallery = assets["galleries"]["iphone"]
    lightbox_markup = render_lightbox_markup(
        homepage_gallery[-1],
        homepage_gallery[0],
        homepage_gallery[1],
        press["lightbox_close"],
        press["lightbox_previous"],
        press["lightbox_next"],
        use_root_paths=True,
    )
    gallery_groups = {
        "press-iphone": [{**image, "src": press_asset_path(image["src"])} for image in assets["galleries"]["iphone"]],
        "press-ipad": [{**image, "src": press_asset_path(image["src"])} for image in assets["galleries"]["ipad"]],
        "press-mac": [{**image, "src": press_asset_path(image["src"])} for image in assets["galleries"]["mac"]],
    }
    primary_nav = render_primary_nav(PRESS_PAGE_LOCALE, ui_strings, badge_paths, shell, current_page="press")

    return f"""<!doctype html>
<html lang="{PRESS_PAGE_LOCALE}" dir="{text_direction}">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{escape_html(press["page_title"])}</title>
    <meta
      name="description"
      content="{escape_html(press["meta_description"])}"
    />
    <meta property="og:title" content="{escape_html(press["page_title"])}" />
    <meta
      property="og:description"
      content="{escape_html(press["meta_description"])}"
    />
    <meta property="og:type" content="website" />
    <meta property="og:url" content="{canonical_url(PRESS_PAGE_LOCALE, "press")}" />
    <meta property="og:image" content="{SOCIAL_IMAGE_URL}" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="{escape_html(press["page_title"])}" />
    <meta
      name="twitter:description"
      content="{escape_html(press["meta_description"])}"
    />
    <meta name="twitter:image" content="{SOCIAL_IMAGE_URL}" />
    <link rel="canonical" href="{canonical_url(PRESS_PAGE_LOCALE, "press")}" />
{hreflang_links}
    <link rel="icon" type="image/png" sizes="512x512" href="../favicon.png" />
    <link rel="stylesheet" href="../styles/base.css" />
    <link rel="stylesheet" href="../styles/secondary-pages.css" />
    <link rel="stylesheet" href="../styles/variant-1.css" />
  </head>
  <body class="page page-1">
    <header class="top-nav">
      <div class="nav-shell">
        <a class="nav-brand" href="/{PRESS_PAGE_LOCALE}/" aria-label="{escape_html(ui_strings["home"])}">
          <img class="nav-brand-icon" src="../favicon.png" alt="" width="32" height="32" />
          <span>40 Below</span>
        </a>
{primary_nav}
      </div>
    </header>

    <main id="main" class="secondary-shell">
{render_press_main()}
    </main>

{lightbox_markup}

    <footer class="site-footer secondary-footer">
      <div class="footer-stack">
        <p>© <span id="year"></span> Fruit Stand Software</p>
        <a class="footer-link" href="/{PRESS_PAGE_LOCALE}/privacy-policy.html">{escape_html(shell["footer_privacy"])}</a>
{footer_locale_switcher}
      </div>
    </footer>

    <script>
      window.galleryGroups = {javascript_value(gallery_groups)};
    </script>
    <script src="../script.js"></script>
  </body>
</html>
"""


def render_homepage(locale: str) -> str:
    translation = get_secondary_page_translation(locale)
    shell = translation["shell"]
    ui_strings = localized_ui_strings(locale)
    badge_paths = app_store_badge_paths(locale)
    description = parse_description(locale)
    title = read_metadata(locale, "name.txt")
    subtitle = read_metadata(locale, "subtitle.txt")
    promotional_text = read_metadata(locale, "promotional_text.txt")
    keywords = read_metadata(locale, "keywords.txt")
    release_notes = read_metadata(locale, "release_notes.txt")
    hreflang_links = render_hreflang_links("home")
    text_direction = locale_text_direction(locale)
    structured_data = software_application_schema(locale, canonical_url(locale, "home"))
    footer_locale_switcher = render_locale_switcher(
        locale, indent="        ", wrapper_class="footer-locale-switcher"
    )
    description_html = render_paragraph_block(description["description_paragraphs"], "            ")
    features_html = render_feature_list(description["features"], "              ")
    screenshot_alt = escape_html(f"{title} — {subtitle}")
    gallery_images = [
        {"src": "Cold_Morning_Dark.png", "alt": "Cold Morning Dark screenshot"},
        {"src": "Cold_Morning_Dark_Forecast.png", "alt": "Cold Morning Dark Forecast screenshot"},
        {"src": "Warm_Midday_Light.png", "alt": "Open Warm Midday Light screenshot"},
        {"src": "Hot_Afternoon_Light.png", "alt": "Hot Afternoon Light screenshot"},
        {"src": "Cold_Night_Dark.png", "alt": "Cold Night Dark screenshot"},
        {"src": "Warm_Night_Dark.png", "alt": "Warm Night Dark screenshot"},
    ]
    primary_nav = render_primary_nav(locale, ui_strings, badge_paths, shell)
    lightbox_markup = render_lightbox_markup(
        gallery_images[-1],
        gallery_images[0],
        gallery_images[2],
        "Close gallery",
        "Previous image",
        "Next image",
    )

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
    <meta property="og:url" content="{canonical_url(locale, "home")}" />
    <meta property="og:image" content="{SOCIAL_IMAGE_URL}" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="{escape_html(title)}" />
    <meta
      name="twitter:description"
      content="{escape_html(promotional_text)}"
    />
    <meta name="twitter:image" content="{SOCIAL_IMAGE_URL}" />
    <link rel="canonical" href="{canonical_url(locale, "home")}" />
{hreflang_links}
    <script type="application/ld+json">
{structured_data}
    </script>
    <link rel="icon" type="image/png" sizes="512x512" href="../favicon.png" />
    <link rel="stylesheet" href="../styles/base.css" />
    <link rel="stylesheet" href="../styles/variant-1.css" />
  </head>
  <body class="page page-1">
    <header class="top-nav">
      <div class="nav-shell">
        <a class="nav-brand" href="/{locale}/" aria-label="{escape_html(ui_strings["home"])}">
          <img class="nav-brand-icon" src="../favicon.png" alt="" width="32" height="32" />
          <span>40 Below</span>
        </a>
{primary_nav}
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
          <button class="gallery-thumb" type="button" data-gallery-group="default" data-gallery-index="0" aria-label="Open Cold Morning Dark screenshot">
            <img src="../Cold_Morning_Dark.png" alt="Cold Morning Dark screenshot" width="250" height="518" loading="lazy" />
          </button>
          <button class="gallery-thumb" type="button" data-gallery-group="default" data-gallery-index="1" aria-label="Open Cold Morning Dark Forecast screenshot">
            <img src="../Cold_Morning_Dark_Forecast.png" alt="Cold Morning Dark Forecast screenshot" width="250" height="518" loading="lazy" />
          </button>
          <button class="gallery-thumb" type="button" data-gallery-group="default" data-gallery-index="2" aria-label="Open Warm Midday Light screenshot">
            <img src="../Warm_Midday_Light.png" alt="Open Warm Midday Light screenshot" width="250" height="518" loading="lazy" />
          </button>
          <button class="gallery-thumb" type="button" data-gallery-group="default" data-gallery-index="3" aria-label="Open Hot Afternoon Light screenshot">
            <img src="../Hot_Afternoon_Light.png" alt="Hot Afternoon Light screenshot" width="250" height="518" loading="lazy" />
          </button>
          <button class="gallery-thumb" type="button" data-gallery-group="default" data-gallery-index="4" aria-label="Open Cold Night Dark screenshot">
            <img src="../Cold_Night_Dark.png" alt="Cold Night Dark screenshot" width="250" height="518" loading="lazy" />
          </button>
          <button class="gallery-thumb" type="button" data-gallery-group="default" data-gallery-index="5" aria-label="Open Warm Night Dark screenshot">
            <img src="../Warm_Night_Dark.png" alt="Warm Night Dark screenshot" width="250" height="518" loading="lazy" />
          </button>
        </div>
      </section>
    </main>

{lightbox_markup}

    <footer class="site-footer">
      <div class="footer-stack">
        <p>{escape_html(COPYRIGHT)}</p>
        <a class="footer-link" href="/{locale}/privacy-policy.html">{escape_html(shell["footer_privacy"])}</a>
{footer_locale_switcher}
      </div>
    </footer>

    <script>
      window.galleryGroups = {javascript_value({"default": gallery_images})};
    </script>
    <script src="../script.js"></script>
  </body>
</html>
"""


def render_secondary_page(locale: str, page_kind: str) -> str:
    translation = get_secondary_page_translation(locale)
    shell = translation["shell"]
    page = translation[page_kind]
    ui_strings = localized_ui_strings(locale)
    badge_paths = app_store_badge_paths(locale)
    hreflang_links = render_hreflang_links(page_kind)
    text_direction = locale_text_direction(locale)
    footer_locale_switcher = render_locale_switcher(
        locale, indent="        ", wrapper_class="footer-locale-switcher"
    )
    footer_link = f"/{locale}/privacy-policy.html"
    main_content = render_support_main(locale) if page_kind == "support" else render_privacy_main(locale)
    primary_nav = render_primary_nav(locale, ui_strings, badge_paths, shell, current_page=page_kind)

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
        <a class="nav-brand" href="/{locale}/" aria-label="{escape_html(ui_strings["home"])}">
          <img class="nav-brand-icon" src="../favicon.png" alt="" width="32" height="32" />
          <span>40 Below</span>
        </a>
{primary_nav}
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


def render_promo_page(locale: str = DEFAULT_LOCALE) -> str:
    page = get_promo_page_translation(locale)
    ui_strings = localized_ui_strings(locale)
    text_direction = locale_text_direction(locale)
    social_image_url = f"{SITE_URL}/40BelowIcons/40BelowLight.png"
    config = {
        "redeemBaseUrl": APP_STORE_REDEEM_URL,
        "appStoreUrl": APP_STORE_URL,
        "validPattern": "^[A-Z0-9]{12}$",
        "introTemplate": page["intro"],
        "successCta": page["success_cta"],
        "fallbackCta": page["fallback_cta"],
        "missingMessage": page["missing_message"],
        "malformedMessage": page["malformed_message"],
    }

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
    <meta property="og:title" content="{escape_html(page["page_title"])}" />
    <meta
      property="og:description"
      content="{escape_html(page["meta_description"])}"
    />
    <meta property="og:type" content="website" />
    <meta property="og:url" content="{SITE_URL}/redeem.html" />
    <meta property="og:image" content="{social_image_url}" />
    <meta name="twitter:card" content="summary" />
    <meta name="twitter:title" content="{escape_html(page["page_title"])}" />
    <meta
      name="twitter:description"
      content="{escape_html(page["meta_description"])}"
    />
    <meta name="twitter:image" content="{social_image_url}" />
    <meta name="robots" content="noindex, nofollow" />
    <link rel="canonical" href="{SITE_URL}/redeem.html" />
    <link rel="icon" type="image/png" sizes="512x512" href="favicon.png" />
    <link rel="stylesheet" href="styles/base.css" />
    <link rel="stylesheet" href="styles/redeem.css" />
  </head>
  <body class="page promo-page">
    <main class="promo-shell">
      <section class="promo-card" aria-labelledby="promo-heading">
        <picture class="promo-icon">
          <source srcset="40BelowIcons/40BelowDark.png" media="(prefers-color-scheme: dark)" />
          <img
            src="40BelowIcons/40BelowLight.png"
            alt="{escape_html(page["icon_alt"])}"
            width="240"
            height="240"
          />
        </picture>
        <div class="promo-copy">
          <p class="promo-message" data-promo-intro>{escape_html(page["intro"])}</p>
          <h1 id="promo-heading" class="promo-title" data-promo-title>{escape_html(page["title"])}</h1>
          <p class="promo-status" data-promo-status role="status" aria-live="polite">
            {escape_html(page["intro"])}
          </p>
        </div>
        <a
          class="promo-button"
          data-promo-button
          href="{APP_STORE_URL}"
          target="_blank"
          rel="noopener noreferrer"
          aria-label="{escape_html(ui_strings["app_store"])}"
        >
          {escape_html(page["fallback_cta"])}
        </a>
      </section>
    </main>

    <script>
      window.promoPageConfig = {javascript_value(config)};
    </script>
    <script src="script.js"></script>
  </body>
</html>
"""


def render_number_one_page(locale: str = DEFAULT_LOCALE) -> str:
    page = get_number_one_page_translation(locale)
    text_direction = locale_text_direction(locale)
    social_image_url = f"{SITE_URL}/40BelowIcons/40BelowLight.png"
    badge_paths = app_store_badge_paths(locale)

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
    <meta property="og:title" content="{escape_html(page["page_title"])}" />
    <meta
      property="og:description"
      content="{escape_html(page["meta_description"])}"
    />
    <meta property="og:type" content="website" />
    <meta property="og:url" content="{SITE_URL}/number-one.html" />
    <meta property="og:image" content="{social_image_url}" />
    <meta name="twitter:card" content="summary" />
    <meta name="twitter:title" content="{escape_html(page["page_title"])}" />
    <meta
      name="twitter:description"
      content="{escape_html(page["meta_description"])}"
    />
    <meta name="twitter:image" content="{social_image_url}" />
    <meta name="robots" content="index, follow" />
    <link rel="canonical" href="{SITE_URL}/number-one.html" />
    <link rel="icon" type="image/png" sizes="512x512" href="favicon.png" />
    <link rel="stylesheet" href="styles/base.css" />
    <link rel="stylesheet" href="styles/redeem.css" />
  </head>
  <body class="page promo-page">
    <main class="promo-shell">
      <section class="promo-card" aria-labelledby="promo-heading">
        <picture class="promo-icon">
          <source srcset="40BelowIcons/40BelowDark.png" media="(prefers-color-scheme: dark)" />
          <img
            src="40BelowIcons/40BelowLight.png"
            alt="{escape_html(page["icon_alt"])}"
            width="240"
            height="240"
          />
        </picture>
        <div class="promo-copy">
          <h1 id="promo-heading" class="promo-title">{escape_html(page["title"])}</h1>
          <p class="promo-footnote">{escape_html(page["footnote"])}</p>
        </div>
        <div class="promo-actions">
          <a
            class="promo-button"
            href="{APP_STORE_URL}"
            target="_blank"
            rel="noopener noreferrer"
            aria-label="{escape_html(page["badge_aria_label"])}"
          >
            {escape_html(page["cta"])}
          </a>
          <a
            class="promo-store-link"
            href="{APP_STORE_URL}"
            target="_blank"
            rel="noopener noreferrer"
            aria-label="{escape_html(page["badge_aria_label"])}"
          >
            <img
              class="promo-badge badge-light"
              src="{badge_paths["light"].removeprefix('../')}"
              alt="{escape_html(page["badge_alt"])}"
              width="180"
              height="60"
            />
            <img
              class="promo-badge badge-dark"
              src="{badge_paths["dark"].removeprefix('../')}"
              alt="{escape_html(page["badge_alt"])}"
              width="180"
              height="60"
            />
          </a>
        </div>
      </section>
    </main>
  </body>
</html>
"""


def render_root_redirect() -> str:
    available_locales = javascript_value(LOCALES)
    title = read_metadata(DEFAULT_LOCALE, "name.txt")
    promotional_text = read_metadata(DEFAULT_LOCALE, "promotional_text.txt")
    fallback_links = render_root_fallback_links()
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
    <meta property="og:image" content="{SOCIAL_IMAGE_URL}" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="{escape_html(title)}" />
    <meta
      name="twitter:description"
      content="{escape_html(promotional_text)}"
    />
    <meta name="twitter:image" content="{SOCIAL_IMAGE_URL}" />
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
{fallback_links}
    </main>
  </body>
</html>
"""


def render_charts_page() -> str:
    storefronts = charts_storefronts()
    storefront_cards = "\n".join(
        f"""        <li class="storefront-card reveal">
          <div class="storefront-card-copy">
            <p class="chart-card-eyebrow">{escape_html(storefront["region"])}</p>
            <h2 class="storefront-card-title">{escape_html(storefront["region_name"])}</h2>
            <p class="storefront-card-detail">Metadata locale: {escape_html(storefront["locale"])}</p>
          </div>
          <a
            class="support-button storefront-card-link"
            href="{escape_html(storefront["chart_url"])}"
            target="_blank"
            rel="noopener noreferrer"
            aria-label="Open the Top Paid iPhone chart for {escape_html(storefront["region_name"])}"
          >
            Open chart
          </a>
        </li>"""
        for storefront in storefronts
    )

    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Top Paid Charts | Fruit Stand Software</title>
    <meta
      name="description"
      content="Open the App Store Top Paid iPhone chart for every storefront represented by this site's localized metadata."
    />
    <meta name="robots" content="noindex, nofollow" />
    <meta property="og:title" content="Top Paid Charts" />
    <meta
      property="og:description"
      content="Open the App Store Top Paid iPhone chart for every storefront represented by this site's localized metadata."
    />
    <meta property="og:type" content="website" />
    <meta property="og:url" content="{SITE_URL}/charts.html" />
    <meta property="og:image" content="{SOCIAL_IMAGE_URL}" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="Top Paid Charts" />
    <meta
      name="twitter:description"
      content="Open the App Store Top Paid iPhone chart for every storefront represented by this site's localized metadata."
    />
    <meta name="twitter:image" content="{SOCIAL_IMAGE_URL}" />
    <link rel="canonical" href="{SITE_URL}/charts.html" />
    <link rel="icon" type="image/png" sizes="512x512" href="favicon.png" />
    <link rel="stylesheet" href="styles/base.css" />
    <link rel="stylesheet" href="styles/secondary-pages.css" />
    <link rel="stylesheet" href="styles/variant-1.css" />
    <link rel="stylesheet" href="styles/charts.css" />
  </head>
  <body class="page page-1">
    <a class="visually-hidden focus-skip" href="#main">Skip to storefront list</a>

    <header class="top-nav">
      <div class="nav-shell">
        <a class="nav-brand" href="/en-US/" aria-label="40 Below home">
          <img class="nav-brand-icon" src="favicon.png" alt="" width="32" height="32" />
          <span>40 Below</span>
        </a>
        <nav class="nav-actions" aria-label="Primary">
          <a class="nav-link" href="/en-US/press.html">Press</a>
          <a class="nav-link" href="/en-US/support.html">Support</a>
          <a
            class="nav-store-link"
            href="{APP_STORE_URL}"
            target="_blank"
            rel="noopener noreferrer"
            aria-label="Download 40 Below on the App Store"
          >
            <img
              class="badge-light"
              src="Download-on-the-App-Store/US/Download_on_App_Store/Black_lockup/SVG/Download_on_the_App_Store_Badge_US-UK_RGB_blk_092917.svg"
              alt="Download on the App Store"
              width="152"
              height="52"
            />
            <img
              class="badge-dark"
              src="Download-on-the-App-Store/US/Download_on_App_Store/White_lockup/SVG/Download_on_the_App_Store_Badge_US-UK_RGB_wht_092917.svg"
              alt="Download on the App Store"
              width="152"
              height="52"
            />
          </a>
        </nav>
      </div>
    </header>

    <main id="main" class="secondary-shell charts-shell">
      <section class="secondary-header-card charts-hero reveal">
        <div class="charts-hero-copy">
          <p>App Store Dashboard</p>
          <h1 class="secondary-page-title">Top Paid iPhone Charts</h1>
          <p class="secondary-page-lead">
            Open the Top Paid iPhone chart for every storefront represented by the localized
            metadata in this repo.
          </p>
        </div>
        <div class="charts-hero-meta">
          <p class="charts-meta-label">Coverage</p>
          <p class="charts-meta-value">{len(storefronts)} storefronts</p>
          <p class="charts-meta-footnote">
            Storefront selection comes directly from the locale directories in `metadata/`.
            Each link opens the live App Store chart page in a new tab.
          </p>
        </div>
      </section>

      <section class="ranking-list-card reveal" aria-labelledby="ranking-results-title">
        <div class="chart-card-header">
          <div>
            <p class="chart-card-eyebrow">Storefronts</p>
            <h2 id="ranking-results-title" class="chart-card-title">Available chart links</h2>
          </div>
        </div>
        <ul class="storefront-grid">
{storefront_cards}
        </ul>
      </section>
    </main>

    <footer class="site-footer secondary-footer">
      <div class="footer-stack">
        <p>&copy; <span id="year"></span> Fruit Stand Software</p>
        <a class="footer-link" href="/en-US/privacy-policy.html">Privacy Policy</a>
      </div>
    </footer>

    <script src="script.js"></script>
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
        if locale == PRESS_PAGE_LOCALE:
            (locale_dir / "press.html").write_text(render_press_page(), encoding="utf-8")

    (ROOT / "index.html").write_text(render_root_redirect(), encoding="utf-8")
    (ROOT / "charts.html").write_text(render_charts_page(), encoding="utf-8")
    (ROOT / "number-one.html").write_text(render_number_one_page(), encoding="utf-8")
    (ROOT / "redeem.html").write_text(render_promo_page(), encoding="utf-8")
    (ROOT / "robots.txt").write_text(render_robots_txt(), encoding="utf-8")
    (ROOT / "sitemap.xml").write_text(render_sitemap_xml(), encoding="utf-8")


if __name__ == "__main__":
    build()
