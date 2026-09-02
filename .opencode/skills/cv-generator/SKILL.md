---
name: cv-generator
description: Use when the user wants to create, generate, update, translate, or co-create their CV/résumé from scratch in this project (PDF + DOCX, Spanish & English). Trigger on requests like "genera mi CV", "crea mi hoja de vida desde cero", "update my CV", "add a project to my resume", or anything about building a CV through a guided interview.
---

# CV Generator & Co-Creation Engine

This project turns structured JSON into a polished CV (PDF + DOCX) in Spanish and English.
Your job is to **co-create** the CV with the user through a guided interview, then generate the files.

## Golden rules
- **Never edit generated `output/` files by hand** — edit the JSON and regenerate.
- Keep `data/cv_es.json` and `data/cv_en.json` in **parity** (same keys, same number of entries). Translate between them; do not leave one empty.
- Respond in the **user's language** (ES or EN).
- The output filenames are derived automatically from `header.name` (e.g. `Laura_Gomez_CV_ES.pdf`).

## Mode detection
1. If `data/cv_es.json` already contains the user's real content → **update mode**: ask what to change, edit, regenerate.
2. If the data is the sample/template (e.g. "Laura Gómez") or missing → **from-scratch mode**: run the interview below.

## From-scratch interview (co-creation)
Move in phases. Ask a few questions at a time; confirm before writing.

**Phase 1 — Identity & directrices (guidelines)**
- Full name, profession/area, target role or objective.
- Desired tone: formal / dynamic / technical / executive.
- What to **emphasize** (e.g. leadership, impact, tools) and what to **omit** (if anything).
- Target audience (recruiters, academia, clients) if relevant.

**Phase 2 — Content, section by section**
- **Experience:** one job at a time — role, company, period, location, scope, and 2–4 bullet_points. Push for **metrics/impact** in bullets.
- **Projects** (optional): name, role, period, description, bullets.
- **Education:** degree, institution, period, location, details.
- **Skills:** grouped by category → items[] (let the user name their own categories).
- **Publications** (optional), **Volunteer** (optional), **Awards** (optional).
- **Certifications** and **Languages** (language + level + optional link).

**Phase 3 — Draft & evaluate**
- Write the JSON to `data/cv_es.json` and `data/cv_en.json`.
- Validate: `python -c "import json; json.load(open('data/cv_es.json', encoding='utf-8')); json.load(open('data/cv_en.json', encoding='utf-8'))"`
- **Evaluate** the draft and report concisely:
  - Clarity & conciseness of the summary and bullets.
  - Presence of **quantified impact** (metrics, %).
  - ES/EN consistency and parity.
  - ATS-friendliness (standard section names, no tables-as-images).
  - Alignment with the user's stated directrices (tone, emphasis, omissions).
  - Length (ideally 1–2 pages).
- Propose 2–3 concrete improvements and let the user accept/reject.

**Phase 4 — Iterate & generate**
- Apply accepted edits, re-validate, then run `python generate_cv.py`.
- Confirm the files appear in `output/`.
- Offer to commit & push: `git add -A && git commit -m "..." && git push origin main`.

## Update mode
- Ask what to change; edit the relevant JSON fields in BOTH languages; re-validate; regenerate; offer commit/push.
- For **batch updates** (Pro): apply the same addition (skill/project/cert) to all selected CVs at once.

## Gestión por vacante (tracking + 1 clic)
Este proyecto incluye `data/vacancies.json` y `data/applications.json` + `manage.py`:
- `python manage.py add-vacancy --empresa X --rol Y --jd "..." --url ...`
- `python manage.py list` / `update-status --app app_001 --estado entrevista`
- `recommend --app app_001` muestra recomendaciones ATS + camino formativo (la IA las genera)
- `apply-one-click --app app_001` marca como aplicado y el siguiente `generate_cv.py` regenera el CV vinculado
- Flujo Pro: pegar vacante → IA adapta CV (keywords ATS, reordena skills) → registra email manual (sin OAuth en v1) → cambia estado → "Aplicar en 1 clic"

## Recomendaciones ATS + camino formativo
- Evalúa **ATS** (keywords faltantes, orden de secciones, densidad) y propone cambios concretos.
- Evalúa **camino formativo** por área/mercado (ej. "te falta dbt/Airflow → curso X"). Preparado para futuros partners de aprendizaje virtual (endpoint `learning_partners`).

## Roles y vigencia
Ver `config/roles.json`. **Admin** gestiona tiers/vigencias/plantillas. **Free** = 1 CV con watermark pronunciada (diagonal + footer, difícil de quitar). **Pago único 12 meses** = 1 CV sin watermark. **Pro** = hasta 10 CVs. Verifica `data/cv_*.json:meta.watermark` y `meta.vigencia_hasta`.

## Integración futura (en la mira)
- Email OAuth (Gmail/Outlook) para auto-track — v1 es log manual (`email_enviado_a`).
- Partners de aprendizaje virtual para camino formativo.

## Conventions
- Editable fields: `meta` (tier/watermark/vigencia_hasta/cv_id), `header`, `summary`, `experience[]`, `projects[]`, `education[]`, `skills`, `publications[]`, `volunteer[]`, `awards[]`, `certifications[]`, `languages[]`.
- Optional sections can be omitted entirely; the generator handles their absence.
- Keep the user's positioning consistent in `title`/`summary` across languages.
