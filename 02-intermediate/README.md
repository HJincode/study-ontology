# 중급 (Intermediate) — 근거 중심 지식 그래프

이 레벨부터 **근거 중심 지식 그래프** 도메인을 적용합니다.  
코드는 작성하지 않고 **뼈대(폴더·문서)** 만 두었습니다. 아래 순서대로 작업하면 됩니다.

---

📰 **1️⃣ Document**  
= 논문 하나

예: *"Aspirin은 대장암 위험을 줄인다."* 이 문장이 들어있는 논문 전체가 Document.

📌 **2️⃣ EvidenceChunk**  
= 논문 안의 "근거 문장" 조각

논문 전체가 아니라, 예: *"Aspirin inhibits COX-1 signaling in colorectal cancer models."* 이 한 문장만 따로 저장.

왜냐면? → 주장은 문장에서 나오기 때문.

🧬 **3️⃣ 생물의학 개체**  
문장에서 등장하는 대상들: Drug(약물), Gene(유전자), Protein(단백질), Disease(질병), Pathway(생물학적 과정)

예 문장에서:

| 단어 | 타입 |
|------|------|
| Aspirin | Drug |
| COX-1 | Gene/Protein |
| colorectal cancer | Disease |

🔗 **4️⃣ 관계들**  
이제 연결을 만든다.

① **MENTIONS** — 문장이 어떤 개체를 언급했다는 뜻.  
EvidenceChunk → MENTIONS → Aspirin

② **ASSOCIATED_WITH** — 관련이 있다 (상관관계 수준)  
Aspirin → ASSOCIATED_WITH → colorectal cancer

③ **INHIBITS** — 억제한다 (기전 관계)  
Aspirin → INHIBITS → COX-1

④ **ACTIVATES** — 활성화한다

📊 **이걸 그림처럼 보면**

```
[Document]
    ↓ contains
[EvidenceChunk]
    ↓ mentions
[Aspirin] ── INHIBITS ──> [COX-1]
       └── ASSOCIATED_WITH ──> [Colorectal cancer]
```

🚨 **왜 "근거 중심"이 중요하냐?**

일반 그래프는: `Aspirin ── INHIBITS ── COX-1` 끝.

하지만 근거 중심 그래프는:

```
Aspirin ── INHIBITS ── COX-1
      ↑
EvidenceChunk (논문 문장)
      ↑
Document (논문)
```

→ 그래서 **"이 관계의 출처가 뭐냐?"** 를 항상 추적 가능.

🎯 **당신 프로젝트에서 왜 중요?**

가설 생성할 때: 그냥 연결 많다고 좋은 게 아님. **"몇 편 논문이 말했는가?"**, **"실험 기반인가?"**, **"리뷰인가?"** 이걸 판단해야 함.

즉, **연결 + 근거 + 출처 = 신뢰 가능한 가설 생성**

🔥 **한 줄 요약**  
근거 중심 지식 그래프는 *"논문 문장에 기반해 생물학적 관계를 연결한 출처 추적 가능한 관계 지도"*다.

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

**ETL 흐름 요약**: **Extract** (PubMed JSON, 선택 PrimeKG) → **Transform** (노드·관계 생성, design.md 식별자·도메인/범위 반영) → **Load** (Neo4j/PostgreSQL 적재). 상세 단계는 본 문서 하단 **「ETL 개요 (순서)」** 참고.

### 1. 도메인·스키마 확정

- [x] **1-1.** `ontology/domain.md` 확인 또는 수정 — 문헌 계층(Document, EvidenceChunk), 생물의학 개체(Gene, Protein, Disease, Drug, Pathway, Phenotype, Assay), 관계(MENTIONS, ASSOCIATED_WITH, INHIBITS/ACTIVATES 스키마만).
- [x] **1-2.** 클래스·속성 설계표 작성 — 각 클래스의 식별자, 속성(데이터 속성/객체 속성), 도메인/범위. 산출물: `ontology/design.md` 또는 별도 표.

### 2. 확장 온톨로지 작성

- [x] **2-1.** RDF(Turtle) 또는 OWL로 온톨로지 파일 작성. 위치: `ontology/` (예: `evidence_kg_ontology.ttl` 또는 `.owl`).
- [x] **2-2.** 정의할 내용: Document, EvidenceChunk, Gene, Protein, Disease, Drug, Compound, Pathway, Phenotype, Assay 클래스; MENTIONS, ASSOCIATED_WITH, INHIBITS, ACTIVATES 속성(객체 속성); 필요 시 데이터 속성(제목, 식별자 등).

