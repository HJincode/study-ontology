# 초급 (Beginner) — 온톨로지 기본 개념

이 레벨에서 만들 예제의 목표와 필요한 파일만 정의합니다.
실제 코드는 이 디렉토리에 순서대로 추가하세요.

## 이 레벨에서 만들 것
- **목표**: 클래스·인스턴스·속성의 정의 방법 이해.
- **산출물**: 소규모 온톨로지(클래스 5~10개), 샘플 데이터(CSV/JSON), RDF/OWL 파일 + 로드·검증 스크립트.

## 필요한 파일/폴더 (틀)
- `ontology/` — 온톨로지 정의 파일 (.owl, .ttl)
- `data/` — 샘플 데이터 (CSV, JSON)
- `scripts/` — 로드·검증 스크립트

## 작업 순서 (이 레벨만)
1. 도메인 정하기 → 2. 클래스·속성 설계 → 3. RDF/OWL 작성 → 4. 샘플 데이터 준비 → 5. 로드·검증 스크립트 작성

---

## 1번부터 순서대로 하는 방법

### 1. 도메인 정하기

**목표**: 이 온톨로지가 다룰 “세계”를 한 문장으로 정하고, 그 안에 나올 “주요 개념(엔티티)”을 나열한다.

**할 일**  
1. **도메인 이름 정하기** — 예: “PubMed 논문 메타데이터” 또는 “학술 논문·저자·저널·주제어”.  
2. **범위 정하기** — 이 예제: **논문(Article)** 과 그에 딸린 **저자(Author), 저널(Journal), MeSH 주제어(MeSHTerm)** 만 다룸. 원문·인용·기관은 초급에서 제외.  
3. **한 줄로 정리** — 예: *“도메인: 학술 논문 메타데이터 — 논문(Article), 저자(Author), 저널(Journal), MeSH 주제어(MeSHTerm).”*  
4. **문서로 남기기** — `01-beginner/ontology/domain.md` 를 만들고 위 한 줄 + “포함/제외” 2~3줄 적기.

**이 예제에서 쓸 도메인 (그대로 사용 가능)**  
- **도메인**: PubMed 기반 학술 논문 메타데이터.  
- **다루는 개념**: 논문(Article), 저자(Author), 저널(Journal), MeSH 주제어(MeSHTerm).  
- **데이터**: `data/pubmed_protein_structure_enzyme_10_cleansed.json` (10건).

---

### 2. 클래스·속성 설계  
클래스(Article, Author, Journal, MeSHTerm)와 속성(hasTitle, hasAuthor, publishedIn, hasMeSH 등)을 표로 정리. 산출물: `ontology/design.md` 또는 검토 문서의 매핑 표 참고.

### 3. RDF/OWL 작성  
설계를 `ontology/` 폴더에 `.ttl` 또는 `.owl` 파일로 작성 (클래스·속성 정의).

### 4. 샘플 데이터 준비  
이미 `data/pubmed_protein_structure_enzyme_10_cleansed.json` 있음. 추가 준비 없음.

### 5. 로드·검증 스크립트 작성  

`scripts/` 에 JSON을 읽어 온톨로지 인스턴스로 변환 후 로드·검증하는 스크립트 작성 (예: `load_and_validate.py`).

#### 1단계: 환경 준비

- **위치**: `01-beginner/scripts/` 에서 작업.
- **필요 패키지**: `rdflib` (RDF 로드/생성/검증용). `pip install rdflib` 로 설치.
- **파일**: 예) `load_and_validate.py` 하나 만들기.

#### 2단계: 스크립트에서 할 일 (순서대로 구현)

1. **경로·입력 설정**
   - `01-beginner/data/pubmed_protein_structure_enzyme_10_cleansed.json` 경로를 변수로 두기 (스크립트 기준 상대 경로 권장).
   - `01-beginner/ontology/pubmed_ontology.ttl` 경로를 변수로 두기.

2. **온톨로지 로드**
   - `rdflib.Graph()` 로 그래프 하나 생성.
   - `graph.parse(ontology_ttl_path, format="turtle")` 로 .ttl 파싱 (스키마만 로드).

3. **JSON 로드**
   - `json.load(open(data_json_path, encoding="utf-8"))` 로 10건 리스트 로드.

4. **URI 설계 (인스턴스 식별자)**
   - **Article**: `ex:Article/<pmid>` (예: `http://example.org/pubmed-ontology#Article/34813064`).
   - **Author**: `ex:Author/<lastname>_<forename>` 형태로 한 문자열 만들어서 사용 (공백은 `_` 등으로 치환). 같은 문자열이면 같은 Author 인스턴스.
   - **Journal**: `ex:Journal/<저널명>` (저널명을 URL-safe 하게 인코딩).
   - **MeSHTerm**: `ex:MeSHTerm/<MeSH문자열>` (문자열을 URL-safe 하게 인코딩).
   - 접두사 `ex`는 `pubmed_ontology.ttl`의 `ex:` 와 동일한 URI로 맞추기.

