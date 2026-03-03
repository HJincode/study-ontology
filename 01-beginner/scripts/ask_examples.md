# ask.py 질의 예시

`01-beginner/scripts/ask.py`는 `output/data_instances.ttl`에 로드된 논문 메타데이터를 대상으로 질의할 수 있습니다.  
**먼저 `load_and_validate.py`를 실행해 `data_instances.ttl`을 생성해 두세요.**

---

## 실행 방법

- **대화형**: 인자 없이 실행하면 메뉴가 나옵니다.
  ```bash
  cd 01-beginner/scripts && python ask.py
  ```
- **CLI**: 질의 유형과 값을 인자로 넘깁니다.
  ```bash
  python ask.py list
  python ask.py pmid 34813064
  python ask.py mesh "Protein Engineering"
  python ask.py author Wongnate
  python ask.py journal FEBS
  ```
- **근거 함께 출력**: 각 결과가 **어떤 RDF 트리플(사실) 때문에 나왔는지** 근거를 남기려면 `--evidence` 옵션을 붙입니다.
  ```bash
  python ask.py --evidence mesh "Protein Engineering"
  python ask.py --evidence author Wongnate
  ```
  대화형 모드에서도 `python ask.py --evidence` 로 실행하면 같은 질의에 대해 근거가 함께 출력됩니다.

---

## 사용자가 할 수 있는 질의 예시

| 질의 유형 | 하고 싶은 질문 (예시) | 입력 방법 |
|----------|------------------------|-----------|
| **전체 목록** | "등록된 논문 전체 목록 보여줘" | 메뉴에서 `5` 선택 또는 `python ask.py list` |
| **PMID로 찾기** | "PMID 34813064 논문 정보 알려줘" | 메뉴에서 `1` 선택 후 `34813064` 입력 또는 `python ask.py pmid 34813064` |
| **MeSH로 찾기** | "Protein Engineering이 MeSH로 붙은 논문 찾아줘" | 메뉴에서 `2` 선택 후 `Protein Engineering` 입력 또는 `python ask.py mesh "Protein Engineering"` |
| **저자로 찾기** | "Wongnate가 저자인 논문 찾아줘" | 메뉴에서 `3` 선택 후 `Wongnate` 입력 또는 `python ask.py author Wongnate` |
| **저널로 찾기** | "FEBS가 들어간 저널에 실린 논문 찾아줘" | 메뉴에서 `4` 선택 후 `FEBS` 입력 또는 `python ask.py journal FEBS` |

---

## 구체적인 입력 예시 (복사해서 사용 가능)

- **전체 논문 10건 제목/PMID 보기**
  - 메뉴: `5`  
  - CLI: `python ask.py list`

- **특정 논문 상세 정보 (PMID)**
  - 메뉴: `1` → `34813064`  
  - CLI: `python ask.py pmid 34813064`

- **MeSH 키워드로 논문 찾기**
  - 메뉴: `2` → `Protein Engineering`  
  - CLI: `python ask.py mesh "Protein Engineering"`
  - 메뉴: `2` → `Enzyme Stability`  
  - CLI: `python ask.py mesh "Enzyme Stability"`

- **저자명으로 논문 찾기**
  - 메뉴: `3` → `Wongnate`  
  - CLI: `python ask.py author Wongnate`
  - 메뉴: `3` → `Nielsen`  
  - CLI: `python ask.py author Nielsen`

- **저널명으로 논문 찾기**
  - 메뉴: `4` → `FEBS`  
  - CLI: `python ask.py journal FEBS`
  - 메뉴: `4` → `Biochimica`  
  - CLI: `python ask.py journal Biochimica`

---

## 참고

- MeSH/저자/저널은 **부분 일치**로 검색됩니다 (대소문자 구분 없음).
- 데이터는 `pubmed_protein_structure_enzyme_10_cleansed.json` 기준 10건이므로, 위 키워드로 결과가 나오는 항목만 있습니다.
