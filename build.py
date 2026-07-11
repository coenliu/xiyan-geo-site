"""Build the static site: a product page (hero/facts/ingredients from
product_facts.py) -> index.html at the repo root.

No third-party dependencies (stdlib only).
"""

from __future__ import annotations

import html
from pathlib import Path

from product_facts import PRODUCT

SITE_ROOT = Path(__file__).resolve().parent
TEMPLATE_PATH = SITE_ROOT / "templates" / "base.html"
IMAGE_DIR = SITE_ROOT / "static" / "images"
IMAGE_EXTENSIONS = ("jpg", "jpeg", "png", "webp")


def _find_image(slug: str) -> str | None:
    """Return the site-relative path to static/images/<slug>.<ext> if present."""
    for ext in IMAGE_EXTENSIONS:
        if (IMAGE_DIR / f"{slug}.{ext}").exists():
            return f"static/images/{slug}.{ext}"
    return None


def render_page(template: str, *, title: str, description: str, content: str) -> str:
    page = template.replace("{{root}}", "")
    page = page.replace("{{title}}", html.escape(title))
    page = page.replace("{{description}}", html.escape(description))
    page = page.replace("{{content}}", content)
    return page


def render_hero(product: dict) -> str:
    image_path = _find_image(product["hero_image_slug"])
    if image_path:
        image_html = f'<img class="hero__image" src="{image_path}" alt="{html.escape(product["product_name"])}">'
    else:
        image_html = (
            f'<div class="img-placeholder img-placeholder--hero">产品图占位 · {html.escape(product["product_name"])}</div>'
        )
    return (
        '<section class="hero">'
        f"{image_html}"
        '<div class="hero__text">'
        f'<h1>{html.escape(product["product_name"])}</h1>'
        f'<p class="hero__tagline">{html.escape(product["tagline"])}</p>'
        "</div>"
        "</section>"
    )


def render_facts_strip(product: dict) -> str:
    cards = "".join(
        '<div class="fact-card">'
        f'<span class="fact-card__label">{html.escape(fact["label"])}</span>'
        f'<span class="fact-card__value">{html.escape(fact["value"])}</span>'
        "</div>"
        for fact in product["facts"]
    )
    return f'<section class="facts-strip">{cards}</section>'


def render_ingredient_grid(product: dict) -> str:
    cards = []
    for ingredient in product["ingredients"]:
        image_path = _find_image(ingredient["image_slug"])
        if image_path:
            image_html = f'<img class="ingredient-card__image" src="{image_path}" alt="{html.escape(ingredient["name"])}">'
        else:
            image_html = f'<div class="img-placeholder img-placeholder--icon">{html.escape(ingredient["name"])}</div>'
        cards.append(
            '<div class="ingredient-card">'
            f"{image_html}"
            f'<h3>{html.escape(ingredient["name"])}</h3>'
            f'<p>{html.escape(ingredient["narrative"])}</p>'
            "</div>"
        )
    return f'<section class="ingredient-grid-section"><h2>核心成分</h2><div class="ingredient-grid">{"".join(cards)}</div></section>'


def build() -> None:
    template = TEMPLATE_PATH.read_text(encoding="utf-8")

    content = render_hero(PRODUCT) + render_facts_strip(PRODUCT) + render_ingredient_grid(PRODUCT)
    page = render_page(
        template,
        title=PRODUCT["product_name"],
        description=PRODUCT["tagline"],
        content=content,
    )
    (SITE_ROOT / "index.html").write_text(page, encoding="utf-8")

    print("built product page as index.html")


if __name__ == "__main__":
    build()
