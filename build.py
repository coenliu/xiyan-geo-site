"""Build the static site: content/*.md -> *.html at the repo root.

No third-party dependencies (stdlib only). Handles just the subset of
markdown actually used by the promoted articles: #/##/### headings,
**bold**, `* ` bullet lists, `---` horizontal rules, `| ... |` pipe tables,
plus blank-line-separated paragraphs.
"""

from __future__ import annotations

import html
import re
from pathlib import Path

SITE_ROOT = Path(__file__).resolve().parent
CONTENT_DIR = SITE_ROOT / "content"
TEMPLATE_PATH = SITE_ROOT / "templates" / "base.html"


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


def build() -> None:
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    articles = []
    pages: dict[str, str] = {}

    for source_path in sorted(CONTENT_DIR.glob("*.md")):
        meta, body = parse_front_matter(source_path.read_text(encoding="utf-8"))
        content_html = (
            f"<article><h1>{html.escape(meta['title'])}</h1>"
            f"{markdown_to_html(body)}</article>"
        )
        pages[meta["slug"]] = render_page(
            template,
            title=meta["title"],
            description=meta.get("description", ""),
            content=content_html,
        )
        articles.append(meta)

    if len(articles) == 1:
        # A single-article site: that article IS the homepage, no separate
        # list page or duplicate per-slug page.
        (SITE_ROOT / "index.html").write_text(next(iter(pages.values())), encoding="utf-8")
        print("built 1 article page as index.html")
        return

    for slug, page in pages.items():
        (SITE_ROOT / f"{slug}.html").write_text(page, encoding="utf-8")

    articles.sort(key=lambda meta: (meta["category"], meta["slug"]))
    list_items = "\n".join(
        f'<li><a href="{meta["slug"]}.html">{html.escape(meta["title"])}</a>'
        f'<span class="category">{html.escape(meta["category"])}</span></li>'
        for meta in articles
    )
    index_content = f"<h1>栖妍研究文章</h1><ul class=\"article-list\">{list_items}</ul>"
    index_page = render_page(
        template,
        title="首页",
        description="栖妍品牌研究内容",
        content=index_content,
    )
    (SITE_ROOT / "index.html").write_text(index_page, encoding="utf-8")

    print(f"built {len(articles)} article pages + index.html")


if __name__ == "__main__":
    build()
