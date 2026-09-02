import os
import json
from jinja2 import Template
from weasyprint import HTML
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# ---------------------------------------------------------------------------
# Etiquetas por idioma (ampliables: añade claves aquí y en el JSON)
# ---------------------------------------------------------------------------
LABELS = {
    "es": {
        "summary": "PERFIL PROFESIONAL",
        "experience": "EXPERIENCIA LABORAL",
        "projects": "PROYECTOS",
        "education": "EDUCACIÓN",
        "skills": "HABILIDADES TÉCNICAS",
        "publications": "PUBLICACIONES",
        "volunteer": "VOLUNTARIADO",
        "awards": "PREMIOS Y RECONOCIMIENTOS",
        "certifications": "CERTIFICACIONES",
        "languages": "IDIOMAS",
    },
    "en": {
        "summary": "PROFESSIONAL SUMMARY",
        "experience": "WORK EXPERIENCE",
        "projects": "PROJECTS",
        "education": "EDUCATION",
        "skills": "TECHNICAL SKILLS",
        "publications": "PUBLICATIONS",
        "volunteer": "VOLUNTEER",
        "awards": "AWARDS & RECOGNITIONS",
        "certifications": "CERTIFICATIONS",
        "languages": "LANGUAGES",
    },
}


def output_names(data):
    """Deriva los nombres de archivo a partir del nombre del usuario."""
    name = data["header"]["name"].strip().replace(" ", "_")
    return {
        "es": {"pdf": f"{name}_CV_ES.pdf", "docx": f"{name}_CV_ES.docx"},
        "en": {"pdf": f"{name}_CV_EN.pdf", "docx": f"{name}_CV_EN.docx"},
    }