5. **RDF 트리플 생성 (JSON → RDF)**  
   각 논문(객체)에 대해:
   - Article 인스턴스 URI에 `rdf:type ex:Article` 추가.
   - `ex:hasTitle`, `ex:hasAbstract`, `ex:hasPubDate` 는 리터럴로 추가 (문자열).
   - `authors[]` 각 항목에 대해 Author URI 만들고, `ex:hasAuthor` 로 Article → Author 연결.
   - Journal URI 하나 만들고, `ex:publishedIn` 로 Article → Journal 연결.
   - `mesh_terms[]` 각 항목에 대해 MeSHTerm URI 만들고, `ex:hasMeSH` 로 Article → MeSHTerm 연결.
   - Author/Journal/MeSHTerm 노드에는 해당 URI에 대해 `rdf:type ex:Author`, `ex:Journal`, `ex:MeSHTerm` 각각 한 번씩만 넣으면 됨 (같은 URI가 여러 번 나와도 트리플은 한 번이면 충분).

6. **같은 인스턴스 재사용**
   - 같은 저자(동일 lastname+forename), 같은 저널명, 같은 MeSH 문자열은 **같은 URI**를 쓰도록 해서 트리플만 추가하고 노드는 중복 생성하지 않기.

7. **검증(간단히)**
   - 로드 결과: `len(graph)` 로 트리플 수 출력 (0보다 크면 로드 성공).
   - 인스턴스 수: `ex:Article` 타입 개수 → 10개인지 확인.
   - (선택) rdflib로 온톨로지 스키마와 인스턴스 그래프를 합친 뒤, 필수 속성(예: Article마다 `ex:hasTitle` 존재 여부)을 SPARQL 또는 `graph.triples()` 로 확인.

8. **출력**
   - 터미널에 예: `"Loaded N triples, M Article instances."` 형태로 요약 출력.
   - (선택) 생성한 RDF를 `01-beginner/output/data_instances.ttl` 같은 파일로 `graph.serialize(destination=..., format="turtle")` 로 저장해 두면, 나중에 확인·재사용하기 좋음.

#### 체크리스트

- [x] JSON 경로·TTL 경로가 프로젝트 구조에 맞는지 확인.
- [x] Article 10개가 모두 RDF로 생성되는지 확인.
- [x] Author/Journal/MeSHTerm 은 중복 없이 URI 하나씩만 쓰는지 확인.
- [x] `ex:hasTitle`, `ex:hasAuthor`, `ex:publishedIn`, `ex:hasMeSH` 등 design.md·pubmed_ontology.ttl 과 동일한 속성 이름(접두사 포함)을 쓰는지 확인.

---

**요약**: 1번은 “도메인 + 포함 개념”을 정해 `domain.md`에 적는 것. 2→3→4→5 순서로 진행하면 됨.

### 6. 질의 스크립트 (ask.py)

`output/data_instances.ttl`이 생성된 뒤, 사용자가 논문을 질의할 수 있는 스크립트를 사용할 수 있다.

- **스크립트**: `scripts/ask.py`
- **실행**: `cd 01-beginner/scripts && python ask.py` (대화형) 또는 `python ask.py list`, `python ask.py mesh "Protein Engineering"` 등
- **질의 예시**: 어떤 질문을 입력하면 되는지 구체적인 예는 `scripts/ask_examples.md` 참고.

| 질의 유형 | 예시 입력 (CLI) |
|----------|------------------|
| 전체 목록 | `python ask.py list` |
| PMID로 찾기 | `python ask.py pmid 34813064` |
| MeSH로 찾기 | `python ask.py mesh "Protein Engineering"` |
| 저자로 찾기 | `python ask.py author Wongnate` |
| 저널로 찾기 | `python ask.py journal FEBS` |

## PubMed 사용 시 데이터 준비
- **API로 가져오기**만 하면 됨. PubMed E-utilities로 메타데이터(PMID, 제목, 저자, 저널, MeSH 등) 수집.
- **Cleansing**: 빈 값·공백·인코딩 정도만 정리하면 됨 (선택).
- **Chunking**: 필요 없음. 초급은 메타데이터 기반 온톨로지만 다루므로 초록을 쪼개지 않음.

**이 데이터로 초급 진행 가능한지 검토**: `../data-fetch/docs/beginner-readiness-review.md` 참고.  
권장 입력 데이터: `../data-fetch/output/pubmed_protein_structure_enzyme_10_cleansed.json` (필요 시 `01-beginner/data/`로 복사).
