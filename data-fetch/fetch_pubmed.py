"""
PubMed E-utilities 연동: 검색어로 논문 ID 조회 후 상세 메타데이터 수집.
- esearch: 검색어로 PMID 목록 조회 (최대 FETCH_LIMIT건)
- efetch: PMID별 메타데이터(제목, 초록, 저자, 저널, MeSH 등) 조회 후 JSON 저장

참고: db=pubmed 는 논문 "원문(본문)" 이 아닌 메타데이터+초록만 제공합니다.
      전체 원문이 필요하면 PMC(db=pmc) 를 사용해야 합니다.
"""

import json
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path

# 프로젝트 루트나 다른 경로에서 실행해도 config 를 찾을 수 있도록 data-fetch 를 path 에 추가
_script_dir = Path(__file__).resolve().parent
if str(_script_dir) not in sys.path:
    sys.path.insert(0, str(_script_dir))

import requests

from config import (
    FETCH_LIMIT,
    get_query_string,
    CATEGORIES,
    INTERMEDIATE_RECOMMENDED,
    ADVANCED_RECOMMENDED,
    FETCH_CATEGORIES,
)

BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
# API 정책: 초당 3회 미만 권장
REQUEST_DELAY_SEC = 0.34


def esearch(query: str, retmax: int = 10) -> list[str]:
    """PubMed esearch: 검색어로 PMID 리스트 반환."""
    print(f"[esearch] 요청 중 (retmax={retmax})...", flush=True)
    url = f"{BASE_URL}/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": retmax,
        "retmode": "json",
        "sort": "relevance",
    }
    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    id_list = data.get("esearchresult", {}).get("idlist", [])
    print(f"[esearch] 완료: PMID {len(id_list)}건", flush=True)
    return id_list


def efetch(id_list: list[str]) -> str:
    """PubMed efetch: PMID 목록에 대해 메타데이터 XML 반환 (원문 본문 아님)."""
    if not id_list:
        return ""
    print(f"[efetch] 요청 중 (PMID {len(id_list)}건)...", flush=True)
    url = f"{BASE_URL}/efetch.fcgi"
    params = {
        "db": "pubmed",
        "id": ",".join(id_list),
        "retmode": "xml",
    }
    resp = requests.get(url, params=params, timeout=60)
    resp.raise_for_status()
    print("[efetch] 완료: XML 수신, 파싱 중...", flush=True)
    return resp.text


def _text(el: ET.Element | None) -> str:
    if el is None:
        return ""
    return (el.text or "").strip()


def _all_text(el: ET.Element | None) -> str:
    if el is None:
        return ""
    return "".join(el.itertext()).strip()


def parse_pubmed_xml(xml_str: str) -> list[dict]:
    """efetch XML 응답을 파싱해 논문별 메타데이터 리스트로 변환."""
    root = ET.fromstring(xml_str)

    def local_tag(e: ET.Element) -> str:
        return e.tag.split("}")[-1] if "}" in e.tag else e.tag

    articles = [e for e in root.iter() if local_tag(e) == "PubmedArticle"]
    result = []
    for article in articles:
        def find(name: str) -> ET.Element | None:
            for e in article.iter():
                if local_tag(e) == name:
                    return e
            return None

        def find_all(name: str) -> list[ET.Element]:
            return [e for e in article.iter() if local_tag(e) == name]

        pmid_el = find("PMID")
        pmid = _text(pmid_el) if pmid_el is not None else ""
        art_el = find("Article")

        title_el = find("ArticleTitle")
        title = _all_text(title_el) if title_el is not None else ""

        abstract_el = find("AbstractText")
        abstract = _all_text(abstract_el) if abstract_el is not None else ""
        abstract_blocks = find_all("AbstractText")
        if abstract_blocks:
            parts = []
            for ab in abstract_blocks:
                parts.append(_all_text(ab))
            abstract = " ".join(parts) if len(parts) > 1 else (parts[0] if parts else "")

        authors = []
        for author_el in find_all("Author"):
            last, first = "", ""
            for c in author_el:
                tag = c.tag.split("}")[-1] if "}" in c.tag else c.tag
                if tag == "LastName":
                    last = _all_text(c)
                elif tag in ("ForeName", "FirstName"):
                    first = _all_text(c)
            if last or first:
                authors.append({"lastname": last, "forename": first})

        journal_el = find("Journal")
        journal_title = ""
        if journal_el is not None:
            for c in journal_el:
                if c.tag.split("}")[-1] == "Title":
                    journal_title = _all_text(c)
                    break

        pub_date = ""
        pub_el = find("PubDate")
        if pub_el is None:
            pub_el = find("ArticleDate")
        if pub_el is not None:
            pub_date = _all_text(pub_el)

        mesh_terms = []
        for mesh_el in find_all("DescriptorName"):
            mesh_terms.append(_text(mesh_el) or _all_text(mesh_el))

        result.append({
            "pmid": pmid,
            "title": title,
            "abstract": abstract[:2000] if abstract else "",  # 초록 길이 제한
            "authors": authors,
            "journal": journal_title,
            "pub_date": pub_date,
            "mesh_terms": mesh_terms,
        })
    return result


