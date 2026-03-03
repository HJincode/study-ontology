# 고급 (Advanced) — 근거 중심 지식 그래프: 통합·추론·ETL·API

이 레벨은 **근거 중심 지식 그래프** 도메인을 **통합·추론·ETL·(선택) API**까지 확장합니다.  
코드는 작성하지 않고 **뼈대(폴더·문서)** 만 두었습니다. 아래 순서대로 작업하면 됩니다.

---

## 이 레벨에서 만들 것

- **목표**: 다중 온톨로지 통합, 추론, ETL, (선택) API/서비스화.
- **도메인**: 중급과 동일 + 외부 온톨로지·**통합 KG(예: PrimeKG)** 매핑, 추론 규칙, 문헌→추출→KG 파이프라인.
- **산출물**: 통합 온톨로지(매핑 포함), 추론 규칙(선택), ETL 스크립트, (선택) REST API 또는 SPARQL 엔드포인트.

---

## 필요한 폴더 (뼈대)

| 폴더 | 용도 |
|------|------|
| `ontology/` | 통합 온톨로지·매핑 정의 (.ttl / .owl). `domain.md` 참고. |
| `data/` | 고급용 데이터 (다중 출처, 추출 결과, 외부 DB 연동용 샘플). |
| `scripts/` | ETL(문헌→추출→KG), 추론 호출, (선택) API 서버 스크립트. |
| `queries/` | 복합·추론 쿼리 (SPARQL 등). |
| `rules/` | 추론 규칙 정의 (선택). |

---

## 순서대로 할 작업 (Task Order)

아래 번호 순서대로 진행하세요.

### 1. 통합 설계

- [ ] **1-1.** 중급 온톨로지(문헌 계층 + 생물의학 개체 + 관계)를 기준으로, **통합할 외부 리소스** 목록 정하기:
  - **온톨로지**: Gene Ontology(GO), Disease Ontology(DO), DrugBank 등 — 우리 클래스와 equivalence/subclass 매핑.
  - **통합 지식 그래프**: **PrimeKG** (정밀의료용 통합 KG, drug/disease/gene 등 20개 리소스 통합) — 우리 Gene/Disease/Drug를 PrimeKG 노드 타입·ID와 매핑해 데이터 보강·연계.
- [ ] **1-2.** 매핑 방침 정하기 — 우리 클래스(Gene, Disease, Drug 등)와 외부 용어(GO term, DOID, DrugBank ID, 또는 PrimeKG 노드 ID)의 equivalence 또는 subclass 관계. 산출물: `ontology/mapping_design.md` 또는 표.

### 2. 통합 온톨로지 작성

- [ ] **2-1.** 통합 온톨로지 파일 작성. 위치: `ontology/` (예: `evidence_kg_integrated.ttl` 또는 `.owl`).
- [ ] **2-2.** 외부 온톨로지와의 매핑(owl:equivalentClass, owl:equivalentProperty, rdfs:subClassOf 등) 반영.
- [ ] **2-3.** (선택) 추론에 쓸 속성·클래스 제약 정리.

### 3. 추론 규칙 (선택)

- [ ] **3-1.** 추론 목표 정하기 — 예: ASSOCIATED_WITH 전이, “Gene A —ACTIVATES→ Pathway P, P —ASSOCIATED_WITH→ Disease D” → 간접 연관 추론.
- [ ] **3-2.** 규칙 정의. 위치: `rules/` (예: SPARQL CONSTRUCT, 또는 규칙 엔진용 규칙 파일).
- [ ] **3-3.** 추론 실행 방법 정하기 — SPARQL 추론 또는 규칙 엔진 호출. 필요 시 `scripts/`에 추론 스크립트.

### 4. ETL 파이프라인

- [ ] **4-1.** 파이프라인 단계 정의 — 문헌 수집 → (선택) 청크 분할 → NER/관계추출 → KG 형식( RDF/JSON) → 저장소(Neo4j/PostgreSQL 또는 RDF 저장소) 로드.
- [ ] **4-2.** ETL 스크립트 뼈대 또는 순서 문서. 위치: `scripts/` (예: `etl_pipeline.md` 또는 단계별 스크립트).
- [ ] **4-3.** INHIBITS/ACTIVATES는 추출 단계에서 채우는 관계로, ETL 출력 스키마에 포함.

### 5. API 또는 SPARQL 엔드포인트 (선택)

- [ ] **5-1.** 노출할 쿼리 또는 API 목록 정하기 — 예: “Gene X를 MENTIONS하는 문서”, “Disease D와 ASSOCIATED_WITH인 Drug”, 추론 결과 조회.
- [ ] **5-2.** REST API 서버 또는 SPARQL 엔드포인트 구성. 위치: `scripts/` 또는 별도 서비스 디렉터리.
- [ ] **5-3.** 호출 방법·예시 문서화.

### 6. 복합 쿼리

- [ ] **6-1.** 통합·추론 반영 쿼리 작성. 위치: `queries/` (예: SPARQL). “간접 연관”, “외부 ID로 조회” 등.
- [ ] **6-2.** 쿼리 실행 및 결과 확인.

---

## 사용 도구

- **저장소**: Neo4j/PostgreSQL + (선택) Jena Fuseki, GraphDB 등 RDF/SPARQL 저장소.
- **추론**: SPARQL CONSTRUCT/추론 엔진, 또는 규칙 엔진.
- **참고**: `../docs/domain-evidence-kg-level-mapping.md` — 고급 범위 요약.

---

## 데이터

- **종류**: 문헌 메타데이터, 추출 결과, 외부 온톨로지/DB 연동용 데이터. **(선택) PrimeKG** — 통합 KG 데이터로 우리 스키마와 매핑해 drug/disease/gene 관계 보강.
- **규모**: 중급보다 다양·다중 출처. ETL로 통합.
- **PrimeKG 참고**: [Zitnik Lab PrimeKG](https://zitniklab.hms.harvard.edu/projects/PrimeKG), [GitHub mims-harvard/PrimeKG](https://github.com/mims-harvard/PrimeKG).
