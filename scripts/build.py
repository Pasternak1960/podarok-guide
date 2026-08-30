#!/usr/bin/env python3
"""
Статический генератор сайта ПодарокГид.
Читает content/published/*.md -> собирает /public (готовый сайт для деплоя).
Не требует внешних сервисов, кроме пакета `markdown` (ставится в CI).
"""
import json
import os
import re
import sys
import urllib.parse
from datetime import datetime, timezone
from string import Template

try:
    import markdown as md
except ImportError:
    sys.exit("Нужен пакет 'markdown'. Установите: pip install markdown")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT_DIR = os.path.join(ROOT, "content", "published")
TEMPLATE_PATH = os.path.join(ROOT, "templates", "base.html")
STATIC_DIR = os.path.join(ROOT, "static")
OUT_DIR = os.path.join(ROOT, "public")
CONFIG_PATH = os.path.join(ROOT, "config.json")

FRONT_MATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.DOTALL)


def load_config():
    with open(CONFIG_PATH, encoding="utf-8") as f:
        return json.load(f)


def parse_front_matter(text):
    m = FRONT_MATTER_RE.match(text)
    if not m:
        raise ValueError("Нет YAML front matter в статье")
    raw_fm, body = m.group(1), m.group(2)
    fm = {}
    for line in raw_fm.splitlines():
        line = line.strip()
        if not line or ":" not in line:
            continue
        key, val = line.split(":", 1)
        fm[key.strip()] = val.strip().strip('"')
    return fm, body


def replace_affiliate_links(html, aff_networks):
    """
    Превращает href="ozon://<url-encoded-target>" и href="wb://..."
    в реальные партнёрские ссылки согласно config.json,
    и добавляет rel/target по стандартам раскрытия рекламных ссылок.
    """
    def _sub(match):
        scheme, encoded = match.group("scheme"), match.group("target")
        target_url = urllib.parse.unquote(encoded)
        base = aff_networks.get(scheme)
        if not base:
            return match.group(0)
        aff_url = base.format(url=urllib.parse.quote(target_url, safe=""))
        return f'href="{aff_url}" target="_blank" rel="nofollow sponsored noopener"'

    pattern = re.compile(r'href="(?P<scheme>ozon|wb)://(?P<target>[^"]+)"')
    return pattern.sub(_sub, html)


def render_article(fm, body_md, aff_networks):
    html_body = md.markdown(body_md, extensions=["extra"])
    html_body = replace_affiliate_links(html_body, aff_networks)
    return html_body


def slugify_check(fm, fname):
    slug = fm.get("slug") or os.path.splitext(fname)[0]
    return slug


def render_page(template, **kwargs):
    return template.safe_substitute(**kwargs)


WORDS_RE = re.compile(r"\w+", re.UNICODE)
TAGS_RE = re.compile(r"<[^>]+>")


def reading_time_minutes(html_body):
    text = TAGS_RE.sub(" ", html_body)
    word_count = len(WORDS_RE.findall(text))
    minutes = max(1, round(word_count / 200))
    return minutes


def pick_related(art, all_articles, count=3):
    same_category = [a for a in all_articles
                      if a["slug"] != art["slug"] and a["category"] == art["category"]]
    others = [a for a in all_articles
              if a["slug"] != art["slug"] and a["category"] != art["category"]]
    return (same_category + others)[:count]


def card_html(art):
    search_blob = f'{art["title"]} {art["description"]} {art["category"]}'.lower()
    return (
        f'<article class="card" data-category="{art["category"]}" '
        f'data-search="{search_blob}">'
        f'<span class="tag">{art["category"]}</span>'
        f'<h3><a href="{art["slug"]}/">{art["title"]}</a></h3>'
        f'<p>{art["description"]}</p>'
        f'<div class="card-footer">'
        f'<span>⏱ {art["reading_time"]} мин чтения</span>'
        f'<a class="read-more" href="{art["slug"]}/">Смотреть идеи →</a>'
        f'</div>'
        f'</article>'
    )


