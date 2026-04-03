from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


BlockType = Literal[
    "heading",
    "paragraph",
    "table",
    "list",
    "code",
    "json",
    "slide",
    "sheet",
    "page",
    "text",
]


class ContentBlock(BaseModel):
    type: BlockType
    text: str
    order: int = Field(ge=0)
    metadata: dict[str, Any] = Field(default_factory=dict)


class NormalizedDocument(BaseModel):
    source_name: str
    source_path: str | None = None
    file_type: str
    title: str | None = None
    text: str
    content_blocks: list[ContentBlock] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
