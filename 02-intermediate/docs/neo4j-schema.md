# Neo4j 스키마 설계 (3-2 산출물)

저장소: **Neo4j** (3-1 선택).  
온톨로지: `ontology/evidence_kg_ontology.ttl`, `ontology/design.md` 기준 매핑.

---

## 매핑 규칙

- **OWL 클래스** → 노드 **레이블**
- **객체 속성** → **관계 타입**
- **데이터 속성** → 노드(또는 관계) **프로퍼티**

문헌 계층: Document–EvidenceChunk는 **`:HAS_CHUNK`** 관계로 연결.

---

## 노드 레이블 및 프로퍼티

| 노드 레이블 | 식별용 프로퍼티 | 기타 프로퍼티 | 비고 |
|-------------|-----------------|---------------|------|
| **Document** | `pmid` (고유) | `title`, `pub_date` | 논문 1건 = 노드 1개 |
| **EvidenceChunk** | `chunk_id` (고유) | `hasText` | 문서당 1청크 시 예: `{pmid}_chunk_0` |
| **Gene** | `name` 또는 `gene_id` | — | mesh_terms / 추출 |
| **Protein** | `name` 또는 `protein_id` | — | mesh_terms / 추출 |
| **Disease** | `name` 또는 `disease_id` | — | mesh_terms / 추출 |
| **Drug** | `name` 또는 `drug_id` | — | mesh_terms / 추출 |
| **Pathway** | `name` 또는 `pathway_id` | — | mesh_terms / 추출 |
| **Phenotype** | `name` 또는 `phenotype_id` | — | mesh_terms / 추출 |
| **Assay** | `name` 또는 `assay_id` | — | mesh_terms / 추출 |
| **Compound** | `name` 또는 `compound_id` | — | mesh_terms / 추출 |

---

## 관계 타입 및 방향

| 관계 타입 | 방향 | From (시작 노드) | To (끝 노드) | 비고 |
|-----------|------|------------------|--------------|------|
| **HAS_CHUNK** | → | Document | EvidenceChunk | 문헌 계층. 1 Document : N Chunk |
| **MENTIONS** | → | Document 또는 EvidenceChunk | Gene, Protein, Disease, Drug, Pathway, Phenotype, Assay, Compound | 문헌/청크가 개체 언급 |
| **ASSOCIATED_WITH** | → | 위 생물의학 레이블 전부 | 동일 | 개체 간 연관. 쿼리 시 양방향 조회 가능 |
| **INHIBITS** | → | 생물의학 개체 | 생물의학 개체 | 주체 → 대상 |
| **ACTIVATES** | → | 생물의학 개체 | 생물의학 개체 | 주체 → 대상 |

---

## Relationship properties

| Relationship       | Properties            | Notes                                                                                                                                 |
|--------------------|-----------------------|---------------------------------------------------------------------------------------------------------------------------------------|
| **HAS_CHUNK**      | —                     | 프로퍼티 없음.                                                                                                                        |
| **MENTIONS**       | —                     | 프로퍼티 없음. 출처는 시작 노드(Document vs EvidenceChunk)로 구분. design.md “MENTIONS 관계: 출처 프로퍼티를 두지 않는 이유” 참고.     |
| **ASSOCIATED_WITH**| `pmid`, `evidence_chunk_id` | - Evidence-based: relationship provenance. `evidence_chunk_id`는 해당 관계를 뒷받침하는 청크를 가리킴. <br/>- 없으면 프로퍼티 생략(omit); 근거 표시가 필요하면 `has_evidence: false` 또는 `evidence_level` 사용 권장 (input-format.md §3.1 참고).                               |
| **INHIBITS**       | `pmid`, `evidence_chunk_id` | Same as above.                                                                                                                   |
| **ACTIVATES**      | `pmid`, `evidence_chunk_id` | Same as above.                                                                                                                   |

- 관계 레코드 입력 포맷(4-1)은 [docs/input-format.md](input-format.md) 참고.

### 왜 “프로퍼티를 안 넣는 방식(omit)”이 더 좋은가

`evidence_chunk_id`가 없을 때 **관계에 해당 프로퍼티를 아예 넣지 않는 것**을 권장한다. (`null`/빈 문자열 대신.)

**1) 의미가 가장 명확함**

- 프로퍼티가 없다 = “근거 chunk 정보가 제공되지 않았다”.
- `""`(빈 문자열)이나 `null`은 “진짜 값이 없는 건지 / ETL 버그인지 / 파싱 실패인지” 구분이 어렵다. “없는 건 없다”가 제일 깔끔하다.

**2) 데이터 품질/검증이 쉬움**

