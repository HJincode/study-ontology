# 입력 데이터 형식 정의 (4-1 산출물)

Neo4j 로드 시 사용하는 입력 형식과 노드·관계 매핑을 정의한다.  
스키마: [neo4j-schema.md](neo4j-schema.md).

---

## 0. 논문 섹션 vs extractor/simulator 출력 필드

### 1️⃣ 논문 섹션 (section)

논문 구조의 일부.

예: `abstract`, `introduction`, `methods`, `results`, `discussion`  
→ 이건 **논문 텍스트 구조**다.

예 데이터:

| 필드 | 예시 |
|------|------|
| `section_id` | `12345678_sec2` |
| `section_category` | `results` |
| `section_text` | `"Aspirin inhibits COX-1..."` |

### 2️⃣ Extractor 출력 (relation extractor output)

논문 텍스트를 분석해서 **엔티티와 관계를 뽑아낸 결과 데이터**.

예: 문장 *"Aspirin inhibits COX-1"* → Extractor 결과:

```json
{
  "subject_id": "Drug:Aspirin",
  "predicate": "INHIBITS",
  "object_id": "Protein:PTGS1",
  "pmid": "12345678",
  "evidence_chunk_id": "12345678_chunk_12"
}
```

**출력 필드(output fields)** 의미:

| 필드 | 의미 |
|------|------|
| `subject_id` | 관계의 시작 엔티티 |
| `predicate` | 관계 타입 |
| `object_id` | 관계의 대상 엔티티 |
| `pmid` | 어느 논문 |
| `evidence_chunk_id` | 어느 문장(chunk) |

(실제 Neo4j 로드용 포맷은 §3에서 `type`, `from_entity_type`, `from_entity_name`, `to_entity_type`, `to_entity_name`, `pmid`, `evidence_chunk_id`로 정의.)

### 3️⃣ Simulator 출력

시뮬레이션이나 모델이 **가설 관계**를 생성하는 경우.

예: *Gene A may activate Pathway B* →

```json
{
  "subject_id": "Gene:TP53",
  "predicate": "ACTIVATES",
  "object_id": "Pathway:Apoptosis",
  "source": "simulation"
}
```

### 4️⃣ 전체 흐름

```
논문
  ↓
section
  ↓
chunk
  ↓
extractor
  ↓
relation output (출력 필드)
  ↓
Neo4j 관계 생성
```

**핵심 요약**: extractor/simulator **출력 필드**는 논문 섹션이 아니라, **텍스트 분석 결과로 생성된 관계 데이터의 컬럼(필드)** 이다.

---

## 1. 현재 원천 JSON (PubMed)

파일: `data/pubmed_distributed_200_cleansed.json`.

| 필드 | 타입 | 비고 |
|------|------|------|
| `pmid` | string | 논문 식별자. Document 노드 `pmid` |
| `title` | string | Document 노드 `title` |
| `abstract` | string | EvidenceChunk 노드 `hasText` (문서당 1청크 시) |
| `pub_date` | string | Document 노드 `pub_date` |
| `authors` | array | 현재 스키마에는 노드로 적재하지 않음 (필요 시 확장) |
| `journal` | string | 현재 스키마에는 미사용 (필요 시 확장) |
| `mesh_terms` | array of string | MeSH 문자열 → 엔티티 매핑 후 MENTIONS 관계 생성 |
| `category` | string | 분배 모드 카테고리 (필요 시 노드/프로퍼티 확장) |

**참고**: `mentions` 배열·`relations` 엣지 리스트는 원천 JSON에 없음. MENTIONS는 mesh_terms→엔티티 매핑 또는 title/abstract NER로, ASSOCIATED_WITH/INHIBITS/ACTIVATES는 추출 파이프라인 또는 시뮬레이션 출력으로 생성한다.

---

## 2. 노드 매핑 요약

