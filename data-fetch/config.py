"""
PubMed 검색 카테고리 및 키워드 설정.
- 초급 예제: Protein Structure & Enzyme Engineering 등 소량 메타데이터.
- 중급 예제: Gene/Protein/Disease/Drug/Pathway가 풍부한 카테고리 (50~200건 권장).
- 고급 예제: ETL·관계추출(INHIBITS/ACTIVATES)·외부 온톨로지 매핑(GO/DO/DrugBank/PrimeKG)·추론에 적합한 카테고리.
"""

# 검색 결과 최대 건수
FETCH_LIMIT = 10

# 분배 모드(--distribute)에서 사용할 카테고리 목록. None이면 INTERMEDIATE_RECOMMENDED 사용.
# 예: FETCH_CATEGORIES = INTERMEDIATE_RECOMMENDED 또는 ADVANCED_RECOMMENDED
FETCH_CATEGORIES = None

# 중급 예제 추천 카테고리 (근거 중심 KG: MENTIONS, ASSOCIATED_WITH 채우기 좋음)
INTERMEDIATE_RECOMMENDED = [
    "Cancer Biology & Oncology",
    "Metabolic Disease & Obesity",
    "Neurodegenerative Diseases",
    "Protein Structure & Enzyme Engineering",
    "Omics & Systems Biology",
    "Antibody Engineering & Therapeutics",
]

# 고급 예제 추천 카테고리 (ETL·관계추출·GO/DO/DrugBank/PrimeKG 매핑·추론에 유리)
ADVANCED_RECOMMENDED = [
    "Cancer Biology & Oncology",
    "Metabolic Disease & Obesity",
    "Neurodegenerative Diseases",
    "Omics & Systems Biology",
    "Antibody Engineering & Therapeutics",
    "Cell & Molecular Mechanisms",
    "AI-based Modeling & Design",
    "Gene Editing & Viral Vectors",
    "Synthetic Biology & Metabolic Engineering",
]

# 카테고리별 검색어 (키워드 사이는 OR로 검색)
CATEGORIES = {
    "Protein Structure & Enzyme Engineering": [
        "protein structure",
        "protein folding",
        "protein stability",
        "thermostability",
        "enzyme stability",
        "enzyme kinetics",
        "catalytic efficiency",
        "substrate specificity",
        "catalytic mechanism",
        "protein engineering",
        "directed evolution",
        "site-directed mutagenesis",
        "saturation mutagenesis",
    ],
    "Cancer Biology & Oncology": [
        "cancer biology",
        "oncology",
        "neoplasm",
        "cancer signaling",
        "oncogenic signaling",
        "signal transduction",
        "tumor microenvironment",
        "tme",
        "immune checkpoint",
        "angiogenesis",
        "metastasis",
        "tumor invasion",
        "chemoresistance",
    ],
    "Metabolic Disease & Obesity": [
        "obesity",
        "type 2 diabetes",
        "metabolic syndrome",
        "glp-1",
        "glucagon-like peptide-1",
        "incretin mimetic",
        "insulin resistance",
        "adipose tissue biology",
        "nash",
        "nafld",
        "energy homeostasis",
    ],
    "Neurodegenerative Diseases": [
        "alzheimer's disease",
        "parkinson's disease",
        "neurodegeneration",
        "amyloid beta",
        "tau protein",
        "blood-brain barrier",
        "bbb penetration",
        "neuroinflammation",
        "microglia",
        "synaptic plasticity",
    ],
    "Omics & Systems Biology": [
        "genome sequencing",
        "genetic variation",
        "chromatin accessibility",
        "crispr screening",
        "protein-protein interaction",
        "ppi network",
        "post-translational modification",
        "ptm mapping",
        "rna sequencing",
        "scrnaseq",
        "gene expression profiling",
        "go enrichment",
        "systems biology modeling",
        "metabolic pathway analysis",
        "flux balance analysis",
        "network topology",
        "big data biology",
    ],
    "Antibody Engineering & Therapeutics": [
        "monoclonal antibody",
        "mab",
        "antibody engineering",
        "bispecific antibody",
        "multispecific antibody",
        "antibody-drug conjugate",
        "adc",
        "nanobody",
        "vhh",
        "single-domain antibody",
        "phage display",
        "affinity maturation",
        "humanization",
        "fc engineering",
        "adcc",
        "cdc",
    ],
    "Cell & Molecular Mechanisms": [
        "signal transduction",
        "receptor binding",
        "membrane receptor",
        "kinase cascade",
        "cell cycle regulation",
        "apoptosis",
        "autophagy",
        "protein-lipid interaction",
        "protein translocation",
        "extracellular matrix",
        "ecm remodeling",
        "cell adhesion",
        "transcription factor",
        "epigenetic regulation",
    ],
    "AI-based Modeling & Design": [
        "ai drug discovery",
        "computational drug design",
        "in silico screening",
        "virtual screening",
        "de novo drug design",
        "de novo protein design",
        "protein language model",
        "structure-based drug design",
        "molecular dynamics simulation",
    ],
    "Gene Editing & Viral Vectors": [
        "gene therapy",
        "viral vector",
        "aav vector",
        "adeno-associated virus",
        "lentivirus",
        "gene editing",
        "crispr-cas9",
        "prime editing",
        "base editing",
        "gene knock-in",
        "gene knockout",
        "ex vivo gene therapy",
    ],
    "Synthetic Biology & Metabolic Engineering": [
        "synthetic biology",
        "metabolic engineering",
        "cell factory",
        "strain engineering",
        "genetic circuit",
        "gene cluster",
        "biosynthesis pathway",
        "biocatalysis",
        "industrial enzyme production",
        "fermentation optimization",
    ],
}

def get_search_terms(category: str = "Protein Structure & Enzyme Engineering") -> list[str]:
    """지정 카테고리의 검색어 리스트 반환."""
    return CATEGORIES.get(category, [])

def get_query_string(category: str = "Protein Structure & Enzyme Engineering") -> str:
    """PubMed 검색용 쿼리 문자열 (OR 결합)."""
    terms = get_search_terms(category)
    return " OR ".join(f'"{t}"' for t in terms)
