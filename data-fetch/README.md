# PubMed 데이터 수집 (data-fetch)

초급/중급/고급 예제용 PubMed 논문 메타데이터를 **API로 수집**하는 폴더입니다.

**이 API가 주는 것**: `db=pubmed` 기준으로 **PMID**와 **메타데이터(제목, 초록, 저자, 저널, MeSH)** 만 제공합니다. 논문 **전체 원문(본문)** 은 없으며, 원문이 필요하면 PMC(`db=pmc`)를 사용해야 합니다. 온톨로지 구축(클래스·인스턴스·관계)에는 메타데이터만으로 충분합니다.

## 카테고리 및 건수

- **카테고리**: `config.py`의 `CATEGORIES`에 여러 카테고리 정의. **중급**은 `INTERMEDIATE_RECOMMENDED`, **고급**은 `ADVANCED_RECOMMENDED` 참고.
- **건수**: `config.FETCH_LIMIT` (기본 100). CLI에서 `-n`으로 변경 가능.

### 중급 예제 추천 카테고리

| 카테고리 | 설명 |
|----------|------|
| Cancer Biology & Oncology | Disease, Gene, Protein, Drug, Pathway 풍부 — MENTIONS/ASSOCIATED_WITH 예제에 적합 |
| Metabolic Disease & Obesity | Disease, Drug(GLP-1 등), Gene, Pathway |
| Neurodegenerative Diseases | Disease(AD, PD), Protein(amyloid, tau), Drug |
| Protein Structure & Enzyme Engineering | Protein, Gene (기존 초급용과 동일) |
| Omics & Systems Biology | Gene, Protein, Pathway, PPI |
| Antibody Engineering & Therapeutics | Protein(항체), Drug(ADC 등), Disease(타깃) |

### 고급 예제 추천 카테고리

ETL·외부 온톨로지 매핑(GO/DO/DrugBank/PrimeKG)·INHIBITS/ACTIVATES 추출·추론에 유리. `config.ADVANCED_RECOMMENDED` 참고. Cell & Molecular Mechanisms, AI-based Modeling & Design, Gene Editing & Viral Vectors, Synthetic Biology & Metabolic Engineering 등이 추가로 포함됨.

## 사용 방법

```bash
cd data-fetch
pip install -r requirements.txt
```

**기본 실행** (Protein Structure & Enzyme Engineering, FETCH_LIMIT건):

```bash
python fetch_pubmed.py
```

**카테고리 지정** (중급·고급 예제용 100건):

```bash
python fetch_pubmed.py "Cancer Biology & Oncology" -n 100
python fetch_pubmed.py "Metabolic Disease & Obesity" -n 100
python fetch_pubmed.py "Cell & Molecular Mechanisms" -n 100
```

**출력 파일 지정**:

```bash
python fetch_pubmed.py "Cancer Biology & Oncology" -n 50 -o output/pubmed_cancer_50.json
```

**분배 모드** — FETCH_LIMIT(또는 -n)을 지정 카테고리에 균등 분배해 수집: `python fetch_pubmed.py -d` 또는 `python fetch_pubmed.py -d -n 200`. `--distribute-categories advanced`면 고급 추천 카테고리 사용. 출력: `output/pubmed_distributed_<limit>.json` (각 논문에 `category` 필드 포함).

**사용 가능한 카테고리 목록 보기**:

```bash
python fetch_pubmed.py --list
```

출력 파일은 기본적으로 `output/pubmed_<카테고리명>_<limit>.json` 형식입니다 (예: `pubmed_cancer_biology_oncology_100.json`). **같은 이름의 파일이 이미 있으면** `_1`, `_2` … 를 붙여 새 파일로 저장합니다 (기존 파일 덮어쓰지 않음).

## 출력 스키마 (JSON 한 건 예시)

- `pmid`: PubMed ID  
- `title`: 논문 제목  
- `abstract`: 초록 (최대 2000자)  
- `authors`: `[{ "lastname", "forename" }, ...]`  
- `journal`: 저널명  
- `pub_date`: 게재일  
- `mesh_terms`: MeSH 용어 리스트  
- (분배 모드 `-d` 사용 시) `category`: 수집 시 사용한 카테고리명  

## 설정 변경

- **건수**: `config.py`에서 `FETCH_LIMIT` 수정, 또는 실행 시 `-n 200` 등으로 지정.
- **카테고리/검색어**: `config.py`의 `CATEGORIES` 수정.

## 초급/중급/고급 예제와 연동

- **초급**: 수집한 JSON을 `01-beginner/data/`로 복사해 로드·검증에 사용.
- **중급**: 수집한 JSON을 `02-intermediate/data/`로 복사해 변환·로드 스크립트 입력으로 사용 (50~200건 권장).
- **고급**: 다중 카테고리 수집 후 `03-advanced/data/`에서 ETL·외부 DB(PrimeKG 등)와 통합.

```bash
cp output/pubmed_cancer_biology_oncology_100.json ../02-intermediate/data/
cp output/pubmed_cell_molecular_mechanisms_100.json ../03-advanced/data/
```
