# HCLS Skills Showcase for Cortex Code

A Snowflake-branded showcase page highlighting **21 purpose-built Health & Life Sciences (HCLS) skills** for [Cortex Code](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code) — Snowflake's AI-powered IDE.

## Live Site

**[View the Showcase](https://sfc-gh-jwarbington.github.io/hcls-skills-showcase/)**

## Skills Catalog

### Cross-Domain (6 skills)
| Skill | Description |
|-------|-------------|
| `hcls-cross-aiml-industrymodels` | Catalog and manage fine-tuned industry models (ICD coding, clinical NER) |
| `hcls-cross-cke-clinical-trials` | RAG-based semantic search across ClinicalTrials.gov |
| `hcls-cross-cke-pubmed` | RAG-based semantic search across PubMed biomedical literature |
| `hcls-cross-platform-multitenancy` | Multi-tenant data platform architecture for health sciences |
| `hcls-cross-research-problem-selection` | Research problem selection and scientific strategy |
| `hcls-cross-skill-development` | Add new industry skills to the HCLS profile |

### Pharma & Life Sciences (9 skills)
| Skill | Description |
|-------|-------------|
| `hcls-pharma-dsafety-clinical-trial-protocol` | Generate clinical trial protocols for devices/drugs |
| `hcls-pharma-dsafety-pharmacovigilance` | FDA FAERS adverse event analysis and signal detection |
| `hcls-pharma-genomics-nextflow` | nf-core bioinformatics pipelines (rnaseq, sarek, atacseq) |
| `hcls-pharma-genomics-scvi-tools` | Deep learning for single-cell analysis (scVI, totalVI, etc.) |
| `hcls-pharma-genomics-single-cell-qc` | scRNA-seq QC using scverse best practices |
| `hcls-pharma-genomics-survival-analysis` | Kaplan-Meier, Cox regression, time-to-event modeling |
| `hcls-pharma-genomics-variant-annotation` | Genomic variant annotation with ClinVar and gnomAD |
| `hcls-pharma-lab-allotrope` | Convert lab instrument output to Allotrope Simple Model (ASM) |
| `hcls-pharma-lab-ml-optimization` | ML to optimize lab workflows and reduce turnaround time |

### Healthcare Provider (6 skills)
| Skill | Description |
|-------|-------------|
| `hcls-provider-cdata-clinical-docs` | Clinical document intelligence and pipeline orchestration |
| `hcls-provider-cdata-clinical-nlp` | GenAI-powered clinical NLP (NER, ICD coding, medication extraction) |
| `hcls-provider-cdata-fhir` | Transform FHIR bundles into relational tables |
| `hcls-provider-cdata-omop` | Transform clinical data to OMOP CDM v5.4 |
| `hcls-provider-claims-data-analysis` | Claims data analytics for real-world evidence |
| `hcls-provider-imaging` | DICOM medical imaging pipelines on Snowflake |

## Source Repository

The skills source code lives in the official (private) repository:

[Snowflake-Solutions/health-sciences-coco-skills-incubator](https://github.com/Snowflake-Solutions/health-sciences-coco-skills-incubator)

## Usage

Invoke any skill in Cortex Code by name:

```
$hcls-provider-cdata-clinical-nlp
```

Or trigger naturally by describing your task — Cortex Code automatically routes to the appropriate skill.

## Built With

- [Snowflake Cortex Code](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code)
- GitHub Pages