### 3. 저장소 선택 및 스키마 반영

- [x] **3-1.** 저장소 결정: **Neo4j** 또는 **PostgreSQL** 중 하나 선택.
- [x] **3-2.** 선택한 저장소에 맞는 스키마/그래프 모델 설계 — 노드 레이블(또는 테이블), 관계(또는 FK), 속성 컬럼.  
  → **산출물**: [docs/neo4j-schema.md](docs/neo4j-schema.md) (노드 레이블·프로퍼티, 관계 타입·방향, 인덱스 권장).

### 4. 변환·로드 스크립트

- [ ] **4-0.** **(선택) 관계 추출** — 초록/본문 텍스트에서 relation extractor를 돌려 ASSOCIATED_WITH / INHIBITS / ACTIVATES 레코드를 생성. 산출물: `data/relations.jsonl` (input-format §3.1 포맷). 이 단계를 생략하면 `build_relations_jsonl.py`처럼 MeSH 쌍만으로 ASSOCIATED_WITH만 생성할 수 있음. INHIBITS·ACTIVATES를 쓰려면 이 단계에서 추출기 또는 외부 KG 매핑 필요.
- [x] **4-1.** 입력 데이터 형식 정의 — 추출기 출력 JSON 또는 시뮬레이션 CSV/JSON (Document, EvidenceChunk, 개체, MENTIONS/ASSOCIATED_WITH 등).  
  → **산출물**: [docs/input-format.md](docs/input-format.md) (원천 JSON 매핑, 관계 레코드 포맷: pmid, evidence_chunk_id 확정).
- [x] **4-2.** 변환 스크립트 작성 — RDF 또는 JSON → Neo4j/PostgreSQL. 위치: `scripts/` (예: `load_to_neo4j.py` 또는 `load_to_postgres.py`).
- [x] **4-3.** 데이터 로드 실행 — 50~200건 수준 권장. 로드 후 노드/관계 수 확인.

### 5. 예제 쿼리 작성·실행

- [ ] **5-1.** 쿼리 1: Document 중 특정 Gene(또는 Disease/Drug)을 MENTIONS하는 문서 조회. 저장: `queries/mentions_by_entity.cypher` 또는 `.sql`.
- [ ] **5-2.** 쿼리 2: 특정 Disease와 ASSOCIATED_WITH인 Drug 조회. 저장: `queries/associated_drugs.cypher` 또는 `.sql`.
- [ ] **5-3.** 쿼리 3: EvidenceChunk별 MENTIONS 집계(또는 문서별 개체 수). 저장: `queries/mentions_aggregate.cypher` 또는 `.sql`.
- [ ] **5-4.** 각 쿼리 실행해 결과 확인.

### 이제 해야 할 작업 (순서대로)

| 순서 | 할 일 | README 위치 |
|------|--------|-------------|
| **2-1** | RDF(Turtle) 또는 OWL 온톨로지 파일 작성. `ontology/evidence_kg_ontology.ttl` (또는 .owl). design.md 클래스·속성 반영. | §2 확장 온톨로지 |
| **2-2** | (2-1과 함께) Document, EvidenceChunk, Gene~Assay 클래스, MENTIONS/ASSOCIATED_WITH/INHIBITS/ACTIVATES 속성, 데이터 속성 정의. | §2 |
| **3-1** | 저장소 결정: **Neo4j** 또는 **PostgreSQL** 중 하나 선택. | §3 저장소 |
| **3-2** | 선택한 저장소용 스키마 설계 (노드 레이블 또는 테이블, 관계/FK, 속성 컬럼). | §3 |
| **4-0** | (선택) 관계 추출. 초록/본문에서 INHIBITS·ACTIVATES 추출 → `data/relations.jsonl`. 생략 시 MeSH 쌍만으로 ASSOCIATED_WITH만 생성 가능. | §4 변환·로드 |
| **4-1** | 입력 데이터 형식 정의 (우리 JSON 구조를 Document/EvidenceChunk/개체/MENTIONS에 어떻게 매핑할지 문서화). | §4 변환·로드 |
| **4-2** | 변환 스크립트 작성. `data/pubmed_*.json` → Neo4j 또는 PostgreSQL. `scripts/` (예: load_to_neo4j.py 등). | §4 |
| **4-3** | 스크립트 실행해 데이터 로드, 노드/관계 수 확인. | §4 |
| **5-1** | 쿼리 1: 특정 Gene/Disease/Drug를 MENTIONS하는 Document 조회. `queries/mentions_by_entity.*` | §5 예제 쿼리 |
| **5-2** | 쿼리 2: 특정 Disease와 ASSOCIATED_WITH인 Drug 조회. `queries/associated_drugs.*` | §5 |
| **5-3** | 쿼리 3: EvidenceChunk별 MENTIONS 집계. `queries/mentions_aggregate.*` | §5 |
| **5-4** | 위 쿼리 실행해 결과 확인. | §5 |

