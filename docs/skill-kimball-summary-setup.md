## name: kimball-chapter-to-markdown
description:

**Convert a chapter from Ralph Kimball & Margy Ross, *The Data Warehouse Toolkit, 3rd Edition*** into a structured markdown knowledge document that mirrors the reference document `docs/insurance_target_markdown_example.md`.

**Triggers** whenever the user asks the agent to create, draft, plan, or build a domain summary from any Kimball chapter — e.g.

- "make a markdown summary from chapter 7"
- "build the accounting one like the insurance doc"
- "do chapter 14 next"

Use this skill for the full workflow (plan → confirm → author → save as markdown).

Do NOT use this for general data warehousing Q&A — that is plain project chat.

# Kimball Chapter → Markdown Document

This skill produces a markdown file that documents the **fact tables and data models** described in a single Kimball chapter, in the exact shape of the reference document `docs/insurance_target_markdown_example.md` (chapter 16, Insurance).

Open and read that reference file before starting any new chapter, so you can match its conventions exactly.

---

## 1. Sources and grounding

Two sources only, per project instructions:

1. The Kimball book — *The Data Warehouse Toolkit, 3rd Edition* — uploaded by the user to this session.
2. The reference file `docs/insurance_target_markdown_example.md` (for **format**, not for facts about other chapters).

**Do not invent facts** about a chapter that are not in the book. If a chapter is light on something the reference calls for (e.g. a chapter has no factless fact table), leave that section out rather than fabricate one.

---

## 2. Workflow (4 phases)

### Phase 1 — Inventory the chapter

Read or search the chapter and produce an internal inventory of every fact table / dimensional model it describes. For each one, note:

- The table's name as Kimball writes it (e.g. "Policy Transaction Fact Table", "General Ledger Periodic Snapshot").
- Its **grain** (one row per …).
- Its **fact-table type** (transaction / periodic snapshot / accumulating snapshot / factless / consolidated / supertype-subtype).
- The **business process** it serves (this drives the H2 grouping later).
- Whether it is **derived from** another fact table in the same chapter (transaction → accumulating snapshot, two atomic tables → consolidated, etc.). This is what powers the lineage diagram.
- Page references in the book (e.g. "p. 383, Fig 16-2"). Include these in your plan so the user can verify.

A chapter typically yields 3–8 tables. If you find more than 10 something is probably double-counted. If you find fewer than 2, double-check — most case-study chapters have at least one transaction table and one snapshot.

### Phase 2 — Lay out a plan, then wait for confirmation

Before authoring anything, write a plain-text plan to the user containing:

1. The list of fact tables you found, grouped by H2 section (subject area — e.g. "Policy-Related", "Premium-Related", "Claim-Related"). The grouping should follow the chapter's own subject-area structure, not be invented.
2. The proposed lineage edges (e.g. "Policy Transaction → Policy Accumulating Snapshot", "Premium Periodic Snapshot + Claim Periodic Snapshot → Policy/Claim Consolidated").
3. The proposed summary-table rows (one per fact table).
4. Any optional appendix patterns from the chapter you would include (e.g. timespan accumulating snapshot, supertype/subtype, mini-dimensions). Only include patterns the chapter explicitly discusses.
5. Anything you are unsure about or where you went beyond the book (e.g. inferring a lineage edge Kimball does not draw explicitly — flag it).

Then **stop and ask the user to approve or adjust** before continuing. Iterate as needed. The plan is cheap; the document is expensive.

### Phase 3 — Author the content

Build the full document as a single markdown string, following the template in §3 below. Do this in your scratch space so the user can review one more time if they want.

### Phase 4 — Save the markdown file

Write the completed markdown to a file in the `docs/` folder, e.g. `docs/accounting_target_markdown.md`. Return the file path to the user and confirm it is saved.

---

## 3. Document template

Match the structure of `docs/insurance_target_markdown_example.md` exactly. Sections in order:

```
# Table-Use case overview
<one short paragraph: what this document covers, sorted by data value chain>

<table: "Kimball <topic> table use-case mapping" — columns: Table | Description | Use Cases | Value Chain Position>

# Table lineage
<mermaid flowchart LR, with Upstream / Midstream / Downstream subgraphs>
<short prose explaining any non-obvious terms used in the diagram>

# Table details
## <Subject-area group 1>
### <Fact Table Name>
<one-line description>
- **Grain:** <one row per …>
- **Key Facts:** <comma-separated list of the main numeric measures>
<details>
<summary>ER diagram</summary>
```