def build():
    cfg = load_config()
    with open(TEMPLATE_PATH, encoding="utf-8") as f:
        template = Template(f.read())

    os.makedirs(OUT_DIR, exist_ok=True)
    # copy static
    static_out = os.path.join(OUT_DIR, "static")
    os.makedirs(static_out, exist_ok=True)
    for fname in os.listdir(STATIC_DIR):
        with open(os.path.join(STATIC_DIR, fname), "rb") as src, \
             open(os.path.join(static_out, fname), "wb") as dst:
            dst.write(src.read())

    verification_tags = ""
    if cfg.get("yandex_verification"):
        verification_tags += f'<meta name="yandex-verification" content="{cfg["yandex_verification"]}">\n'
    if cfg.get("google_verification"):
        verification_tags += f'<meta name="google-site-verification" content="{cfg["google_verification"]}">\n'
    if cfg.get("mitgo_verification"):
        verification_tags += f'<meta name="mitgo-verification" content="{cfg["mitgo_verification"]}">\n'

    articles = []
    if os.path.isdir(CONTENT_DIR):
        for fname in sorted(os.listdir(CONTENT_DIR)):
            if not fname.endswith(".md"):
                continue
            with open(os.path.join(CONTENT_DIR, fname), encoding="utf-8") as f:
                raw = f.read()
            fm, body_md = parse_front_matter(raw)
            slug = slugify_check(fm, fname)
            html_body = render_article(fm, body_md, cfg["aff_networks"])
            articles.append({
                "slug": slug,
                "title": fm.get("title", slug),
                "description": fm.get("description", cfg["description"]),
                "category": fm.get("category", ""),
                "date": fm.get("date", ""),
                "html": html_body,
                "reading_time": reading_time_minutes(html_body),
            })

    articles.sort(key=lambda a: a["date"], reverse=True)

    year = datetime.now(timezone.utc).year

    # article pages
    for art in articles:
        page_dir = os.path.join(OUT_DIR, art["slug"])
        os.makedirs(page_dir, exist_ok=True)
        canonical = f'{cfg["site_url"].rstrip("/")}/{art["slug"]}/'

        related = pick_related(art, articles)
        related_html = ""
        if related:
            related_cards = "".join(card_html(r) for r in related)
            related_html = (
                f'<section class="related"><h2>Похожие подборки</h2>'
                f'<div class="card-grid small">{related_cards}</div></section>'
            )

        breadcrumbs_html = (
            f'<nav class="breadcrumbs"><a href="../">Главная</a> · '
            f'<span>{art["category"]}</span></nav>'
        )

        content_html = (
            f'<div class="article-wrap">'
            f'{breadcrumbs_html}'
            f'<h1>{art["title"]}</h1>'
            f'<p class="meta">{art["date"]} · <span class="tag">{art["category"]}</span> '
            f'· ⏱ {art["reading_time"]} мин чтения</p>'
            f'{art["html"]}'
            f'{related_html}'
            f'</div>'
        )
        page = render_page(
            template,
            page_title=f'{art["title"]} — {cfg["site_name"]}',
            page_description=art["description"],
            canonical_url=canonical,
            verification_tags=verification_tags,
            root_prefix="..",
            site_name=cfg["site_name"],
            content=content_html,
            year=year,
        )
        with open(os.path.join(page_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(page)

    # homepage
    categories = sorted({a["category"] for a in articles if a["category"]})
    pills = ['<button class="filter-pill active" data-filter="all" type="button">Все</button>']
    for cat in categories:
        pills.append(f'<button class="filter-pill" data-filter="{cat}" type="button">{cat}</button>')

    cards = [card_html(art) for art in articles]

    home_content = (
        f'<section class="hero">'
        f'<h1>{cfg["site_name"]}</h1>'
        f'<p class="intro">{cfg["description"]}</p>'
        f'<div class="hero-stats"><span>🎁 {len(articles)} подборок идей</span>'
        f'<span>🔄 Обновляется каждую неделю</span></div>'
        f'</section>'
        f'<div class="toolbar">'
        f'<div class="search-box"><input type="text" placeholder="Найти подборку идей..." aria-label="Поиск"></div>'
        f'<div class="filter-pills">{"".join(pills)}</div>'
        f'</div>'
        f'<div class="card-grid" data-filterable>{"".join(cards)}</div>'
        f'<p class="no-results">Ничего не найдено — попробуйте другой запрос или категорию.</p>'
    )
    home_page = render_page(
        template,
        page_title=f'{cfg["site_name"]} — {cfg["description"]}',
        page_description=cfg["description"],
        canonical_url=cfg["site_url"] + "/",
        verification_tags=verification_tags,
        root_prefix=".",
        site_name=cfg["site_name"],
        content=home_content,
        year=year,
    )
    with open(os.path.join(OUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(home_page)

    # about page
    about_dir = os.path.join(OUT_DIR, "o-sayte")
    os.makedirs(about_dir, exist_ok=True)
    about_content = (
        '<div class="article-wrap">'
        '<nav class="breadcrumbs"><a href="../">Главная</a> · <span>О сайте</span></nav>'
        "<h1>О сайте</h1>"
        f"<p>{cfg['site_name']} — сайт с подборками идей подарков на разные праздники, "
        "бюджеты и типы получателей. Мы не продаём товары напрямую: ссылки в статьях "
        "ведут на маркетплейсы (Ozon, Wildberries и другие), где вы можете сравнить цены, "
        "отзывы и сделать покупку.</p>"
        "<p>Сайт может получать партнёрское вознаграждение с покупок, совершённых по "
        "ссылкам из наших статей. Это никак не влияет на итоговую цену товара для покупателя "
        "и не влияет на то, какие идеи мы рекомендуем.</p>"
        '</div>'
    )
    about_page = render_page(
        template,
        page_title=f'О сайте — {cfg["site_name"]}',
        page_description="Информация о сайте и партнёрских ссылках",
        canonical_url=cfg["site_url"] + "/o-sayte/",
        verification_tags=verification_tags,
        root_prefix="..",
        site_name=cfg["site_name"],
        content=about_content,
        year=year,
    )
    with open(os.path.join(about_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(about_page)

    # sitemap.xml
    urls = [cfg["site_url"] + "/", cfg["site_url"] + "/o-sayte/"] + \
           [f'{cfg["site_url"]}/{a["slug"]}/' for a in articles]
    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>',
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        sitemap.append(f"<url><loc>{u}</loc></url>")
    sitemap.append("</urlset>")
    with open(os.path.join(OUT_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write("\n".join(sitemap))

    # robots.txt
    with open(os.path.join(OUT_DIR, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(f"User-agent: *\nAllow: /\nSitemap: {cfg['site_url']}/sitemap.xml\n")

    # rss.xml (простая лента)
    rss_items = []
    for a in articles[:20]:
        rss_items.append(
            f"<item><title>{a['title']}</title>"
            f"<link>{cfg['site_url']}/{a['slug']}/</link>"
            f"<description>{a['description']}</description></item>"
        )
    rss = (
        '<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel>'
        f"<title>{cfg['site_name']}</title><link>{cfg['site_url']}</link>"
        f"<description>{cfg['description']}</description>"
        + "".join(rss_items) + "</channel></rss>"
    )
    with open(os.path.join(OUT_DIR, "rss.xml"), "w", encoding="utf-8") as f:
        f.write(rss)

    print(f"Собрано статей: {len(articles)}. Готовый сайт: {OUT_DIR}")


if __name__ == "__main__":
    build()
