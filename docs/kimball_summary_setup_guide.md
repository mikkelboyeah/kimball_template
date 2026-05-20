# Skill: Kimball Chapter Summary Creator

## Purpose

This skill guides you through using an AI tool to generate a structured domain knowledge markdown file from a Kimball *Data Warehouse Toolkit* chapter. The resulting markdown captures key fact tables, lineage relationships, and business context — and becomes the domain reference document that agents and developers in this project use.

The output replaces (or becomes) the content of the `docs/` folder for your specific domain.

---

## When to Use This

Use this skill when you are adapting this template to a **new domain** (e.g. retail, healthcare, banking). You have access to the relevant Kimball chapter covering that domain's dimensional model patterns, and you want to produce a structured summary that can guide an agent building the analytics stack.

For reference, see [`insurance_target_markdown_example.md`](insurance_target_markdown_example.md) — this is an example of the output produced for the insurance domain.

---

## What You Need

1. **The Kimball book** — *The Data Warehouse Toolkit, 3rd Edition* by Ralph Kimball & Margy Ross, or the relevant chapter covering your domain.
2. **An AI tool of your choice** — upload the book (or chapter) to one of:
   - [NotebookLM](https://notebooklm.google.com/)
   - [Claude](https://claude.ai/) (upload PDF directly)
   - [ChatGPT / Codex](https://chatgpt.com/) (upload PDF or paste text)
   - Any other AI assistant that supports document uploads or large context

---

## Instructions

### Step 1 — Upload the book and the skill file

Upload **two files** to your AI tool of choice:

1. The Kimball book (or the relevant domain chapter).
2. **`skill-kimball-summary-setup.md`** — this is the agent skill that tells the AI exactly what to produce and how to structure it. Upload it as a second document or paste it into the system prompt, depending on your tool.

### Step 2 — Send the following prompt

```
You are a data warehouse expert helping me extract structured domain knowledge from a Kimball chapter.

Based on the uploaded chapter covering [YOUR DOMAIN] (e.g. "Chapter 14: Insurance"), produce a structured markdown document with the following sections:

1. **Table-Use Case Overview**
   A table listing each major fact table identified in the chapter. For each table include:
   - Table name
   - Description
   - Representative use cases (2-3 bullet points)
   - Value chain position: Upstream (atomic transactions), Midstream (derived snapshots), or Downstream (consolidated views)

2. **Table Lineage**
   A Mermaid flowchart showing how the fact tables relate to and derive from each other. Use subgraphs for Upstream / Midstream / Downstream. Show directional arrows with a brief label describing the relationship (e.g. "Rolls forward pipeline state", "Calculates monthly revenue").

3. **Dimension Tables**
   For each major dimension table in the chapter, provide:
   - Table name
   - Description
   - Key attributes (as a list)
   - Which fact tables it joins to

4. **Grain Definitions**
   For each fact table, define the grain (one row represents...).

5. **Rolling Forward Pattern**
   If the chapter describes an accumulating snapshot or rolling-forward pattern, explain it in plain language with an example.

6. **Business Questions Answered**
   A bullet list of the key business questions this chapter data model is designed to answer.

Output format: clean markdown, suitable for use as a reference document in a code repository. Use headers, tables, bullet lists, and Mermaid code blocks where appropriate. Do not include any preamble or explanation outside the document itself.
```

### Step 3 — Save the output

Save the AI response as a `.md` file inside `docs/`. For example:
- `docs/retail_target_markdown.md`
- `docs/healthcare_target_markdown.md`

This file becomes the domain knowledge source for agents working in this project. You can replace or supplement the existing `docs/insurance_target_markdown_example.md` with your new file.

### Step 4 — Reference it in agent instructions

If you have a `.agent/` folder, update `.agent/README.md` or the relevant instruction file to point to your new domain markdown as the reference document for data modelling decisions.

---

## Tips

- If the AI tool truncates or misses sections, ask follow-up questions like: *"Now add the dimension tables section"* or *"Complete the Mermaid diagram"*.
- If the output uses inconsistent naming, ask the AI to normalise table names to `snake_case`.
- The more specific your domain label in Step 2 (e.g. "Chapter 14: Insurance" vs just "insurance"), the better the AI will anchor its response to the right chapter content.
