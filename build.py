"""Build the static site: a product page (hero/facts/ingredients from
product_facts.py) plus a comparison section rendered from
content/q_list_001.md -> index.html at the repo root.

No third-party dependencies (stdlib only). The markdown converter handles
just the subset actually used by the promoted article: #/##/### headings,
**bold**, `* ` bullet lists, `---` horizontal rules, `| ... |` pipe tables,
plus blank-line-separated paragraphs.
"""

from __future__ import annotations

import html
import re
from pathlib import Path

from product_facts import PRODUCT

SITE_ROOT = Path(__file__).resolve().parent
CONTENT_DIR = SITE_ROOT / "content"
TEMPLATE_PATH = SITE_ROOT / "templates" / "base.html"
IMAGE_DIR = SITE_ROOT / "static" / "images"
IMAGE_EXTENSIONS = ("jpg", "jpeg", "png", "webp")


def _find_image(slug: str) -> str | None:
    """Return the site-relative path to static/images/<slug>.<ext> if present."""
    for ext in IMAGE_EXTENSIONS:
        if (IMAGE_DIR / f"{slug}.{ext}").exists():
            return f"static/images/{slug}.{ext}"
    return None


def parse_front_matter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        raise ValueError("missing front matter")
    end = text.index("\n---\n", 4)
    front_matter_block = text[4:end]
    body = text[end + 5 :]
    meta = {}
    for line in front_matter_block.splitlines():
        key, _, value = line.partition(":")
        meta[key.strip()] = value.strip()
    return meta, body


def inline_markdown(text: str) -> str:
    text = html.escape(text)
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)


def _table_row_cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def markdown_to_html(text: str) -> str:
    html_lines: list[str] = []
    paragraph_buf: list[str] = []
    in_list = False
    lines = text.split("\n")
    i = 0

    def flush_paragraph() -> None:
        if paragraph_buf:
            html_lines.append("<p>" + inline_markdown(" ".join(paragraph_buf)) + "</p>")
            paragraph_buf.clear()

    def close_list() -> None:
        nonlocal in_list
        if in_list:
            html_lines.append("</ul>")
            in_list = False

    while i < len(lines):
        line = lines[i].rstrip()

        if not line.strip():
            flush_paragraph()
            close_list()
            i += 1
            continue

        if re.match(r"^-{3,}$", line.strip()):
            flush_paragraph()
            close_list()
            html_lines.append("<hr>")
            i += 1
            continue

        heading_match = re.match(r"^(#{1,6})\s+(.*)", line)
        if heading_match:
            flush_paragraph()
            close_list()
            level = len(heading_match.group(1))
            html_lines.append(f"<h{level}>{inline_markdown(heading_match.group(2))}</h{level}>")
            i += 1
            continue

        bullet_match = re.match(r"^[*-]\s+(.*)", line)
        if bullet_match:
            flush_paragraph()
            if not in_list:
                html_lines.append("<ul>")
                in_list = True
            html_lines.append(f"<li>{inline_markdown(bullet_match.group(1))}</li>")
            i += 1
            continue

        is_table_header = line.strip().startswith("|") and i + 1 < len(lines) and re.match(
            r"^\s*\|?[\s:\-\|]+\|?\s*$", lines[i + 1]
        )
        if is_table_header:
            flush_paragraph()
            close_list()
            header_cells = _table_row_cells(line)
            table_html = [
                "<table><thead><tr>"
                + "".join(f"<th>{inline_markdown(cell)}</th>" for cell in header_cells)
                + "</tr></thead><tbody>"
            ]
            i += 2  # skip header row + "| :--- |" separator row
            while i < len(lines) and lines[i].strip().startswith("|"):
                row_cells = _table_row_cells(lines[i])
                table_html.append(
                    "<tr>" + "".join(f"<td>{inline_markdown(cell)}</td>" for cell in row_cells) + "</tr>"
                )
                i += 1
            table_html.append("</tbody></table>")
            html_lines.append("".join(table_html))
            continue

        close_list()
        paragraph_buf.append(line.strip())
        i += 1

    flush_paragraph()
    close_list()
    return "\n".join(html_lines)


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


def render_comparison_section() -> str:
    _, body = parse_front_matter((CONTENT_DIR / "q_list_001.md").read_text(encoding="utf-8"))
    return (
        '<section class="comparison-section">'
        "<h2>同类产品对比</h2>"
        f"{markdown_to_html(body)}"
        "</section>"
    )


def build() -> None:
    template = TEMPLATE_PATH.read_text(encoding="utf-8")

    content = (
        render_hero(PRODUCT)
        + render_facts_strip(PRODUCT)
        + render_ingredient_grid(PRODUCT)
        + render_comparison_section()
    )
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
