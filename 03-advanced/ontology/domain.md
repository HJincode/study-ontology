# 고급 도메인: 근거 중심 지식 그래프 (통합·추론·ETL)

## 도메인 (중급과 동일 + 아래 확장)

**"생물의학 학술 문헌에 보고된 연구 결과와 그 근거를 구조화하는 근거 중심 지식 그래프"**

- 중급의 문헌 계층·생물의학 개체·관계 **전부 유지**.
- 고급에서 추가: **외부 온톨로지 통합**, **추론**, **ETL**, **(선택) API**.

## 추가 요소 (고급)

- **외부 온톨로지 매핑**: Gene Ontology(GO), Disease Ontology(DO), DrugBank 등과 equivalence/매핑.
- **추론**: ASSOCIATED_WITH 전이, Gene—ACTIVATES→Pathway—ASSOCIATED_WITH→Disease 등 간접 근거.
- **ETL**: 문헌 → NER/관계추출 → KG 파이프라인. INHIBITS/ACTIVATES는 추출 단계에서 채움.
- **API/엔드포인트**: (선택) REST API 또는 SPARQL 엔드포인트.

## 이 폴더에 넣을 것 (작업 시)

- 통합 온톨로지 파일 (.ttl / .owl), 매핑 정의.
- `rules/` — 추론 규칙 (선택).
