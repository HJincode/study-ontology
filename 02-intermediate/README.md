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

- [ ] **1-1.** `ontology/domain.md` 확인 또는 수정 — 문헌 계층(Document, EvidenceChunk), 생물의학 개체(Gene, Protein, Disease, Drug, Pathway, Phenotype, Assay), 관계(MENTIONS, ASSOCIATED_WITH, INHIBITS/ACTIVATES 스키마만).
- [ ] **1-2.** 클래스·속성 설계표 작성 — 각 클래스의 식별자, 속성(데이터 속성/객체 속성), 도메인/범위. 산출물: `ontology/design.md` 또는 별도 표.

### 2. 확장 온톨로지 작성

- [ ] **2-1.** RDF(Turtle) 또는 OWL로 온톨로지 파일 작성. 위치: `ontology/` (예: `evidence_kg_ontology.ttl` 또는 `.owl`).
- [ ] **2-2.** 정의할 내용: Document, EvidenceChunk, Gene, Protein, Disease, Drug, Compound, Pathway, Phenotype, Assay 클래스; MENTIONS, ASSOCIATED_WITH, INHIBITS, ACTIVATES 속성(객체 속성); 필요 시 데이터 속성(제목, 식별자 등).

### 3. 저장소 선택 및 스키마 반영

- [ ] **3-1.** 저장소 결정: **Neo4j** 또는 **PostgreSQL** 중 하나 선택.
- [ ] **3-2.** 선택한 저장소에 맞는 스키마/그래프 모델 설계 — 노드 레이블(또는 테이블), 관계(또는 FK), 속성 컬럼.  
  → **산출물**: [docs/neo4j-schema.md](docs/neo4j-schema.md) (노드 레이블·프로퍼티, 관계 타입·방향, 인덱스 권장).

### 4. 변환·로드 스크립트

- [ ] **4-0.** **(선택) 관계 추출** — 초록/본문 텍스트에서 relation extractor를 돌려 ASSOCIATED_WITH / INHIBITS / ACTIVATES 레코드를 생성. 산출물: `data/relations.jsonl` (input-format §3.1 포맷). 이 단계를 생략하면 `build_relations_jsonl.py`처럼 MeSH 쌍만으로 ASSOCIATED_WITH만 생성할 수 있음. INHIBITS·ACTIVATES를 쓰려면 이 단계에서 추출기 또는 외부 KG 매핑 필요.
- [ ] **4-1.** 입력 데이터 형식 정의 — 추출기 출력 JSON 또는 시뮬레이션 CSV/JSON (Document, EvidenceChunk, 개체, MENTIONS/ASSOCIATED_WITH 등).  
  → **산출물**: [docs/input-format.md](docs/input-format.md) (원천 JSON 매핑, 관계 레코드 포맷: pmid, evidence_chunk_id 확정).
- [ ] **4-2.** 변환 스크립트 작성 — RDF 또는 JSON → Neo4j/PostgreSQL. 위치: `scripts/` (예: `load_to_neo4j.py` 또는 `load_to_postgres.py`). **`data/relations.jsonl`**을 `--relations` 인자로 넘기면 ASSOCIATED_WITH/INHIBITS/ACTIVATES 관계를 Neo4j에 적재한다.
- [ ] **4-3.** 데이터 로드 실행 — 50~200건 수준 권장. 로드 후 노드/관계 수 확인. 관계까지 넣으려면 **`data/relations.jsonl`**을 지정한 뒤 실행한다 (예: `python scripts/load_to_neo4j.py --relations data/relations.jsonl --password ...`).

**relations.jsonl 활용 흐름**

| 단계 | 역할 | relations.jsonl |
|------|------|------------------|
| **4-0** | (선택) 관계 추출 | `extract_relations.py` → `relations_extract.jsonl`. (선택) `build_relations_jsonl.py` → `relations_build.jsonl` 후 `merge_relations.py`로 합쳐 **`data/relations.jsonl`** 생성. |
| **4-2** | 변환 스크립트 | `load_to_neo4j.py`가 `--relations data/relations.jsonl`로 읽어 Neo4j에 ASSOCIATED_WITH/INHIBITS/ACTIVATES 엣지 적재. |
| **4-3** | 로드 실행 | 위 스크립트 실행 시 `--relations data/relations.jsonl`을 넘기면 해당 파일이 활용됨. |

- **포맷**: [docs/input-format.md](docs/input-format.md) §3.1 (type, from_entity_type/name, to_entity_type/name, pmid, evidence_chunk_id).
- **없을 때**: `--relations`를 생략하면 문서·청크·MENTIONS만 로드되고, 개체 간 관계(ASSOCIATED_WITH 등)는 0건이다.