| Neo4j 노드 | 식별 | 원천 |
|------------|------|------|
| Document | `pmid` | JSON `pmid` |
| EvidenceChunk | `chunk_id` (예: `{pmid}_chunk_0`) | 규칙 생성. 내용은 `abstract` |
| Gene, Protein, Disease, Drug, Pathway, Phenotype, Assay, Compound | `name` (또는 *_id) | mesh_terms 매핑 또는 NER/추출 |

---

## 3. 관계 레코드 입력 포맷 (확정)

ASSOCIATED_WITH, INHIBITS, ACTIVATES는 **관계 출처를 그래프에서 쿼리**하기 위해 관계 프로퍼티를 둔다.  
추출기 출력 또는 시뮬레이션에서 아래 형식으로 관계 레코드를 내어 주면, 4-2 로드 스크립트가 Neo4j 관계 생성 시 프로퍼티로 적재한다.

### 3.1 개체 간 관계 레코드 (ASSOCIATED_WITH / INHIBITS / ACTIVATES)

각 레코드는 **한 개의 관계(엣지) 1건**에 대응한다.

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `type` | string | ✓ | `ASSOCIATED_WITH` \| `INHIBITS` \| `ACTIVATES` |
| `from_entity_type` | string | ✓ | 시작 노드 레이블 (Gene, Disease, Drug 등) |
| `from_entity_name` | string | ✓ | 시작 개체 식별(예: name) |
| `to_entity_type` | string | ✓ | 끝 노드 레이블 |
| `to_entity_name` | string | ✓ | 끝 개체 식별 |
| **`pmid`** | string | ✓ | 해당 관계의 근거 문헌 PubMed ID. Neo4j 관계 프로퍼티 `pmid` |
| **`evidence_chunk_id`** | string | 권장 | 해당 관계를 뒷받침하는 EvidenceChunk 식별자(예: `{pmid}_chunk_0`). Neo4j 관계 프로퍼티 `evidence_chunk_id` |

- **입력 예시 (JSON 한 줄)**:  
  `{ "type": "ASSOCIATED_WITH", "from_entity_type": "Disease", "from_entity_name": "Neoplasms", "to_entity_type": "Drug", "to_entity_name": "Metformin", "pmid": "33546704", "evidence_chunk_id": "33546704_chunk_0" }`
- 추출 파이프라인에서 chunk 단위로 관계를 낼 경우 `evidence_chunk_id`를 반드시 채우면, 나중에 “이 청크에서 나온 관계만” 쿼리할 수 있다.

**evidence_chunk_id 없을 때 (4-2 로드 스크립트 규칙)**

- **있으면**: 관계 프로퍼티 `evidence_chunk_id`로 저장.
- **없으면**: 해당 프로퍼티를 저장하지 않음(omit). `null`/빈 문자열은 넣지 않음.
- “근거 없는 관계”를 표시해야 하면 별도 프로퍼티 사용을 권장:
  - `has_evidence: false` (선택), 또는
  - `evidence_level: "none" | "chunk" | "multi"` (확장).

### 3.2 MENTIONS

MENTIONS는 **관계 프로퍼티 없음**.  
Document 또는 EvidenceChunk → 엔티티 노드로의 엣지만 생성하면 되며, 출처는 시작 노드 레이블로 구분한다.  
입력은 “문서/청크 식별자 + 엔티티 타입 + 엔티티 name” 리스트로 충분하다(별도 `pmid`/`evidence_chunk_id` 관계 프로퍼티는 두지 않음).

---

## 4. 4-2 로드 스크립트에서 참고할 것

- 노드: 위 §1·§2와 [neo4j-schema.md](neo4j-schema.md) 노드 레이블·프로퍼티 표 준수.
- 관계: HAS_CHUNK·MENTIONS는 프로퍼티 없음. ASSOCIATED_WITH/INHIBITS/ACTIVATES는 §3.1 형식에서 `pmid`, `evidence_chunk_id`를 읽어 Neo4j 관계 프로퍼티로 저장.