erDiagram

…

```
</details>
- **How it works:** <one paragraph: when rows are inserted/updated, ETL cadence, special handling>
- **Structure:** <one paragraph: dimensions used, role-playing, degenerate dimensions, junk dimensions, supertype/subtype splits, conformed dimensions reused>
- **Best Use Case:** <one paragraph: the analytical questions this table answers well>

### <next fact table … same shape>

## <Subject-area group 2>
…

---

# <Optional appendix sections for chapter-specific patterns>
<e.g. "Timespan Accumulating Snapshot", "Supertype/Subtype Products", "Mini-Dimensions">
```

### Notes on Key Facts vs Facts

Use only **`Key Facts`** as a bulleted list near the top of each table block. Fold any narrative about what the facts mean into the **How it works** or **Structure** paragraph. Do not add a separate **Facts** section.

### Section group headings

Use `## Group name` for subject-area groupings. The groups should come from the chapter itself, e.g.:

- Chapter 7 (Accounting): "General Ledger", "Budgeting Chain", "Consolidated"
- Chapter 9 (HR): "Employee Profile", "Headcount Snapshot", "HR Process Pipelines"
- Chapter 14 (Healthcare): "Billing & Payments", "EMR & Diagnostics", "Operational"
- Chapter 16 (Insurance): "Policy-Related", "Premium-Related", "Claim-Related", "Consolidated and Factless"

If a chapter has only one subject area, you can drop the H2 grouping and use H3 directly.

---

## 4. Conventions for the Mermaid diagrams

### 4a. Lineage flowchart

Use this skeleton, adjust the nodes for the chapter:

```mermaid
flowchart LR
    subgraph Upstream ["1. Upstream (Atomic Transactions)"]
        direction TB
        <node> ["<Fact Table Name><br/>Fact Table"]
    end

    subgraph Midstream ["2. Midstream (Derived Snapshots)"]
        direction TB
        <node> ["<Fact Table Name><br/>Snapshot"]
    end

    subgraph Downstream ["3. Downstream (Consolidated Views)"]
        direction TB
        <node> ["<Fact Table Name><br/>Consolidated"]
    end

    <node> -->|<edge label>| <node>
```

Conventions:

- **Upstream** = atomic transaction-grain fact tables and factless event tables (the closest layer to source data).
- **Midstream** = derived snapshots — accumulating and periodic snapshots that are *rolled forward* from transactions.
- **Downstream** = consolidated / drill-across fact tables that combine multiple business processes.
- Solid arrows (`-->`) for direct ETL derivations (e.g. "rolls forward pipeline state").
- Dashed arrows (`-.->`) for looser conceptual links (e.g. "provides event context to" between a factless table and an accumulating snapshot).
- Always label the edges with a verb phrase, not just a line.

**Honesty caveat.** Kimball does not draw an explicit data-flow lineage between fact tables across the chapter; this diagram is a synthesis. Edges that derive from text the book explicitly states are safe. Edges you are inferring should be called out in the plan in Phase 2 and described in plain prose under the diagram so the reader sees they are synthesis, not direct quotes.

### 4b. ER diagrams

Use Mermaid `erDiagram`. Each ER diagram lives inside a `<details><summary>ER diagram</summary>…</details>` toggle so the document stays scannable.

Naming conventions:

- `_FK` suffix on foreign-key columns on the fact table.
- `_PK` suffix on the primary key of dimension tables.
- `_DD` suffix on degenerate dimensions (policy number, transaction number, claim number, etc.).
- Relationship lines: `Dimension ||--o{ Fact_Table : "<role>"`.
- For role-playing date dimensions (multiple foreign keys pointing to one date dimension), draw one relationship per role with the role name as the label, e.g.:

```
Date_Dimension ||--o{ Policy_Transaction_Fact : "transaction_date"
Date_Dimension ||--o{ Policy_Transaction_Fact : "effective_date"
```

You only need to fully define each dimension table once per ER diagram — referencing it by name is enough for the others.

---

## 5. Per-fact-table content checklist

Before moving on from a fact table, every block must contain, in this order:

