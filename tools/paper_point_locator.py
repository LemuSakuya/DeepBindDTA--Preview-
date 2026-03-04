from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from pypdf import PdfReader


@dataclass(frozen=True)
class Hit:
    pdf: str
    point_id: str
    keyword: str
    page: int
    snippet: str


def _normalize_ws(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def extract_pages(pdf_path: Path) -> list[str]:
    reader = PdfReader(str(pdf_path))
    pages: list[str] = []
    for page in reader.pages:
        txt = page.extract_text() or ""
        pages.append(txt)
    return pages


def find_hits(pdf_path: Path, point_id: str, keywords: Iterable[str], max_hits: int = 8) -> list[Hit]:
    pages = extract_pages(pdf_path)
    hits: list[Hit] = []
    for keyword in keywords:
        if not keyword:
            continue
        pattern = re.compile(re.escape(keyword), re.IGNORECASE)
        for idx, txt in enumerate(pages, start=1):
            if not txt:
                continue
            m = pattern.search(txt)
            if not m:
                continue
            start = max(0, m.start() - 140)
            end = min(len(txt), m.end() + 200)
            snippet = _normalize_ws(txt[start:end])
            hits.append(Hit(pdf=str(pdf_path), point_id=point_id, keyword=keyword, page=idx, snippet=snippet))
            if len([h for h in hits if h.keyword == keyword]) >= 2:
                break
        if len(hits) >= max_hits:
            break
    return hits


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--spec", required=True, help="JSON spec file: {points:[{id, pdf, keywords:[...]}]} ")
    parser.add_argument("--out", required=True, help="Output JSON path")
    args = parser.parse_args()

    spec_path = Path(args.spec)
    out_path = Path(args.out)

    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    points = spec.get("points", [])

    all_hits: list[dict] = []
    for p in points:
        point_id = p["id"]
        pdf = Path(p["pdf"])
        keywords = p.get("keywords", [])
        if not pdf.exists():
            continue
        hits = find_hits(pdf, point_id, keywords)
        for h in hits:
            all_hits.append(
                {
                    "pdf": h.pdf,
                    "point_id": h.point_id,
                    "keyword": h.keyword,
                    "page": h.page,
                    "snippet": h.snippet,
                }
            )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps({"hits": all_hits}, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