PrimeKG를 쓸 경우: 위 흐름이 끝난 뒤(또는 4단계와 병렬로) ETL 개요의 **「4. (선택) 외부 KG 연동 시 ETL」** 순서대로 추가.

---

## **4-2 변환 스크립트 작업 순서**

### **1\. 환경·입력 정하기**

* Python: 3.8+ 가정.  
* Neo4j 드라이버: `pip install neo4j` (공식 드라이버). 또는 `py2neo` 사용 가능.  
* 입력 파일  
* 필수: `data/pubmed_distributed_200_cleansed.json` (문서 배열).  
* 선택: `data/relations.jsonl` (ASSOCIATED\_WITH/INHIBITS/ACTIVATES용). 없으면 1차에는 문서·청크·MENTIONS만 로드.

스크립트는 `02-intermediate/scripts/load_to_neo4j.py` 하나로 두고, 인자로 JSON 경로(와 선택적으로 relations.jsonl 경로)를 받도록 하면 됩니다.

---

### **2\. 스크립트 골격**

* `argparse`로 다음만 받으면 충분합니다.  
* `--pubmed-json` (기본: `data/pubmed_distributed_200_cleansed.json`)  
* `--relations` (선택: `data/relations.jsonl`)  
* `--neo4j-uri`, `--user`, `--password` (기본값 또는 환경변수)  
* `neo4j.GraphDatabase.driver(uri, auth=(user, password))` 로 연결.  
* 끝날 때 `driver.close()`.

---

### **3\. 인덱스/제약 (한 번만 실행해도 되게)**

* `run()`으로 다음을 실행하는 함수 하나 만듦.  
* `Document(pmid)` 유니크 제약 또는 유니크 인덱스  
* `EvidenceChunk(chunk_id)` 유니크 제약 또는 유니크 인덱스  
* 생물의학 노드는 레이블이 많으므로, 우선은 “필요 시 나중에” 두고, 1차에는 `MERGE (n:Label {name: $name})` 만 해도 됨.  
* 스크립트 시작 시 “제약/인덱스 설정” 단계를 한 번 호출하거나, `CREATE CONSTRAINT ... IF NOT EXISTS` 형태로 넣어 두면 됨.

---

### **4\. PubMed JSON → 노드·관계 (트랜잭션 단위)**

한 트랜잭션에서 “한 문서” 또는 “N개 문서”씩 처리하면 됨.4-1. Document 노드

* JSON 한 건당 `(pmid, title, pub_date)` 로

`MERGE (d:Document {pmid: $pmid}) SET d.title = $title, d.pub_date = $pub_date`

* `pmid`가 없으면 스킵.

4-2. EvidenceChunk 노드

* 같은 문서에 대해 `chunk_id = f"{pmid}_chunk_0"`, `hasText = abstract`

`MERGE (c:EvidenceChunk {chunk_id: $chunk_id}) SET c.hasText = $hasText`

* 문서당 1청크 규칙 유지.

4-3. HAS\_CHUNK 관계

* `MATCH (d:Document {pmid: $pmid}), (c:EvidenceChunk {chunk_id: $chunk_id}) MERGE (d)-[:HAS_CHUNK]->(c)`  
* 프로퍼티 없음.

4-4. mesh\_terms → 엔티티 노드 \+ MENTIONS

