---
name: architecture
description: >
  Use this skill whenever you are tasked with implementing a new domain's analytics architecture
  in this repository. This includes reading a Kimball-style domain markdown file and producing
  the full data stack: synthetic data generators, dlt ingestion, dbt transformations, and
  Power BI semantic model files. Also use this skill to understand the existing insurance
  implementation as a reference for any domain-specific questions.
---

# Architecture Skill — Domain Adaptation Guide

This skill guides an agent through creating a complete, domain-specific implementation of the
analytics stack from scratch, starting from the template state and ending with a working
end-to-end pipeline for any industry domain.

## Skill Map

| File | When to read it |
|---|---|
| [01-as-is-template-architecture.md](01-as-is-template-architecture.md) | First — understand what already exists in the clean repo |
| [02-to-be-target-architecture.md](02-to-be-target-architecture.md) | Second — understand what you need to build for the new domain |
| [03-reading-the-target-markdown.md](03-reading-the-target-markdown.md) | Alongside the domain markdown — how to extract tables, grains, facts, and dimensions |

## Workflow Overview

```
1. Read the domain *_target_markdown.md               ← use skill 03
2. Identify all star schemas and their tables          ← use skill 03
3. Understand the template's pre-built scaffolding    ← use skill 01
4. Build the domain-specific files layer by layer     ← use skill 02
   a. Data generators (src/data_generators/)
   b. Update src_raw.yml (transform/models/src_raw.yml)
   c. Update dbt_project.yml (transform/dbt_project.yml)
   d. dbt staging models (transform/models/staging/)
   e. dbt mart models (transform/models/mart/)
   f. dbt reporting models (transform/models/reporting/)
   g. Update Taskfile.yml (generate-data task)
5. Run full-load to verify end-to-end                 ← task full-load
```

## Guiding Principles

- **One star schema = one subfolder** across `src/data_generators/`, `data/raw/`, `transform/models/staging/`, `transform/models/mart/`, and `transform/models/reporting/`.
- **Never modify** `src/pipeline/`, `src/export_reporting/`, or `src/generate_powerbi/` — these are domain-agnostic and already work.
- **The Taskfile drives everything.** Add new `generate-data` commands; everything else (`ingest`, `transform-prod`, `export-reporting`, `generate-powerbi`) already works generically.
- **Naming is load-bearing.** The export and Power BI scripts discover star schemas by folder name; be consistent.
