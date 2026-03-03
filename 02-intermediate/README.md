# 중급 (Intermediate) — 근거 중심 지식 그래프

이 레벨부터 **근거 중심 지식 그래프** 도메인을 적용합니다.  
코드는 작성하지 않고 **뼈대(폴더·문서)** 만 두었습니다. 아래 순서대로 작업하면 됩니다.

---

## 이 레벨에서 만들 것

- **목표**: 온톨로지 확장, 그래프/관계형 DB 반영, 쿼리 작성.
- **도메인**: 생물의학 학술 문헌에 보고된 연구 결과와 근거를 구조화하는 지식 그래프.
- **산출물**: 확장 온톨로지(문헌 계층 + 생물의학 개체 + 관계), Neo4j 또는 PostgreSQL 변환·로드, 예제 쿼리(Cypher/SQL).

---

## 필요한 폴더 (뼈대)

| 폴더 | 용도 |
|------|------|
| `ontology/` | 확장 온톨로지 정의 (.ttl / .owl). `domain.md` 참고. |
| `data/` | 중급용 데이터 (추출 또는 시뮬레이션 JSON/CSV, 50~200건 권장). |
| `scripts/` | RDF 또는 JSON → Neo4j/PostgreSQL 변환·로드 스크립트. |
| `queries/` | Cypher 또는 SQL 예제 쿼리. |

---

## 순서대로 할 작업 (Task Order)

아래 번호 순서대로 진행하세요.

### 1. 도메인·스키마 확정

- [ ] **1-1.** `ontology/domain.md` 확인 또는 수정 — 문헌 계층(Document, EvidenceChunk), 생물의학 개체(Gene, Protein, Disease, Drug, Pathway, Phenotype, Assay), 관계(MENTIONS, ASSOCIATED_WITH, INHIBITS/ACTIVATES 스키마만).
- [ ] **1-2.** 클래스·속성 설계표 작성 — 각 클래스의 식별자, 속성(데이터 속성/객체 속성), 도메인/범위. 산출물: `ontology/design.md` 또는 별도 표.

### 2. 확장 온톨로지 작성

- [ ] **2-1.** RDF(Turtle) 또는 OWL로 온톨로지 파일 작성. 위치: `ontology/` (예: `evidence_kg_ontology.ttl` 또는 `.owl`).
- [ ] **2-2.** 정의할 내용: Document, EvidenceChunk, Gene, Protein, Disease, Drug, Compound, Pathway, Phenotype, Assay 클래스; MENTIONS, ASSOCIATED_WITH, INHIBITS, ACTIVATES 속성(객체 속성); 필요 시 데이터 속성(제목, 식별자 등).

### 3. 저장소 선택 및 스키마 반영

- [ ] **3-1.** 저장소 결정: **Neo4j** 또는 **PostgreSQL** 중 하나 선택.
- [ ] **3-2.** 선택한 저장소에 맞는 스키마/그래프 모델 설계 — 노드 레이블(또는 테이블), 관계(또는 FK), 속성 컬럼.

### 4. 변환·로드 스크립트

- [ ] **4-1.** 입력 데이터 형식 정의 — 추출기 출력 JSON 또는 시뮬레이션 CSV/JSON (Document, EvidenceChunk, 개체, MENTIONS/ASSOCIATED_WITH 등).
- [ ] **4-2.** 변환 스크립트 작성 — RDF 또는 JSON → Neo4j/PostgreSQL. 위치: `scripts/` (예: `load_to_neo4j.py` 또는 `load_to_postgres.py`).
- [ ] **4-3.** 데이터 로드 실행 — 50~200건 수준 권장. 로드 후 노드/관계 수 확인.

### 5. 예제 쿼리 작성·실행

- [ ] **5-1.** 쿼리 1: Document 중 특정 Gene(또는 Disease/Drug)을 MENTIONS하는 문서 조회. 저장: `queries/mentions_by_entity.cypher` 또는 `.sql`.
- [ ] **5-2.** 쿼리 2: 특정 Disease와 ASSOCIATED_WITH인 Drug 조회. 저장: `queries/associated_drugs.cypher` 또는 `.sql`.
- [ ] **5-3.** 쿼리 3: EvidenceChunk별 MENTIONS 집계(또는 문서별 개체 수). 저장: `queries/mentions_aggregate.cypher` 또는 `.sql`.
- [ ] **5-4.** 각 쿼리 실행해 결과 확인.

---

## 사용 도구

- **저장소**: Neo4j 또는 PostgreSQL.
- **언어**: Python (rdflib, py2neo 또는 psycopg2 등).
- **참고**: `../docs/domain-evidence-kg-level-mapping.md` — 중급 범위 요약.

---

## 데이터

- **종류**: 추출 파이프라인 출력 또는 시뮬레이션 JSON/CSV.
- **내용**: Document, EvidenceChunk, Gene/Protein/Disease/Drug/Pathway/Phenotype/Assay 인스턴스, MENTIONS·ASSOCIATED_WITH 관계.
- **건수**: 50~200건 권장.
