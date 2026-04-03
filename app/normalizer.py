from __future__ import annotations

import re
from typing import Iterable

from .models import ContentBlock


_WS_RE = re.compile(r"[ \t]+")
_TRIPLE_NL_RE = re.compile(r"\n{3,}")
_SOFT_HYPHEN_RE = re.compile("\u00ad")


def normalize_text(value: str) -> str:
    text = value.replace("\r\n", "\n").replace("\r", "\n")
    text = _SOFT_HYPHEN_RE.sub("", text)
    text = _WS_RE.sub(" ", text)
    text = "\n".join(line.strip() for line in text.split("\n"))
    text = _TRIPLE_NL_RE.sub("\n\n", text)
    return text.strip()


def render_markdown(block: ContentBlock) -> str:
    text = normalize_text(block.text)
    if not text:
        return ""

    if block.type == "heading":
        return f"## {text}"
    if block.type == "table":
        return text
    if block.type == "json":
        return f"```json\n{text}\n```"
    if block.type == "code":
        return f"```\n{text}\n```"
    if block.type == "page":
        page = block.metadata.get("page")
        return f"## Page {page}\n\n{text}" if page else text
    if block.type == "slide":
        slide = block.metadata.get("slide")
        return f"## Slide {slide}\n\n{text}" if slide else text
    if block.type == "sheet":
        sheet = block.metadata.get("sheet")
        return f"## Sheet: {sheet}\n\n{text}" if sheet else text
    return text


def join_block_texts(blocks: Iterable[ContentBlock]) -> str:
    parts = [render_markdown(block) for block in blocks if render_markdown(block)]
    return "\n\n".join(parts)


def markdown_table(rows: list[list[object]]) -> str:
    if not rows:
        return ""
    width = max(len(row) for row in rows)
    normalized_rows = []
    for row in rows:
        normalized_rows.append([(str(cell).strip() if cell is not None else "") for cell in row] + [""] * (width - len(row)))
    header = normalized_rows[0]
    separator = ["---"] * width
    body = normalized_rows[1:] or []
    all_rows = [header, separator, *body]
    return "\n".join("| " + " | ".join(row) + " |" for row in all_rows)
