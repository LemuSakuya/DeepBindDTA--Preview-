from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

from pypdf import PdfReader


# ──────────────────────────────────────────────
# helpers
# ──────────────────────────────────────────────

SECTION_PAT = re.compile(
    r"(?m)^\s*"
    r"("
    r"(?:\d{1,2}(?:\.\d{1,2}){0,2})"   # e.g. 1  /  2.1  /  3.1.2
    r"\s+"
    r"[A-Z][A-Za-z\s\-:,()]{2,60}"      # title words
    r")"
    r"\s*$"
)

ABSTRACT_PAT = re.compile(r"\bABSTRACT\b", re.IGNORECASE)


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def extract_pages(pdf_path: Path) -> list[str]:
    reader = PdfReader(str(pdf_path))
    pages: list[str] = []
    for page in reader.pages:
        txt = page.extract_text() or ""
        pages.append(txt)
    return pages


def build_section_map(pages: list[str]) -> list[tuple[int, int, str]]:
    """
    Returns list of (page_1indexed, offset_in_page, section_title) sorted by page.
    Also includes ABSTRACT/INTRODUCTION detected roughly.
    """
    sections: list[tuple[int, int, str]] = []
    for page_idx, txt in enumerate(pages, start=1):
        # standard numbered sections
        for m in SECTION_PAT.finditer(txt):
            title = _normalize(m.group(1))
            sections.append((page_idx, m.start(), title))
        # abstract – usually first page unnumbered
        if page_idx <= 2:
            m = ABSTRACT_PAT.search(txt)
            if m:
                sections.append((page_idx, m.start(), "Abstract"))
    sections.sort(key=lambda x: (x[0], x[1]))
    return sections


def find_section_for_page(sections: list[tuple[int, int, str]], page: int) -> str:
    """Find the latest section that starts at or before `page`."""
    result = "—"
    for (p, _, title) in sections:
        if p <= page:
            result = title
        else:
            break
    return result


def find_hits_with_section(
    pdf_path: Path,
    point_id: str,
    keywords: list[str],
    sections: list[tuple[int, int, str]],
    pages: list[str],
    max_per_keyword: int = 2,
) -> list[dict]:
    hits: list[dict] = []
    for keyword in keywords:
        if not keyword:
            continue
        pat = re.compile(re.escape(keyword), re.IGNORECASE)
        count = 0
        for idx, txt in enumerate(pages, start=1):
            m = pat.search(txt)
            if not m:
                continue
            start = max(0, m.start() - 120)
            end = min(len(txt), m.end() + 180)
            snippet = _normalize(txt[start:end])
            sec = find_section_for_page(sections, idx)
            hits.append(
                {
                    "point_id": point_id,
                    "pdf_short": pdf_path.name[:80],
                    "keyword": keyword,
                    "page": idx,
                    "section": sec,
                    "snippet": snippet,
                }
            )
            count += 1
            if count >= max_per_keyword:
                break
    return hits


def deduplicate_by_page(hits: list[dict], max_pages: int = 4) -> list[dict]:
    seen: set[int] = set()
    out: list[dict] = []
    for h in sorted(hits, key=lambda x: (x["page"], x["keyword"])):
        if h["page"] in seen:
            continue
        seen.add(h["page"])
        out.append(h)
        if len(out) >= max_pages:
            break
    return out


def main() -> None:
    spec_path = Path("tools/paper_points_spec.json")
    out_md = Path("papers_keypoints_mapping.md")

    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    points = spec.get("points", [])

    # group points by PDF so we only open each PDF once
    pdf_to_points: dict[str, list[dict]] = defaultdict(list)
    for p in points:
        pdf_to_points[p["pdf"]].append(p)

    # collect all results
    all_results: list[dict] = []     # {point_id, pdf_short, entries:[{page, section, keyword, snippet}]}
    pdf_sections_cache: dict[str, list[tuple[int, int, str]]] = {}
    pdf_pages_cache: dict[str, list[str]] = {}

    for pdf_str, pts in pdf_to_points.items():
        pdf_path = Path(pdf_str)
        if not pdf_path.exists():
            print(f"[SKIP] {pdf_str}")
            continue
        pages = extract_pages(pdf_path)
        sections = build_section_map(pages)
        pdf_pages_cache[pdf_str] = pages
        pdf_sections_cache[pdf_str] = sections

        for p in pts:
            hits = find_hits_with_section(
                pdf_path, p["id"], p.get("keywords", []), sections, pages
            )
            deduped = deduplicate_by_page(hits)
            all_results.append(
                {
                    "point_id": p["id"],
                    "pdf_short": pdf_path.name[:90],
                    "entries": deduped,
                }
            )

    # ── render markdown ──────────────────────────────
    lines: list[str] = []
    lines.append("# 5 篇论文要点 → 对应页码与章节（Section-level）\n")
    lines.append(
        "> 本文档由 `tools/paper_section_locator.py` 自动生成。\n"
        "> 章节标题从 PDF 页面文本中用正则抽取（`\\d. Title` 模式），若 PDF 排版不规则可能有偏差。\n"
    )

    # group by pdf_short to organize output
    pdf_order = []
    for r in all_results:
        if r["pdf_short"] not in pdf_order:
            pdf_order.append(r["pdf_short"])

    for pdf_short in pdf_order:
        pts_for_pdf = [r for r in all_results if r["pdf_short"] == pdf_short]
        if not pts_for_pdf:
            continue
        lines.append(f"\n---\n\n## {pdf_short}\n")
        for rec in pts_for_pdf:
            lines.append(f"\n### 要点：{rec['point_id']}\n")
            if not rec["entries"]:
                lines.append("_（未找到关键词命中，请检查 PDF 文本提取）_\n")
                continue
            lines.append("| 页码 | 所在章节（推断） | 关键词 | 上下文片段 |")
            lines.append("|------|-----------------|--------|------------|")
            for e in rec["entries"]:
                snip = e["snippet"].replace("|", "｜")[:180]
                sec = e["section"].replace("|", "｜")
                lines.append(
                    f"| p.{e['page']} | {sec} | `{e['keyword']}` | {snip}… |"
                )
        lines.append("")

    out_md.write_text("\n".join(lines), encoding="utf-8")
    print(f"Written → {out_md}  ({len(all_results)} points, {sum(len(r['entries']) for r in all_results)} hits)")


if __name__ == "__main__":
    main()
