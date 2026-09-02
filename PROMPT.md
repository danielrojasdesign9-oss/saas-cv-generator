# PROMPT.md — Prompt copiable para crear este proyecto

Este archivo contiene un **prompt ya hecho** que cualquier persona puede copiar y pegar
en su OpenCode (en una carpeta vacía) para generar un proyecto idéntico a esta plantilla,
funcional y listo para usar.

Copia únicamente el bloque de abajo 👇

---

```text
Crea un proyecto generador de CV (Hoja de Vida) listo para usar, en una carpeta llamada "cv-template". Requisitos:

1. Arquitectura data-driven: todo el contenido vive en data/cv_es.json y data/cv_en.json (con meta: tier/watermark/vigencia_hasta). El script generate_cv.py genera PDF y DOCX en español e inglés y añade watermark pronunciada (diagonal + footer) si meta.watermark=true.
2. El nombre de archivo de salida se deriva automaticamente de header.name (ej. "Laura_Gomez_CV_ES.pdf" y ".docx").
3. Usa WeasyPrint (HTML/CSS) para el PDF y python-docx para el DOCX; Jinja2 para la plantilla. Estilos: cabecera azul marino (#1e3d59), acentos verde (#17b978), formato A4, fuente Arial, secciones con borde inferior. Watermark CSS fixed diagonal difícil de quitar.
4. Secciones soportadas (el generador debe ignorar las que falten): header, summary, experience, projects (opcional), education, skills (por categorias), publications (opcional), volunteer (opcional), awards (opcional), certifications, languages, meta.
5. Incluye datos de ejemplo de OTRA area (no diseno), por ejemplo una "Ingeniera de Datos" con experiencia, proyectos y publicaciones, tanto en ES como en EN, para que el usuario vea la estructura real.
6. Crea config/roles.json con roles admin, user_free (1 CV watermark), user_single 12 meses (1 CV sin watermark), user_pro (hasta 10 CVs) y manage.py con data/vacancies.json y data/applications.json para tracking por vacante (add-vacancy, list, update-status, recommend, apply-one-click). En v1 log manual de email; OAuth en la mira.
7. Crea .opencode/skills/cv-generator/SKILL.md: una skill que, al pedirle "genera mi CV" o "crea mi hoja de vida desde cero", entreviste al usuario por fases (identidad, tono y directrices, luego secciones), organice la informacion en el JSON, la evalue (claridad, impacto con metricas, paridad ES/EN, ATS + camino formativo, alineacion con las directrices) y genere los archivos; maneje batch updates y gestión por vacante; mantenga ambos idiomas en paralelo y ofrezca hacer commit/push.
8. requirements.txt con: weasyprint, python-docx, jinja2.
9. README.md bilingue (ES/EN) con los pasos: clonar, "pip install -r requirements.txt", abrir en OpenCode y escribir "Genera mi CV desde cero"; explicar roles, watermark, gestión por vacante y pagos QR Bre-B 0% / Wompi link.
10. PROMPT.md que contenga este mismo prompt para que cualquiera pueda recrear el proyecto.

Al final, ejecuta "python generate_cv.py" y "python manage.py list" para verificar que genera los PDF/DOCX y el tracking sin errores.
```

---

Una vez pegado, OpenCode creará la carpeta `cv-template/` completa y verificará la generación.