- `null`/`""`가 들어가면 이후에 `""` vs `null` vs `"NULL"` 같은 표준화 지옥이 생기고, 파이프라인마다 다르게 넣을 가능성이 크다.
- omit이면 “있으면 저장, 없으면 키 자체가 없음” 규칙이 단순해서 QA/validator 작성이 쉽다.

**3) 쿼리도 더 깔끔함**

- 예: 근거 있는 관계만 보고 싶다.
- **omit 방식**: `WHERE exists(r.evidence_chunk_id)` 로 끝.
- **null/"" 방식**: `WHERE r.evidence_chunk_id IS NOT NULL AND r.evidence_chunk_id <> ""` 처럼 조건이 늘고, 실수 가능성도 늘어난다.

**4) 저장공간/인덱싱 측면에서도 이득**

- 대부분의 관계에 `evidence_chunk_id`가 없을 수 있는 초기 단계에서는, 빈 값/`null`을 대량으로 저장하는 건 의미가 없다. (나중에 인덱스를 걸면) null/빈값 처리도 신경 써야 한다. omit이면 불필요한 데이터가 안 쌓인다.

**예외: null을 쓰는 게 더 나은 경우(드묾)**

- “`evidence_chunk_id`는 항상 있어야 하는데, 현재는 미정/대기 상태”를 표현하고 싶다 — 즉 **상태 모델링**이 필요할 때(예: `evidence_status: "pending"`) — 라면 null도 고려할 수 있다.
- 하지만 그런 경우에도 null보다 **상태 필드를 따로 두는 것**(예: `evidence_status: "pending"`)이 보통 더 낫다.

---

## 인덱스 / 제약 (권장)

- **Document**: `pmid` UNIQUE 제약(또는 유니크 인덱스)
- **EvidenceChunk**: `chunk_id` UNIQUE 제약(또는 유니크 인덱스)
- **생물의학 노드**: 레이블별 `name` (또는 해당 `*_id`) 인덱스 — MERGE/조회 성능

(실제 `CREATE CONSTRAINT` / `CREATE INDEX`는 4-2 로드 스크립트 또는 수동 실행.)

---

## §5 예제 쿼리와의 대응

- **5-1** (특정 Gene/Disease/Drug를 MENTIONS하는 Document): `(d:Document)-[:MENTIONS]->(e)` 사용.
- **5-2** (특정 Disease와 ASSOCIATED_WITH인 Drug): `(d:Disease)-[:ASSOCIATED_WITH]-(dr:Drug)` 사용.
- **5-3** (EvidenceChunk별 MENTIONS 집계): `(c:EvidenceChunk)-[:MENTIONS]->(e)` 후 `COUNT(e)`.

위 스키마로 세 쿼리 모두 작성 가능.



---

## [참고]

### OWL(.ttl)과 Neo4j 역할 구분 — 관계 메타데이터를 TTL에 넣지 않는 이유

**1️⃣ OWL(.ttl)의 역할**

온톨로지는 **개념 구조**를 정의하는 용도이다. 
예: Drug INHIBITS Protein, ASSOCIATED_WITH, MENTIONS 

— 즉 **어떤 개체와 어떤 관계가 존재하는지** 정의하는 것.  
👉 하지만 **관계에 붙는 메타데이터**(예: pmid, evidence_chunk_id)는 보통 OWL에 넣지 않는다.

**2️⃣ Neo4j의 역할**

Neo4j에서는 **관계에 속성(property)** 을 붙일 수 있다. 
예:
```
Aspirin -[:INHIBITS {pmid: "12345678", evidence_chunk_id: "chunk_12"}]-> COX1
```
즉 Neo4j에서는 **관계**, **관계의 출처**, **근거 문장** 같은 데이터를 함께 저장한다.

**3️⃣ 그래서 TTL을 수정하지 않은 이유**

관계 메타데이터(pmid, evidence_chunk_id)는 온톨로지 구조가 아니라 **데이터 저장용 정보**이기 때문에, Neo4j에서만 사용하고 OWL에는 추가하지 않는다.

**4️⃣ 문서에 한 줄 적어 두는 이유**

“왜 TTL에는 pmid가 없지?”라고 혼동할 수 있다. 그래서 다음을 명시한다:
> 관계의 출처 정보(pmid, evidence_chunk_id)는 Neo4j에서만 사용하고 OWL 온톨로지에는 포함하지 않는다.

**핵심 한 줄 요약: OWL(.ttl)은 개념 구조만 정의하고, 관계의 근거 정보(pmid, evidence_chunk_id)는 Neo4j 관계 속성으로만 관리한다.**