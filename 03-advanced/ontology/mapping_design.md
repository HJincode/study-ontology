# 통합 설계 (고급) — 여기에 매핑·추론 설계를 채우세요

## 외부 온톨로지 매핑

| 우리 클래스 | 외부 온톨로지/DB | 매핑 방식 (예: equivalence, subClassOf) |
|-------------|-------------------|------------------------------------------|
| Gene | Gene Ontology (GO) | (작업 시 채우기) |
| Disease | Disease Ontology (DO) | (작업 시 채우기) |
| Drug | DrugBank 등 | (작업 시 채우기) |

## 추론 규칙 (예시)

- ASSOCIATED_WITH 전이: (작업 시 채우기)
- 간접 근거: Gene —ACTIVATES→ Pathway —ASSOCIATED_WITH→ Disease → (작업 시 채우기)

작업 시 위 내용을 구체화한 뒤 `ontology/` 통합 파일과 `rules/` 에 반영하세요.
