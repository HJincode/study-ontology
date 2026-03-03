"""
선택적 클렌징: pub_date 정규화 (YYYY 또는 YYYY-MM), title/abstract 앞뒤 공백 제거.
입력: output/ 아래 PubMed JSON (단일 카테고리 또는 분배 모드 출력, 예: pubmed_distributed_200.json).
출력: output/cleaned/ 아래에 <입력 stem>_cleansed.json (기존 파일 있으면 _cleansed_1, _cleansed_2 … 생성, 원본 덮어쓰지 않음).
분배 모드 JSON의 category 필드는 유지됨.
"""

import argparse
import json
import re
import sys
from pathlib import Path

MONTH = {
    "Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "Jun": "06",
    "Jul": "07", "Aug": "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12",
}


def normalize_pub_date(raw: str) -> str:
    """PubMed pub_date를 YYYY 또는 YYYY-MM으로 정규화."""
    if not raw or not isinstance(raw, str):
        return raw
    s = raw.strip()
    # YYYY only
    if re.match(r"^\d{4}$", s):
        return s
    # YYYYMon or YYYYMonDD
    m = re.match(r"^(\d{4})(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\d*$", s, re.I)
    if m:
        year, mon = m.group(1), m.group(2)
        return f"{year}-{MONTH.get(mon.capitalize(), mon)}"
    return s


def cleanse(in_path: Path, out_path: Path) -> None:
    with open(in_path, encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError("Expected a JSON array of article objects")
    for item in data:
        if not isinstance(item, dict):
            continue
        if "pub_date" in item and item["pub_date"]:
            item["pub_date"] = normalize_pub_date(item["pub_date"])
        if "title" in item and isinstance(item["title"], str):
            item["title"] = item["title"].strip()
        if "abstract" in item and isinstance(item["abstract"], str):
            item["abstract"] = item["abstract"].strip()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Cleansed {len(data)} records -> {out_path}")


if __name__ == "__main__":
    base = Path(__file__).resolve().parent.parent
    output_dir = base / "output"
    default_input_candidates = [
        output_dir / "pubmed_protein_structure_enzyme_10.json",
        output_dir / "pubmed_distributed_200.json",
        output_dir / "pubmed_distributed_100.json",
    ]
    default_input = next((p for p in default_input_candidates if p.exists()), default_input_candidates[0])

    parser = argparse.ArgumentParser(
        description="PubMed JSON 클렌징: pub_date 정규화, title/abstract 공백 제거. 분배 모드(pubmed_distributed_*.json) 지원."
    )
    parser.add_argument(
        "input",
        nargs="?",
        default=str(default_input),
        help="입력 JSON 경로 (기본: output 내 pubmed_*.json 중 존재하는 첫 파일)",
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default=None,
        help="출력 JSON 경로 (미지정 시 output/cleaned/ 아래 stem_cleansed.json)",
    )
    args = parser.parse_args()

    in_file = Path(args.input)
    if not in_file.is_absolute():
        cand = base / "output" / in_file.name
        if cand.exists():
            in_file = cand
    if not in_file.exists():
        print(f"Not found: {in_file}", file=sys.stderr)
        sys.exit(1)

    if args.output:
        out_file = Path(args.output)
    else:
        cleaned_dir = output_dir / "cleaned"
        cleaned_dir.mkdir(parents=True, exist_ok=True)
        out_file = cleaned_dir / f"{in_file.stem}_cleansed{in_file.suffix}"

    if out_file.exists():
        stem, suffix = out_file.stem, out_file.suffix
        out_dir = out_file.parent
        n = 1
        while out_file.exists():
            out_file = out_dir / f"{stem}_{n}{suffix}"
            n += 1

    cleanse(in_file, out_file)