### 5. 예제 쿼리 작성·실행

- [ ] **5-1.** 쿼리 1: Document 중 특정 Gene(또는 Disease/Drug)을 MENTIONS하는 문서 조회. 저장: `queries/mentions_by_entity.cypher` 또는 `.sql`.
- [ ] **5-2.** 쿼리 2: 특정 Disease와 ASSOCIATED_WITH인 Drug 조회. 저장: `queries/associated_drugs.cypher` 또는 `.sql`.
- [ ] **5-3.** 쿼리 3: EvidenceChunk별 MENTIONS 집계(또는 문서별 개체 수). 저장: `queries/mentions_aggregate.cypher` 또는 `.sql`.
- [ ] **5-4.** 각 쿼리 실행해 결과 확인.

### 6. 지식 그래프 활용 — 질의 & 가설 생성

구축된 근거 중심 지식 그래프를 **실제로 활용**하는 단계. 두 가지 스크립트를 작성한다.

#### 6-1. 지식 그래프 질의 (`scripts/ask.py`)

**사용자에게 질문을 받고**, **어떤 질문을 할 수 있는지 가이드를 제시**한 뒤, **질문에 대한 답**을 보여주는 CLI 스크립트.

- [ ] **6-1-1.** 질문 유형 정의 — 아래 3가지를 최소 지원.

| 질문 유형 | 예시 | 내부 동작 |
|-----------|------|-----------|
| **엔티티 → 문서** | "Neoplasms가 언급된 논문은?" | 엔티티 이름으로 MENTIONS 역추적 → Document 목록 반환. |
| **엔티티 → 관계** | "Obesity와 연관된 것은?" | 엔티티 이름으로 ASSOCIATED_WITH/INHIBITS/ACTIVATES 탐색 → 연결된 노드 + 관계 타입 반환. |
| **두 엔티티 관계** | "Obesity하고 Insulin Resistance 관계는?" | 두 엔티티 간 직접 관계 조회 → 관계 타입 + 근거 문헌(pmid) 반환. |

- [ ] **6-1-2.** 동작 흐름.

  1. **가이드 제시** — 실행 시(또는 `--guide`) "어떤 질문을 할 수 있는지" 3가지 유형과 예시 문장을 출력.
  2. **질문 받기** — `--question "질문"` 으로 한 번에 넘기거나, 인자 없이 실행하면 대화형으로 "질문을 입력하세요" 프롬프트 후 입력 받기.
  3. **답 보여주기** — 질문 문자열을 파싱해 유형(mentions/relations/between)과 엔티티를 추출한 뒤, 해당 Cypher 실행 결과를 테이블 형태로 출력.

- [ ] **6-1-3.** 사용법.

```
# 가이드만 보기
python scripts/ask.py --guide

# 질문 한 줄로 넘기기
python scripts/ask.py --question "Neoplasms가 언급된 논문은?"
python scripts/ask.py -q "Obesity와 연관된 것은?"
python scripts/ask.py -q "Obesity하고 Insulin Resistance 관계는?"

# 대화형 (가이드 출력 후 질문 입력 반복, 종료: q)
python scripts/ask.py

# 기존 방식 유지 (--type + --entity / --from --to)
python scripts/ask.py --type mentions --entity "Neoplasms"
```

- [ ] **6-1-4.** 작업 순서.
  1. 가이드 상수(문자열) 정의 — 3가지 질문 유형과 예시.
  2. 질문 파싱: "A가 언급된 논문", "A와 연관된 것", "A하고 B 관계" 등 패턴으로 유형·엔티티 추출.
  3. Neo4j 연결 후 유형별 Cypher 실행, 결과를 테이블로 출력.
  4. `--guide` / `--question` / 인자 없이(대화형) 동작 구현.
- [ ] **6-1-5.** 실행 테스트 — 가이드 출력, 질문 3가지 유형별 답 확인.

#### 6-2. 가설 생성 & 문헌 증명 (`scripts/create_hypothesis.py`)

**사용자가 연구 주제를 입력**하면, **그 주제에 맞는 문서**를 기반으로 **새로운 가설 후보**를 생성하고, **각 가설이 어떤 문서들을 이용해 만들어졌는지 근거**를 제시하는 CLI 스크립트.

- [ ] **6-2-1.** 가설 생성 로직 정의.

