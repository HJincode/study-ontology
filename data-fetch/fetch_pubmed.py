"""
PubMed E-utilities 연동: 검색어로 논문 ID 조회 후 상세 메타데이터 수집.
- esearch: 검색어로 PMID 목록 조회 (최대 FETCH_LIMIT건)
- efetch: PMID별 메타데이터(제목, 초록, 저자, 저널, MeSH 등) 조회 후 JSON 저장

참고: db=pubmed 는 논문 "원문(본문)" 이 아닌 메타데이터+초록만 제공합니다.
      전체 원문이 필요하면 PMC(db=pmc) 를 사용해야 합니다.
"""