def fetch_pubmed(category: str = "Protein Structure & Enzyme Engineering", limit: int | None = None) -> list[dict]:
    """지정 카테고리로 PubMed 검색 후 최대 limit건 메타데이터 반환."""
    limit = limit or FETCH_LIMIT
    print(f"[fetch] 카테고리: {category} (최대 {limit}건)", flush=True)
    query = get_query_string(category)
    ids = esearch(query, retmax=limit)
    time.sleep(REQUEST_DELAY_SEC)
    if not ids:
        print("[fetch] 검색 결과 없음", flush=True)
        return []
    xml_str = efetch(ids)
    time.sleep(REQUEST_DELAY_SEC)
    papers = parse_pubmed_xml(xml_str)
    print(f"[fetch] 수집 완료: {len(papers)}건", flush=True)
    return papers


def fetch_pubmed_distributed(
    categories: list[str],
    total_limit: int,
) -> list[dict]:
    """여러 카테고리에 total_limit를 균등 분배해 수집. 각 논문에 'category' 필드 추가."""
    if not categories:
        return []
    n = len(categories)
    per_limit = max(1, total_limit // n)
    remainder = total_limit - per_limit * n
    limits = [per_limit + (1 if i < remainder else 0) for i in range(n)]
    print(f"[distribute] 총 {total_limit}건을 {n}개 카테고리에 분배 (카테고리당 약 {per_limit}~{per_limit + (1 if remainder else 0)}건)", flush=True)
    combined = []
    for idx, (cat, cap) in enumerate(zip(categories, limits), 1):
        if cat not in CATEGORIES:
            continue
        print(f"[distribute] ({idx}/{n}) {cat} (최대 {cap}건)", flush=True)
        papers = fetch_pubmed(category=cat, limit=cap)
        for p in papers:
            p["category"] = cat
        combined.extend(papers)
    print(f"[distribute] 전체 수집 완료: {len(combined)}건", flush=True)
    return combined


def _category_to_basename(category: str) -> str:
    """카테고리명을 파일명에 쓸 수 있는 문자열로 변환 (소문자, 공백·특수문자 제거)."""
    return category.lower().replace(" & ", "_").replace(" ", "_").replace("-", "_").replace("'", "")


def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="PubMed 메타데이터 수집 (esearch + efetch). 중급 예제용 카테고리 지원."
    )
    parser.add_argument(
        "category",
        nargs="?",
        default="Protein Structure & Enzyme Engineering",
        help="검색 카테고리 (기본: Protein Structure & Enzyme Engineering)",
    )
    parser.add_argument(
        "-n", "--limit",
        type=int,
        default=None,
        help=f"최대 논문 건수 (기본: config.FETCH_LIMIT={FETCH_LIMIT})",
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default=None,
        help="출력 JSON 파일 경로 (미지정 시 output/pubmed_<category>_<limit>.json)",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="사용 가능한 카테고리 및 중급 추천 카테고리 출력 후 종료",
    )
    parser.add_argument(
        "-d", "--distribute",
        action="store_true",
        help="FETCH_LIMIT(또는 -n)을 지정 카테고리에 균등 분배해 수집. 출력: pubmed_distributed_<limit>.json",
    )
    parser.add_argument(
        "--distribute-categories",
        choices=("intermediate", "advanced"),
        default=None,
        help="분배 시 사용할 카테고리 묶음 (기본: config.FETCH_CATEGORIES 또는 intermediate)",
    )
    args = parser.parse_args()

    if args.list:
        print("사용 가능한 카테고리:")
        for name in CATEGORIES:
            marks = []
            if name in INTERMEDIATE_RECOMMENDED:
                marks.append("중급 추천")
            if name in ADVANCED_RECOMMENDED:
                marks.append("고급 추천")
            mark = f" [{', '.join(marks)}]" if marks else ""
            print(f"  - {name}{mark}")
        print("\n중급 추천:", ", ".join(INTERMEDIATE_RECOMMENDED))
        print("고급 추천:", ", ".join(ADVANCED_RECOMMENDED))
        return

    if args.distribute:
        if args.distribute_categories == "advanced":
            categories = list(ADVANCED_RECOMMENDED)
        else:
            categories = list(FETCH_CATEGORIES) if FETCH_CATEGORIES else list(INTERMEDIATE_RECOMMENDED)
        categories = [c for c in categories if c in CATEGORIES]
        if not categories:
            print("No valid categories for distribute mode.", file=sys.stderr)
            sys.exit(1)
        total_limit = args.limit or FETCH_LIMIT
        out_dir = Path(__file__).resolve().parent / "output"
        out_dir.mkdir(parents=True, exist_ok=True)
        out_file = out_dir / f"pubmed_distributed_{total_limit}.json"
        stem, suffix = out_file.stem, out_file.suffix
        n = 1
        while out_file.exists():
            out_file = out_dir / f"{stem}_{n}{suffix}"
            n += 1
        papers = fetch_pubmed_distributed(categories, total_limit)
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(papers, f, ensure_ascii=False, indent=2)
        from collections import Counter
        counts = Counter(p.get("category") for p in papers)
        print(f"Saved {len(papers)} articles to {out_file}")
        for cat, cnt in sorted(counts.items(), key=lambda x: -x[1]):
            print(f"  - {cat}: {cnt}")
        return

    category = args.category
    if category not in CATEGORIES:
        print(f"Unknown category: {category}", file=sys.stderr)
        print("Use --list to see available categories.", file=sys.stderr)
        sys.exit(1)

    limit = args.limit or FETCH_LIMIT
    out_dir = Path(__file__).resolve().parent / "output"
    out_dir.mkdir(parents=True, exist_ok=True)

    if args.output:
        out_file = Path(args.output)
    else:
        base = _category_to_basename(category)
        out_file = out_dir / f"pubmed_{base}_{limit}.json"

    papers = fetch_pubmed(category=category, limit=limit)

    # 기존 파일에 덮어쓰지 않고, 같은 이름이 있으면 _1, _2 ... 붙여 새 파일로 저장
    if out_file.exists():
        stem, suffix = out_file.stem, out_file.suffix
        n = 1
        while out_file.exists():
            out_file = out_dir / f"{stem}_{n}{suffix}"
            n += 1

    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(papers, f, ensure_ascii=False, indent=2)

    print(f"Saved {len(papers)} articles to {out_file}")
    for i, p in enumerate(papers[:3], 1):
        print(f"  {i}. [{p.get('pmid')}] {p.get('title', '')[:60]}...")


if __name__ == "__main__":
    main()
