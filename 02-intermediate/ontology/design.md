# 확장 온톨로지 설계 (중급) — 여기에 클래스·속성 표를 채우세요

## 클래스 (예시)

| 클래스 | 설명 | 식별자 |
|--------|------|--------|
| Document | 논문 | (작업 시 채우기) |
| EvidenceChunk | abstract/section 단위 | (작업 시 채우기) |
| Gene | 유전자 | (작업 시 채우기) |
| Protein | 단백질 | (작업 시 채우기) |
| Disease | 질병 | (작업 시 채우기) |
| Drug | 약물 | (작업 시 채우기) |
| Pathway | 경로 | (작업 시 채우기) |
| Phenotype | 표현형 | (작업 시 채우기) |
| Assay | assay | (작업 시 채우기) |

## 객체 속성 (관계)

| 속성 | 도메인 | 범위 |
|------|--------|------|
| MENTIONS | EvidenceChunk / Document | Gene, Protein, Disease, ... |
| ASSOCIATED_WITH | (개체 간) | (작업 시 채우기) |
| INHIBITS | (스키마만) | (작업 시 채우기) |
| ACTIVATES | (스키마만) | (작업 시 채우기) |

작업 시 위 표를 완성한 뒤 RDF/OWL 파일로 옮기세요.
