# 근거 중심 지식 그래프 도메인 — 초/중/고급 적용 매핑

목표 도메인: **“생물의학 학술 문헌에 보고된 연구 결과와 그 근거를 구조화하는 근거 중심 지식 그래프”**

- 문헌 기반, 실험 결과/가설/주장 = “보고된 내용”, 실제 실험 실행/실패는 제외.

---

## 1. 전체 도메인 요약 (참고)

| 구분 | 내용 |
|------|------|
| **문헌 계층** | Document (논문), EvidenceChunk (abstract/section 단위) |
| **생물의학 개체** | Gene / Protein, Disease, Drug / Compound, Pathway, Phenotype, Assay |
| **관계** | MENTIONS, ASSOCIATED_WITH (선택), INHIBITS / ACTIVATES (추출 단계에서만) |

---

## 2. 레벨별 적용 가능 범위

### 초급 (01-beginner) — **도메인 축소판**

**적용 가능**: ✅ **일부만** 적용.

- **포함할 것**
  - **문헌 계층**: Document, EvidenceChunk (또는 초급에서는 Document만 + “Chunk” 1개로 단순화).
  - **생물의학 개체**: **2~3개만** 선택 (예: Gene, Disease, Drug). 나머지(Pathway, Phenotype, Assay)는 초급에서 제외.
  - **관계**: **MENTIONS 1개**만 정의. ASSOCIATED_WITH / INHIBITS / ACTIVATES는 제외.
- **클래스 수**: 5~7개 (Document, EvidenceChunk, Gene, Disease, Drug + 선택 1~2개).
- **데이터**: 추출 파이프라인 없이 **수동·간이 데이터** (예: JSON/CSV). “문헌 A의 청크 1이 Gene X를 MENTIONS” 같은 식으로 10~20건 정도.
- **목표**: 클래스·인스턴스·속성 정의, RDF/OWL 작성, 로드·검증 한 사이클.

**정리**: 전체 도메인의 **최소 집합**으로 초급 예제 가능. 문헌 + 청크 + 소수 생물의학 개체 + MENTIONS.

---

### 중급 (02-intermediate) — **전체 스키마 + 저장소 + 쿼리**

**적용 가능**: ✅ **대부분** 적용.

- **포함할 것**
  - **문헌 계층**: Document, EvidenceChunk 전부.
  - **생물의학 개체**: Gene, Protein, Disease, Drug/Compound, Pathway, Phenotype, Assay **전부**.
  - **관계**: MENTIONS, ASSOCIATED_WITH. INHIBITS/ACTIVATES는 **스키마에 정의**하고, 값은 추출 결과가 있으면 넣고 없으면 빈 채로 둠.
- **할 일**
  - 초급에서 만든 소규모 온톨로지를 **확장**해 위 클래스·속성 반영.
  - **Neo4j 또는 PostgreSQL**에 스키마/그래프 모델 반영, RDF(또는 JSON) → 저장소 **변환·로드**.
  - **예제 쿼리**: “Document 중 Gene X를 MENTIONS하는 것”, “Disease D와 ASSOCIATED_WITH인 Drug”, “EvidenceChunk별 MENTIONS 집계” 등.
- **데이터**: 추출기 출력(또는 시뮬레이션 JSON)을 변환 스크립트로 저장소에 로드. 50~200건 수준 권장.

**정리**: **전체 엔티티 + MENTIONS/ASSOCIATED_WITH** 를 한 번에 다루기에 적합. “근거 중심 지식 그래프”의 **구조와 쿼리**를 경험하는 단계.

---

### 고급 (03-advanced) — **통합·추론·ETL·API**

**적용 가능**: ✅ **전체 + 통합·추론·서비스**.

- **포함할 것**
  - 위 **전부** 유지.
  - **외부 온톨로지 통합**: Gene Ontology(GO), Disease Ontology(DO), DrugBank 등과 **매핑/equivalence** (예: 우리 Gene 클래스 ↔ GO term).
  - **추론**: ASSOCIATED_WITH 전이, “Gene A —ACTIVATES→ Pathway P, P —ASSOCIATED_WITH→ Disease D” 등 **간접 근거** 추론 (규칙 또는 SPARQL).
  - **INHIBITS/ACTIVATES**: 추출 단계에서 채우는 관계이므로, **ETL 파이프라인** (문헌 → NER/관계추출 → KG) 설계·구현.
  - **API/엔드포인트**: 근거 그래프를 REST API 또는 **SPARQL 엔드포인트**로 노출 (선택).
- **데이터**: 여러 출처(문헌 메타데이터, 추출 결과, 외부 DB)를 ETL로 통합.

**정리**: **다중 온톨로지 통합 + 추론 + ETL + (선택) API** 까지 적용하는 레벨.

---

## 3. 요약 표

| 레벨 | 문헌 계층 | 생물의학 개체 | 관계 | 데이터 | 적용 가능 여부 |
|------|-----------|----------------|------|--------|----------------|
| **초급** | Document, EvidenceChunk(단순화 가능) | Gene, Disease, Drug 등 **2~3개만** | **MENTIONS** 만 | 수동/간이 JSON·CSV (10~20건) | ✅ **축소판** |
| **중급** | Document, EvidenceChunk **전부** | Gene, Protein, Disease, Drug, Pathway, Phenotype, Assay **전부** | MENTIONS, ASSOCIATED_WITH; INHIBITS/ACTIVATES 스키마만 | 추출 또는 시뮬레이션 데이터 → Neo4j/PostgreSQL (50~200건) | ✅ **대부분** |
| **고급** | 전부 | 전부 + **외부 온톨로지 매핑** | 전부 + **추론 규칙** | ETL(문헌→추출→KG), 다중 출처 | ✅ **전체** |

---

## 4. 한 줄 정리

- **초급**: “문헌 + 청크 + Gene/Disease/Drug + MENTIONS” 만 정의하고, 소량 수동 데이터로 로드·검증.
- **중급**: 위 도메인 **전체 스키마**를 넣고 Neo4j/PostgreSQL에 로드한 뒤, MENTIONS/ASSOCIATED_WITH 중심으로 쿼리.
- **고급**: 외부 온톨로지 통합, ASSOCIATED_WITH/ACTIVATES 등 **추론**, 문헌→추출→KG **ETL**, (선택) API.

이 도메인은 **초/중/고급 모두에 적용 가능**하며, 초급은 축소판, 중급은 전체 스키마·쿼리, 고급은 통합·추론·ETL·API로 단계를 나누면 됩니다.
