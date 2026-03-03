# 중급 도메인: 근거 중심 지식 그래프 (Evidence-based Knowledge Graph)

## 도메인 한 문장

**"생물의학 학술 문헌에 보고된 연구 결과와 그 근거를 구조화하는 근거 중심 지식 그래프"**

- 문헌 기반. 실험 결과/가설/주장 = "보고된 내용". 실제 실험 실행/실패는 제외.

## 문헌 계층

- **Document** — 논문
- **EvidenceChunk** — abstract / section 단위

## 생물의학 개체

- Gene, Protein, Disease, Drug/Compound, Pathway, Phenotype, Assay

## 관계

- **MENTIONS** — EvidenceChunk / Document가 개체를 언급
- **ASSOCIATED_WITH** — 개체 간 연관
- **INHIBITS / ACTIVATES** — 스키마에만 정의, 값은 추출 결과가 있으면 채움

## 이 폴더에 넣을 것 (작업 시)

- 확장 온톨로지 파일: `.ttl` 또는 `.owl` (클래스·속성 정의)
