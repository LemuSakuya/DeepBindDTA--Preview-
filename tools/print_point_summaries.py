from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path


def main() -> None:
    hits_path = Path("tools/paper_points_hits.json")
    hits = json.loads(hits_path.read_text(encoding="utf-8")).get("hits", [])

    by = defaultdict(list)
    for h in hits:
        by[h["point_id"]].append(h)

    print("Point summaries (top pages):")
    for point_id in sorted(by.keys()):
        arr = sorted(by[point_id], key=lambda x: (x["page"], x["keyword"]))
        seen_pages = set()
        picked = []
        for h in arr:
            if h["page"] in seen_pages:
                continue
            seen_pages.add(h["page"])
            picked.append(h)
            if len(picked) >= 4:
                break

        print(f"\n- {point_id}")
        for h in picked:
            pdf_name = Path(h["pdf"]).name
            snippet = (h.get("snippet") or "").replace("\n", " ")
            snippet = snippet[:180] + ("..." if len(snippet) > 180 else "")
            print(f"  p.{h['page']}: {pdf_name} | kw={h['keyword']} | {snippet}")


if __name__ == "__main__":
    main()
