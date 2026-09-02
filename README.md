# Generador de CV / CV Generator

Plantilla lista para usar que convierte un JSON en un **CV profesional en PDF y Word (.docx), en español e inglés**, editable por chat y fácil de actualizar. La IA (OpenCode) te entrevista, organiza tu información, la evalúa y genera los archivos.

A template that turns a JSON into a **professional CV in PDF and Word (.docx), in Spanish & English**, editable by chat and easy to update. The AI (OpenCode) interviews you, organizes your info, evaluates it, and generates the files.

---

## Cómo usar / How to use

### 1. Clonar e instalar (1 comando)
```bash
git clone <este-repo>/cv-template.git
cd cv-template
pip install -r requirements.txt
```
> En Windows, WeasyPrint necesita las librerías del sistema (Pango/GDK). Ver notas abajo.

### 2. Abrir en OpenCode y pedir tu CV
Abre la carpeta en OpenCode y escribe, por ejemplo:
- **ES:** `"Genera mi CV desde cero"`
- **EN:** `"Create my CV from scratch"`

La IA te hará preguntas (identidad, tono, experiencia, etc.), organizará tus datos, los evaluará y generará:
```
output/<Nombre>_CV_ES.pdf / .docx
output/<Nombre>_CV_EN.pdf / .docx
```

### 3. Editar rápido
Pídelo por chat: *"agrega este proyecto a mi experiencia"*, *"cambia el título a X"*, *"actualiza y regenera"*. La IA edita el JSON y regenera.

---

## Estructura / Structure
```
cv-template/
├── data/            # cv_es.json + cv_en.json, vacancies.json, applications.json
├── templates/       # plantilla visual (PDF) con watermark pronunciado
├── output/          # CVs generados (PDF/DOCX)
├── config/roles.json # roles (admin, free, single 12m, pro 10 CVs) y vigencia
├── generate_cv.py   # motor de generación (parametrizado, watermark condicional)
├── manage.py        # helper gestión por vacante (add-vacancy, list, update-status, recommend, apply-one-click)
├── requirements.txt
├── .opencode/skills/cv-generator/  # "prompt" de co-creación + gestión
├── PROMPT.md        # prompt copiable para crear este proyecto desde cero
└── README.md
```

## Roles y pagos / Roles & billing
- **Admin:** gestiona tiers/vigencias/plantillas. No edita CVs ajenos.
- **Free:** 1 CV con marca de agua pronunciada (diagonal + footer, difícil de quitar), 3 exports/mes.
- **Pago único 12 meses (QR Bre-B 0% / Wompi link, solo cobra al usar):** 1 CV único sin watermark, edición simple (colores/tipos/espaciados/contenido).
- **Pro (suscripción Wompi):** hasta 10 CVs, gestión por vacante, lote y asesoría continua.

## Gestión por vacante / Vacancy tracking
```bash
python manage.py add-vacancy --empresa "TechCorp" --rol "Data Engineer" --jd "..." --url "..."
python manage.py list
python manage.py update-status --app app_001 --estado entrevista
python manage.py recommend --app app_001   # ATS + camino formativo
python manage.py apply-one-click --app app_001
```
Emails se registran manual (`email_enviado_a`) en v1; OAuth Gmail/Outlook queda en la mira.

## Secciones soportadas / Supported sections
`header`, `summary`, `experience`, `projects*`, `education`, `skills`, `publications*`, `volunteer*`, `awards*`, `certifications`, `languages`, `meta` (tier/watermark/vigencia_hasta).
(*) Opcionales: si no están en el JSON, no aparecen.

## Notas / Notes
- Los nombres de archivo se derivan de `header.name` automáticamente.
- Mantén `cv_es.json` y `cv_en.json` con la misma estructura y `meta.watermark` coherente con tu tier.
- WeasyPrint (PDF) en Windows requiere Pango/GDK-PixBuf instalados (p.ej. vía MSYS2). En macOS: `brew install pango gdk-pixbuf`.

## Prompt de arranque / Bootstrap prompt
Ver `PROMPT.md` para un texto que puedes copiar y pegar en OpenCode y recrear este proyecto completo desde cero.