# ---------------------------------------------------------------------------
# 1. Generador de PDF
# ---------------------------------------------------------------------------
def generate_pdf(data, labels, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    template_path = os.path.join(BASE_DIR, "templates", "template.html")
    with open(template_path, "r", encoding="utf-8") as f:
        template = Template(f.read())
    rendered_html = template.render(data=data, labels=labels)
    HTML(string=rendered_html).write_pdf(filename)


# ---------------------------------------------------------------------------
# 2. Generador de DOCX (estilo consistente con el PDF)
# ---------------------------------------------------------------------------
def generate_docx(data, labels, filename):
    doc = docx.Document()
    for section in doc.sections:
        section.top_margin = Inches(0.7)
        section.bottom_margin = Inches(0.7)
        section.left_margin = Inches(0.65)
        section.right_margin = Inches(0.65)

    # Tema todo negro (base estándar ATS: negro puro, tipografía Helvetica/Arial)
    BLACK = RGBColor(0x00, 0x00, 0x00)
    NAVY = BLACK
    GREEN = BLACK
    DARK_GRAY = RGBColor(0x11, 0x11, 0x11)
    LIGHT_GRAY = RGBColor(0x44, 0x44, 0x44)
    WATERMARK_RED = RGBColor(0xCC, 0x1F, 0x1F)

    # Watermark pronunciado para planes gratuitos (difícil de quitar)
    is_watermark = bool(data.get("meta", {}).get("watermark", False))
    if is_watermark:
        # Header repetido en cada página con marca diagonal simulada
        for section in doc.sections:
            header = section.header
            header.is_linked_to_previous = False
            p_wm = header.paragraphs[0] if header.paragraphs else header.add_paragraph()
            p_wm.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r_wm = p_wm.add_run(f"BORRADOR — {data['header']['email']} — NO VÁLIDO PARA ENVÍO")
            r_wm.font.name = "Arial"
            r_wm.font.size = Pt(9)
            r_wm.font.bold = True
            r_wm.font.color.rgb = WATERMARK_RED
            # Footer adicional con aviso
            footer = section.footer
            footer.is_linked_to_previous = False
            p_ft = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
            p_ft.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r_ft = p_ft.add_run(f"BORRADOR — {data['header']['name']} — Actualiza a pago único/Pro para quitar esta marca")
            r_ft.font.name = "Arial"
            r_ft.font.size = Pt(7)
            r_ft.font.color.rgb = WATERMARK_RED

    def add_bottom_border(paragraph):
        pPr = paragraph._element.get_or_add_pPr()
        pBdr = parse_xml(
            r'<w:pBdr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
            r'<w:bottom w:val="single" w:sz="6" w:space="4" w:color="DCDDE1"/>'
            r"</w:pBdr>"
        )
        pPr.append(pBdr)

    # Nombre
    p_name = doc.add_paragraph()
    r_name = p_name.add_run(data["header"]["name"])
    r_name.font.name = "Arial"
    r_name.font.size = Pt(20)
    r_name.font.bold = True
    r_name.font.color.rgb = NAVY

    # Título
    p_title = doc.add_paragraph()
    r_title = p_title.add_run(data["header"]["title"])
    r_title.font.name = "Arial"
    r_title.font.size = Pt(10.5)
    r_title.font.bold = True
    r_title.font.color.rgb = GREEN

    # Tagline
    if data["header"].get("tagline"):
        p_tag = doc.add_paragraph()
        p_tag.paragraph_format.space_after = Pt(4)
        r_tag = p_tag.add_run(data["header"]["tagline"])
        r_tag.font.name = "Arial"
        r_tag.font.size = Pt(8.5)
        r_tag.font.italic = True
        r_tag.font.color.rgb = LIGHT_GRAY

    # Contacto
    p_contact = doc.add_paragraph()
    contact_str = (
        f"{data['header']['email']}  |  {data['header']['phone']}  |  {data['header']['location']}\n"
        f"https://{data['header']['linkedin']}"
    )
    if data["header"].get("portfolio"):
        contact_str += f"  |  https://{data['header']['portfolio']}"
    r_contact = p_contact.add_run(contact_str)
    r_contact.font.name = "Arial"
    r_contact.font.size = Pt(8.5)
    r_contact.font.color.rgb = LIGHT_GRAY
    add_bottom_border(p_contact)

    def add_section_header(title_text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(6)
        r = p.add_run(title_text)
        r.font.name = "Arial"
        r.font.size = Pt(11)
        r.font.bold = True
        r.font.color.rgb = NAVY
        add_bottom_border(p)

    def add_job_row(role, secondary, period, location, period_loc_size=8.5):
        table = doc.add_table(rows=1, cols=2)
        cell_l, cell_r = table.rows[0].cells
        cell_l.width, cell_r.width = Inches(5.2), Inches(2.0)
        p_l = cell_l.paragraphs[0]
        r_role = p_l.add_run(role)
        r_role.bold, r_role.font.name, r_role.font.size = True, "Arial", Pt(10)
        r_comp = p_l.add_run(f" | {secondary}")
        r_comp.font.name, r_comp.font.size, r_comp.font.color.rgb = "Arial", Pt(10), LIGHT_GRAY
        p_r = cell_r.paragraphs[0]
        p_r.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r_date = p_r.add_run(f"{period} | {location}")
        r_date.font.name, r_date.font.size, r_date.font.bold = "Arial", period_loc_size, True
        return table

    def add_bullets(items):
        for bullet in items or []:
            bp = doc.add_paragraph(style="List Bullet")
            bp.paragraph_format.space_after = Pt(2)
            r_bp = bp.add_run(bullet)
            r_bp.font.name, r_bp.font.size = "Arial", Pt(9.5)

    # Perfil
    add_section_header(labels["summary"])
    p_sum = doc.add_paragraph()
    r_sum = p_sum.add_run(data["summary"])
    r_sum.font.name = "Arial"
    r_sum.font.size = Pt(9.5)
    r_sum.font.color.rgb = DARK_GRAY

    # Experiencia
    add_section_header(labels["experience"])
    for job in data["experience"]:
        add_job_row(job["role"], job["company"], job.get("period", ""), job.get("location", ""))
        if job.get("scope"):
            p_scope = doc.add_paragraph()
            p_scope.paragraph_format.space_after = Pt(2)
            r_scope = p_scope.add_run(job["scope"])
            r_scope.font.name = "Arial"
            r_scope.font.size = Pt(8)
            r_scope.font.italic = True
            r_scope.font.color.rgb = LIGHT_GRAY
        add_bullets(job.get("bullet_points"))

    # Proyectos (opcional)
    if data.get("projects"):
        add_section_header(labels["projects"])
        for p in data["projects"]:
            add_job_row(p.get("name", ""), p.get("role", ""), p.get("period", ""), p.get("location", ""))
            if p.get("description"):
                p_desc = doc.add_paragraph()
                p_desc.paragraph_format.space_after = Pt(2)
                r_desc = p_desc.add_run(p["description"])
                r_desc.font.name = "Arial"
                r_desc.font.size = Pt(8)
                r_desc.font.italic = True
                r_desc.font.color.rgb = LIGHT_GRAY
            add_bullets(p.get("bullet_points"))

    # Educación
    add_section_header(labels["education"])
    for edu in data["education"]:
        add_job_row(edu["degree"], edu["institution"], edu.get("period", ""), edu.get("location", ""))
        if edu.get("details"):
            p_det = doc.add_paragraph()
            p_det.paragraph_format.space_after = Pt(4)
            r_det = p_det.add_run(edu["details"])
            r_det.font.name = "Arial"
            r_det.font.size = Pt(9)
            r_det.font.color.rgb = LIGHT_GRAY

    # Habilidades
    add_section_header(labels["skills"])
    for category, items in data["skills"].items():
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(2)
        r_cat = p.add_run(f"{category}: ")
        r_cat.bold, r_cat.font.name, r_cat.font.size = True, "Arial", Pt(9.5)
        r_items = p.add_run(", ".join(items))
        r_items.font.name, r_items.font.size, r_items.font.color.rgb = "Arial", Pt(9.5), DARK_GRAY

    # Publicaciones (opcional)
    if data.get("publications"):
        add_section_header(labels["publications"])
        for pub in data["publications"]:
            p = doc.add_paragraph(style="List Bullet")
            p.paragraph_format.space_after = Pt(2)
            text = ""
            if pub.get("authors"):
                text += pub["authors"] + ". "
            r_t = p.add_run(text + pub.get("title", ""))
            r_t.italic = True
            r_t.font.name, r_t.font.size = "Arial", Pt(9.5)
            extra = ""
            if pub.get("venue"):
                extra += ". " + pub["venue"]
            if pub.get("year"):
                extra += f" ({pub['year']})"
            if extra:
                r_e = p.add_run(extra)
                r_e.font.name, r_e.font.size = "Arial", Pt(9.5)

            if pub.get("link"):
                r_l = p.add_run(f"  |  https://{pub['link']}")
                r_l.font.name, r_l.font.size, r_l.font.color.rgb = "Arial", Pt(8.5), NAVY

    # Voluntariado (opcional)
    if data.get("volunteer"):
        add_section_header(labels["volunteer"])
        for v in data["volunteer"]:
            add_job_row(v.get("role", ""), v.get("organization", ""), v.get("period", ""), v.get("location", ""))
            add_bullets(v.get("bullet_points"))

    # Premios (opcional)
    if data.get("awards"):
        add_section_header(labels["awards"])
        for a in data["awards"]:
            p = doc.add_paragraph(style="List Bullet")
            p.paragraph_format.space_after = Pt(2)
            r_a = p.add_run(a.get("name", ""))
            r_a.bold, r_a.font.name, r_a.font.size = True, "Arial", Pt(9.5)
            extra = ""
            if a.get("issuer"):
                extra += f" — {a['issuer']}"
            if a.get("year"):
                extra += f" ({a['year']})"
            if a.get("description"):
                extra += f" — {a['description']}"
            if extra:
                r_e = p.add_run(extra)
                r_e.font.name, r_e.font.size = "Arial", Pt(9.5)

    # Certificaciones
    add_section_header(labels["certifications"])
    for cert in data["certifications"]:
        p = doc.add_paragraph(style="List Bullet")
        p.paragraph_format.space_after = Pt(2)
        r_cert = p.add_run(cert)
        r_cert.font.name, r_cert.font.size = "Arial", Pt(9.5)

    if data.get("certificates_url"):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(2)
        r_link = p.add_run(f"https://{data['certificates_url']}")
        r_link.font.name, r_link.font.size = "Arial", Pt(8.5)
        r_link.font.color.rgb = NAVY

    # Idiomas
    add_section_header(labels["languages"])
    for lang in data["languages"]:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(2)
        r_lang = p.add_run(lang["language"])
        r_lang.bold, r_lang.font.name, r_lang.font.size = True, "Arial", Pt(9.5)
        r_lvl = p.add_run(f" — {lang['level']}")
        r_lvl.font.name, r_lvl.font.size, r_lvl.font.color.rgb = "Arial", Pt(9.5), DARK_GRAY
        if lang.get("link"):
            r_link = p.add_run(f"  |  https://{lang['link']}")
            r_link.font.name, r_link.font.size, r_link.font.color.rgb = "Arial", Pt(8.5), NAVY

    os.makedirs(os.path.dirname(filename), exist_ok=True)
    doc.save(filename)


# ---------------------------------------------------------------------------
# 3. Función principal
# ---------------------------------------------------------------------------
def main():
    for lang in ["es", "en"]:
        data_path = os.path.join(BASE_DIR, "data", f"cv_{lang}.json")
        if os.path.exists(data_path):
            with open(data_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            labels = LABELS[lang]
            out = output_names(data)
            generate_pdf(data, labels, os.path.join(BASE_DIR, "output", out[lang]["pdf"]))
            generate_docx(data, labels, os.path.join(BASE_DIR, "output", out[lang]["docx"]))
            print(f"[OK] Generado correctamente: {out[lang]['pdf']} y {out[lang]['docx']}")
        else:
            print(f"[WARN] No se encontró {data_path}")


if __name__ == "__main__":
    main()