* `mesh_terms`는 MeSH 문자열 배열이므로, “어떤 레이블로 쓸지”를 한 번 정해야 함.  
* 간단한 방법: 모든 MeSH를 한 레이블로 (예: `Phenotype` 또는 `Assay`) MERGE하고, Document 또는 EvidenceChunk에서 MENTIONS 생성.  
* 조금 구분하는 방법: 미리 작은 매핑 테이블을 두고 (예: "Neoplasms" → Disease, "Metabolic Networks and Pathways" → Pathway), 나머지는 Phenotype 등 기본 레이블.  
* 각 mesh 문자열에 대해:  
* `MERGE (e:Label {name: $name})` (Label은 위에서 정한 규칙대로).  
* `(Document {pmid}) -[:MENTIONS]-> (e)` 또는 `(EvidenceChunk {chunk_id}) -[:MENTIONS]-> (e)`  
* MENTIONS는 관계 프로퍼티 없음 (input-format, neo4j-schema 준수).

Document 기준으로 MENTIONS를 만들지, EvidenceChunk 기준으로 만들지는 설계 선택. 한쪽만 하면 “문서가 언급” / “청크가 언급” 중 하나로 통일됨.(권장: EvidenceChunk → Entity 로 MENTIONS를 두면, 나중에 evidence\_chunk\_id와도 맞추기 좋음.)

---

### **5\. relations.jsonl 처리 (선택)**

* 파일이 있으면: 한 줄씩 읽어 `json.loads(line)` → `type`, `from_entity_type`, `from_entity_name`, `to_entity_type`, `to_entity_name`, `pmid`, (선택) `evidence_chunk_id`.  
* `type`이 ASSOCIATED\_WITH / INHIBITS / ACTIVATES일 때만 처리.  
* `MERGE`로 from 노드, to 노드 찾기:

`MERGE (a:FromLabel {name: $from_name})`, `MERGE (b:ToLabel {name: $to_name})`.레이블은 `from_entity_type` / `to_entity_type` 문자열을 그대로 사용하면 됨 (Gene, Disease, Drug 등).

* 관계 생성 시:  
* `pmid`는 항상 프로퍼티로 설정.  
* `evidence_chunk_id`는 있을 때만 프로퍼티에 넣고, 없으면 omit (neo4j-schema, input-format 규칙).  
* Cypher 예:

`MERGE (a:LabelFrom {name: $from_name}) MERGE (b:LabelTo {name: $to_name}) MERGE (a)-[r:REL_TYPE]->(b) SET r.pmid = $pmid`그리고 `evidence_chunk_id`가 있을 때만 `SET r.evidence_chunk_id = $evidence_chunk_id` 추가하거나, 파라미터로만 넘겨서 “있을 때만 SET” 하면 됨.

---

### **6\. 실행 순서 정리**

1. 드라이버 연결.  
1. 제약/인덱스 설정 (한 번).  
1. PubMed JSON 로드 → Document → EvidenceChunk → HAS\_CHUNK → (mesh\_terms → 엔티티 MERGE \+ MENTIONS).  
1. (선택) relations.jsonl 있으면 위 규칙으로 ASSOCIATED\_WITH/INHIBITS/ACTIVATES 생성.  
1. 마지막에 노드 수·관계 수 세기 (예: `MATCH (n) RETURN count(n)`, `MATCH ()-[r]->() RETURN count(r)`)해서 출력.  
1. `driver.close()`.

---

### **7\. 확인용 출력**

* 로드한 Document 수, EvidenceChunk 수, MENTIONS 수, (있으면) ASSOCIATED\_WITH/INHIBITS/ACTIVATES 수.  
* 50\~200건 권장이므로, `--limit 200` 같은 옵션을 두고 테스트해도 됨.

---

### **8\. 참고할 문서**

* 노드/관계 정의: `docs/neo4j-schema.md` (노드 레이블·프로퍼티, 관계 타입·방향, 관계 프로퍼티).  
* 입력 형식: `docs/input-format.md` (§1 원천 JSON, §2 노드 매핑, §3.1 관계 레코드, evidence\_chunk\_id omit 규칙).  
* 설계 근거: `ontology/design.md` (관계 출처는 Neo4j만, ttl에는 넣지 않음).

이 순서대로 구현하면 “RDF 또는 JSON → Neo4j” 4-2 요구사항을 충족하는 변환 스크립트를 직접 작성할 수 있습니다.원하면 `load_to_neo4j.py`의 함수별 목차(예: `def create_constraints`, `def load_pubmed`, `def load_relations`)까지 나눠서 쓸 수 있다.