1. **H3 heading** with the fact table's name as written in the book.
2. **One-line description** (no bold, no bullet) describing what the table captures.
3. **`**Grain:**`** — one row per …
4. **`**Key Facts:**`** — comma-separated list of the main additive numeric measures. Include semi-additive flags where relevant (e.g. "Current Reserve to Date Dollar Amount (semi-additive)").
5. **ER diagram in a toggle.**
6. **`**How it works:**`** — when rows are inserted, when/if they are updated, ETL cadence, what makes this table behave like a transaction / snapshot / accumulating snapshot.
7. **`**Structure:**`** — dimensions, role-playing, degenerate dimensions, junk/profile dimensions, supertype/subtype if applicable, conformed dimensions reused from siblings.
8. **`**Best Use Case:**`** — what business questions this table answers well, and any contrast with sibling tables.

Skip blocks that do not fit (e.g. if a table has no role-playing dimensions, do not mention them in Structure). But do not skip any of the eight items above.

---

## 6. Optional appendix sections

If the chapter discusses a notable pattern that does not belong to any one fact table, add an H1 section at the bottom after `---`. Examples drawn from chapter 16: *Timespan Accumulating Snapshot*, *Supertype/Subtype for Heterogeneous Products*, *Multivalued Dimensions via Bridge Tables*.

For chapter 7 (Accounting) this would include *Ragged Variable-Depth Hierarchies with Bridge Tables*, *Pathstring Hierarchies*, *Year-to-Date Facts*, *Multiple Fiscal Calendars*, etc.

Each appendix entry: an H2 or H1 heading, one short paragraph of context, and a pointer back to where Kimball uses it within this chapter.

---

## 7. Style notes

- **Voice:** explanatory, concrete, business-flavored — matching the reference document. Not academic. Not bullet-heavy beyond the canonical bullets per fact table.
- **Length per fact table:** roughly 200–400 words including the ER diagram. Do not pad.
- **Citations:** weave page references into prose lightly ("p. 383", "Fig. 16-9"). Do not produce a separate bibliography.
- **Bolding:** bold the key concept names the first time they appear within a block (e.g. **role-playing date dimensions**, **degenerate dimension**, **conformed dimensions**). The reference document does this consistently.
- **Out-of-book content:** if the user asks for advice beyond what the book covers, state clearly that this is not from Kimball before answering.

---

## 8. Quick reference: chapter 16 (Insurance) as the worked example

The reference document covers these fact tables (use this as a sanity check for how a chapter should decompose):

| Group | Fact table | Type | Grain |
| --- | --- | --- | --- |
| Policy-Related | Policy Transaction Fact | Transaction | 1 row / policy transaction |
| Policy-Related | Policy Accumulating Snapshot | Accumulating snapshot | 1 row / coverage × covered item on a policy |
| Premium-Related | Premium Periodic Snapshot | Periodic snapshot | 1 row / coverage × covered item × month |
| Claim-Related | Claim Transaction Fact | Transaction | 1 row / claim task transaction |
| Claim-Related | Claim Accumulating Snapshot | Accumulating snapshot | 1 row / claim |
| Claim-Related | Claim Periodic Snapshot | Periodic snapshot | 1 row / active claim × month |
| Consolidated & Factless | Policy/Claim Consolidated Periodic Snapshot | Consolidated periodic snapshot | 1 row / policy × coverage × covered item × agent × month |
| Consolidated & Factless | Factless Accident Events | Factless | 1 row / involved party × role × accident |

Lineage edges in the reference document:

- Policy Transaction → Policy Accumulating Snapshot (rolls forward pipeline state)
- Policy Transaction → Premium Periodic Snapshot (calculates monthly revenue)
- Claim Transaction → Claim Accumulating Snapshot (rolls forward claim state)
- Claim Transaction → Claim Periodic Snapshot (calculates monthly claim financials)
- Premium Periodic Snapshot → Policy/Claim Consolidated (provides premium revenues)
- Claim Periodic Snapshot → Policy/Claim Consolidated (provides claim losses)
- Factless Accident Events ⇢ Claim Accumulating Snapshot (provides event context, dashed)

Appendix in the reference document: *Timespan Accumulating Snapshot* (applied to the Claim Accumulating Snapshot).

Use this decomposition as the model when sizing up other chapters.

---

## 9. What success looks like

A finished document should let a reader who has never opened Kimball:

1. See at a glance (from the use-case table) which tables are close to the source and which are close to the consumer, with concrete example use cases.
2. Trace data flow between tables (from the lineage diagram).
3. For any single table, understand grain, key facts, structure, and the analytical questions it serves — without needing to flip to the book.
4. Match the visual rhythm and conventions of the chapter-16 reference document closely enough that the two could sit side by side without looking out of place.

If your output does not pass those four tests, iterate before saving.