| 단계 | 하는 일 |
|------|---------|
| ① 연구 주제 입력 | 사용자가 `--topic "cancer immunotherapy"` 또는 `--topic "obesity metabolism"` 처럼 **연구 주제**(키워드/문구) 지정. |
| ② 주제에 맞는 문서 선정 | Document의 title(또는 EvidenceChunk.hasText)에서 주제 키워드가 포함된 문서만 필터. 예: title 또는 hasText에 "cancer", "immunotherapy" 등 포함된 pmid 목록 조회. |
| ③ 해당 문서에서 가설 후보 생성 | 위에서 얻은 문서(pmid 집합)에 **출처로 달린** 관계만 사용. 즉, ASSOCIATED_WITH/INHIBITS/ACTIVATES 엣지 중 `r.pmid`가 해당 집합에 들어가는 것만 추출 → 각 `(엔티티 A)–[관계 타입]–(엔티티 B)` 를 가설 후보로 정리. |
| ④ 근거 수집 | 각 가설(엣지)에 달린 `pmid` → Document(제목), EvidenceChunk(청크 텍스트) 조회. **이 가설을 만드는 데 사용된 문서 목록**을 근거로 제시. |
| ⑤ 출력 | 가설별로 "가설 문장 + **이 가설을 뒷받침하는 문서 목록(PMID, 제목, 청크 발췌)**" 형태로 출력. |

- [ ] **6-2-2.** 스크립트 골격 작성 — `scripts/create_hypothesis.py`.

```
사용법:
  python scripts/create_hypothesis.py --topic "cancer immunotherapy"
  python scripts/create_hypothesis.py --topic "obesity" --limit 10
```

- [ ] **연구 주제 예시** — `--topic`에 넣을 수 있는 연구 주제와, 해당 시 예상되는 문헌·질문 예시.

**1. Tumor microenvironment(TME)과 면역 치료**

- **포함 문헌**: Cancer Biology & Oncology 위주 (약 34편).  
  예: "Cancer metabolic reprogramming and immune response", "CAFs and immune cells in TME", "TAM polarization in cancer immunotherapy", "Immune evasion in HCC" 등.
- **핵심 개념**: Tumor microenvironment, immune evasion, cancer-associated fibroblasts(CAFs), tumor-associated macrophages(TAMs), immunotherapy, immune checkpoint, metabolic reprogramming.
- **가능한 연구 질문**  
  - TME·면역 관련해서 어떤 Disease/Pathway/Phenotype이 가장 자주 공동 언급되는가?  
  - 문헌 기반으로 "TME → immune evasion" 또는 "metabolism → immunotherapy response" 같은 관계를 그래프로 요약할 수 있는가?

**2. 대사 경로(Metabolic pathways)와 질병: 암·비만·신경퇴행**

- **포함 문헌**: Cancer(대사 재편), Metabolic Disease & Obesity(GLP-1, obesity), Neurodegenerative Diseases(알츠하이머·신경염증)를 묶어서 봄.
- **핵심 개념**: Metabolic Networks and Pathways, Energy Metabolism, Lipid Metabolism, insulin resistance, neuroinflammation, metabolic syndrome.
- **가능한 연구 질문**  
  - "Metabolic pathway" 또는 "Energy metabolism"가 암 / 비만·대사질환 / 신경퇴행 문헌에서 각각 어떤 개체(Disease, Drug, Phenotype)와 ASSOCIATED_WITH로 연결되는가?  
  - 세 질병 영역을 하나의 지식 그래프로 넣고, 공통·차별 경로를 비교.

**3. 항체·단백질 기반 치료 전략 (암·표적 치료)**

- **포함 문헌**: Antibody Engineering & Therapeutics(ADCs, single-domain antibody, humanization) + Cancer Biology(immunotherapy, targeted therapy) + Protein Structure & Enzyme Engineering(효소 안정화, 리간드 설계).
- **핵심 개념**: Antibodies Monoclonal/Bispecific, Immunoconjugates, Immune Checkpoint Inhibitors, Drug Resistance, enzyme stability, protein engineering.
- **가능한 연구 질문**  
  - "Monoclonal antibody" 또는 "Immune checkpoint inhibitor"가 어떤 Disease(Neoplasms 등) 및 Pathway와 함께 언급되는가?  
  - 문헌에서 추출한 Drug–Disease, Drug–Pathway 관계로 "어떤 치료 전략이 어떤 암/경로와 연결되는지" 요약.