---

## 사용 도구

- **저장소**: Neo4j (3-1 선택). 스키마: [docs/neo4j-schema.md](docs/neo4j-schema.md).
- **언어**: Python (rdflib, py2neo 또는 psycopg2 등).
- **참고**: `../docs/domain-evidence-kg-level-mapping.md` — 중급 범위 요약.

### Neo4j 설치 및 실행 (Docker)

4-2·4-3(변환 스크립트 실행, 데이터 로드)를 하려면 Neo4j 서버가 떠 있어야 한다. 로컬에서 Docker로 띄우는 방법이다.

**방법 1: `docker run` 한 줄**

```bash
docker run -d --name neo4j-intermediate \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/your-password \
  neo4j:latest
```

- **7474**: 브라우저 UI (http://localhost:7474)
- **7687**: Bolt (스크립트 연결용 `neo4j://localhost:7687`)
- `your-password`를 원하는 비밀번호로 바꾼 뒤, 로드 스크립트의 `--password`에도 동일하게 넣는다.

**방법 2: docker-compose**

프로젝트 루트 또는 `02-intermediate/`에 `docker-compose.yml`을 두고:

```yaml
services:
  neo4j:
    image: neo4j:latest
    ports:
      - "7474:7474"
      - "7687:7687"
    environment:
      NEO4J_AUTH: neo4j/your-password
```

실행: `docker-compose up -d`. 중지: `docker-compose down`.

---

## 데이터

- **종류**: 추출 파이프라인 출력 또는 시뮬레이션 JSON/CSV.
- **내용**: Document, EvidenceChunk, Gene/Protein/Disease/Drug/Pathway/Phenotype/Assay 인스턴스, MENTIONS·ASSOCIATED_WITH 관계.
- **건수**: 50~200건 권장.

---

## ETL 개요 (순서)

PubMed JSON → 저장소(Neo4j/PostgreSQL) 파이프라인과, **PrimeKG** 등 외부 KG 사용 시 ETL 순서입니다.

### 1. Extract (추출)

| 순서 | 대상 | 내용 |
|------|------|------|
| 1-1 | PubMed | `data/pubmed_*.json` (또는 data-fetch/output, cleaned) 읽기. Document·EvidenceChunk·mesh_terms 등 추출. |
| 1-2 | (선택) 관계 추출 | 초록/청크 텍스트에서 NER + relation extractor 실행 → `data/relations.jsonl` (type: ASSOCIATED_WITH / INHIBITS / ACTIVATES). 생략 시 MeSH 쌍만으로 ASSOCIATED_WITH만 생성(예: build_relations_jsonl.py). |
| 1-3 | (선택) PrimeKG | Harvard Dataverse 등에서 kg.csv 또는 nodes.tab + edges.csv 다운로드 후 파싱. |

### 2. Transform (변환)

| 순서 | 작업 | 내용 |
|------|------|------|
| 2-1 | 노드 생성 | JSON의 pmid → Document. pmid_chunk_0 + abstract → EvidenceChunk. mesh_terms → Gene/Disease/Drug/Pathway 등 개체 노드(MeSH→클래스 매핑 적용). |
| 2-2 | 관계 생성 | Document/EvidenceChunk ↔ 개체 → MENTIONS. (선택) relations.jsonl → ASSOCIATED_WITH, INHIBITS, ACTIVATES. (선택) PrimeKG 엣지 → 동일 관계 타입 매핑. |
| 2-3 | 식별자·속성 정규화 | design.md의 식별자(pmid, pmid_chunk_0, name 등)와 데이터 속성(title, pub_date 등) 반영. |

### 3. Load (적재)

| 순서 | 대상 | 내용 |
|------|------|------|
| 3-1 | 스키마 준비 | Neo4j: 레이블·관계 타입. PostgreSQL: 테이블·FK 정의. |
| 3-2 | 노드 적재 | Document, EvidenceChunk, 개체(Gene, Disease, …) 순으로 INSERT/CREATE. |
| 3-3 | 관계 적재 | MENTIONS, (선택) ASSOCIATED_WITH, INHIBITS, ACTIVATES 적재. |
| 3-4 | 검증 | 노드/관계 수, 샘플 쿼리로 확인. |

### 4. (선택) 외부 KG 연동 시 ETL

PrimeKG 사용 시 추가 단계:

| 순서 | 단계 | 내용 |
|------|------|------|
| 4-1 | Extract | PrimeKG kg.csv(또는 nodes.tab + edges.csv) 다운로드·파싱. |
| 4-2 | Transform | PrimeKG node_type → 우리 클래스 매핑. relation → ASSOCIATED_WITH / INHIBITS / ACTIVATES 매핑. (선택) PubMed 개체 ↔ PrimeKG node_id 매핑. |
| 4-3 | Load | 변환된 PrimeKG 노드·엣지를 동일 저장소에 적재(기존 Document/MENTIONS와 공존). |


---

## 개체 추출: MeSH vs NER

문헌에서 **Gene, Protein, Disease, Drug** 같은 개체를 얻는 방법은 크게 두 가지입니다. 둘 다 이해해 두면 데이터 설계(design.md)와 변환 스크립트 작성에 도움이 됩니다.

### NER (Named Entity Recognition)

- **뜻**: 텍스트에서 의미 있는 개체(엔티티)를 **자동으로 찾아 분류**하는 기술.
- **입력**: 문장·문단 같은 자유 텍스트.
- **출력**: “여기서부터 여기까지가 Disease”, “이 구간은 Gene”처럼 **위치 + 타입**으로 표시된 엔티티 목록.

**예시**  
문장: *"BRCA1 mutation increases risk of breast cancer and ovarian cancer."*

| 추출된 엔티티 | 타입   | 텍스트 위치        |
|---------------|--------|---------------------|
| BRCA1         | Gene   | 문장 앞부분         |
| breast cancer | Disease| 문장 중간           |
| ovarian cancer| Disease| 문장 뒷부분         |

→ NER은 **초록·본문 문자열**을 넣으면 그 안에 등장하는 유전자명, 질병명, 약물명 등을 자동으로 찾아줍니다.

---

### MeSH (Medical Subject Headings)

- **뜻**: PubMed/의학 문헌에 **사람이 붙인 표준 주제어** 체계. NER이 아니라 “이 논문은 이런 주제다”라고 할당된 **레이블 목록**.
- **입력**: 논문 메타데이터(제목·초록 등)를 보고 **인덱서(또는 시스템)**가 MeSH 용어를 선택.
- **출력**: 논문 단위로 부여된 MeSH 용어 리스트(우리 JSON의 `mesh_terms`).

**예시**  
같은 논문에 부여된 MeSH가 `["Neoplasms", "BRCA1 Protein", "Genetic Predisposition to Disease"]` 라면:

- **Neoplasms** → Disease(질병) 계열로 매핑 가능.
- **BRCA1 Protein** → Protein/Gene 계열로 매핑 가능.
- **Genetic Predisposition to Disease** → Phenotype/Pathway 등으로 해석 가능.

→ MeSH는 **논문 전체**에 대한 주제이므로, “이 문장의 이 단어가 Disease” 같은 **위치 정보는 없습니다**. 대신 표준 용어라서 **외부 DB(DO, GO 등)와 매핑**하기 좋습니다.

---

### 비교 요약

| 구분       | NER                          | MeSH                         |
|------------|------------------------------|------------------------------|
| **역할**   | 텍스트에서 개체를 **자동 추출** | 논문에 **표준 주제어 부여**   |
| **단위**   | 문장·구·단어(위치 있음)       | 논문 단위(위치 없음)          |
| **출처**   | 초록·본문 **텍스트**          | PubMed 메타데이터 `mesh_terms` |
| **예시**   | "BRCA1" → Gene, "breast cancer" → Disease | "Neoplasms", "BRCA1 Protein" |
| **중급에서** | design.md에서 “title·abstract 추출”로 적힌 개체의 원천. 고급 ETL에서 관계 추출과 함께 사용. | 이미 JSON에 있음. Disease/Pathway 등으로 매핑해 MENTIONS·노드로 사용. |

**정리**: 중급에서는 **MeSH(`mesh_terms`)만으로도** Document–개체(MENTIONS) 구조를 만들 수 있습니다. **NER**은 초록/본문에서 더 많은 Gene·Disease·Drug를 뽑고 싶을 때, 또는 고급에서 ETL(문헌→추출→KG)을 구축할 때 활용하면 됩니다.
