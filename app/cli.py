from __future__ import annotations

import argparse
from pathlib import Path

from .extractors import extract


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert files into normalized Markdown for RAG ingestion.")
    parser.add_argument("paths", nargs="+", help="Files to convert")
    parser.add_argument("--out", type=Path, default=Path("processed"), help="Output directory")
    args = parser.parse_args()

    out_dir = args.out
    out_dir.mkdir(parents=True, exist_ok=True)

    for raw_path in args.paths:
        path = Path(raw_path)
        doc = extract(path)
        out_path = out_dir / f"{path.stem}.md"
        out_path.write_text(doc.text, encoding="utf-8")
        print(f"Saved: {out_path}")


if __name__ == "__main__":
    main()