- [ ] **6-2-3.** 작업 순서.
  1. argparse로 `--topic` (연구 주제 문자열), `--limit` (가설 개수 상한, 기본 예: 20), `--output` (선택) 인자 받기.
  2. Neo4j 드라이버 연결.
  3. 주제에 맞는 문서 조회:
     - 주제를 공백으로 split한 키워드 리스트로, Document.title 또는 EvidenceChunk.hasText에 **모든 키워드(또는 하나라도)** 포함된 Document의 pmid 집합 조회.  
     - 예: `MATCH (d:Document)-[:HAS_CHUNK]->(c:EvidenceChunk) WHERE toLower(d.title) CONTAINS toLower($keyword1) OR ... RETURN DISTINCT d.pmid`
  4. 해당 pmid 집합에 출처가 달린 관계만으로 가설 후보 수집:
     - `MATCH (a)-[r:ASSOCIATED_WITH|INHIBITS|ACTIVATES]-(b) WHERE r.pmid IN $pmids RETURN a.name, type(r), b.name, r.pmid` (중복 제거 후 가설 목록 생성).
  5. 각 가설(엔티티 A – 관계 – 엔티티 B)에 대해 근거 수집:
     - `MATCH (d:Document {pmid: $pmid})-[:HAS_CHUNK]->(c:EvidenceChunk) RETURN d.title, c.chunk_id, c.hasText`
  6. 출력 형식:
     ```
     [연구 주제] cancer immunotherapy

     === 가설 1 ===
     Tumor Microenvironment — ASSOCIATED_WITH — Macrophages
       (이 가설은 아래 문서들을 이용해 생성되었습니다.)

       [근거 1] PMID: 35844605
       제목: Shaping Polarization Of Tumor-Associated Macrophages ...
       청크: 35844605_chunk_0
       발췌: "..."

       [근거 2] PMID: 34635121
       ...
     ```
  7. (선택) `--output hypothesis_report.md` 인자로 마크다운 파일 저장 지원.
- [ ] **6-2-4.** 실행 테스트 — 연구 주제 1~2개로 실행해 "주제에 맞는 문서 → 가설 후보 → 근거 문서 목록"이 나오는지 확인.

### 이제 해야 할 작업 (순서대로)

| 순서 | 할 일 | README 위치 |
|------|--------|-------------|
| **2-1** | RDF(Turtle) 또는 OWL 온톨로지 파일 작성. `ontology/evidence_kg_ontology.ttl` (또는 .owl). design.md 클래스·속성 반영. | §2 확장 온톨로지 |
| **2-2** | (2-1과 함께) Document, EvidenceChunk, Gene~Assay 클래스, MENTIONS/ASSOCIATED_WITH/INHIBITS/ACTIVATES 속성, 데이터 속성 정의. | §2 |
| **3-1** | 저장소 결정: **Neo4j** 또는 **PostgreSQL** 중 하나 선택. | §3 저장소 |
| **3-2** | 선택한 저장소용 스키마 설계 (노드 레이블 또는 테이블, 관계/FK, 속성 컬럼). | §3 |
| **4-0** | (선택) 관계 추출. 초록/본문에서 INHIBITS·ACTIVATES 추출 → `data/relations.jsonl`. 생략 시 MeSH 쌍만으로 ASSOCIATED_WITH만 생성 가능. | §4 변환·로드 |
| **4-1** | 입력 데이터 형식 정의 (우리 JSON 구조를 Document/EvidenceChunk/개체/MENTIONS에 어떻게 매핑할지 문서화). | §4 변환·로드 |
| **4-2** | 변환 스크립트 작성. `data/pubmed_*.json` (+ 선택 `data/relations.jsonl`) → Neo4j. `scripts/load_to_neo4j.py` 등. | §4 |
| **4-3** | 스크립트 실행해 데이터 로드 (`--relations data/relations.jsonl`로 관계 포함 시). 노드/관계 수 확인. | §4 |
| **5-1** | 쿼리 1: 특정 Gene/Disease/Drug를 MENTIONS하는 Document 조회. `queries/mentions_by_entity.*` | §5 예제 쿼리 |
| **5-2** | 쿼리 2: 특정 Disease와 ASSOCIATED_WITH인 Drug 조회. `queries/associated_drugs.*` | §5 |
| **5-3** | 쿼리 3: EvidenceChunk별 MENTIONS 집계. `queries/mentions_aggregate.*` | §5 |
| **5-4** | 위 쿼리 실행해 결과 확인. | §5 |
| **6-1** | `scripts/ask.py` — 질문 받기, 가이드 제시, 답 보여주기 (3가지 질문 유형 지원). | §6 활용 |
| **6-2** | `scripts/create_hypothesis.py` — 연구 주제 입력 → 주제에 맞는 문서로 가설 생성 → 각 가설의 근거 문서 목록 제시. | §6 활용 |

PrimeKG를 쓸 경우: 위 흐름이 끝난 뒤(또는 4단계와 병렬로) ETL 개요의 **「4. (선택) 외부 KG 연동 시 ETL」** 순서대로 추가.

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
