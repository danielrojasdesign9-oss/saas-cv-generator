import os, json, sys
from datetime import date
from jinja2 import Template
from weasyprint import HTML

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data", "letters")
LETTER_TMPL = os.path.join(BASE_DIR, "templates", "letter_template.html")

MONTHS_ES = {1:"enero",2:"febrero",3:"marzo",4:"abril",5:"mayo",6:"junio",7:"julio",8:"agosto",9:"septiembre",10:"octubre",11:"noviembre",12:"diciembre"}

def format_date(lang):
    t=date.today()
    return f"{t.day} de {MONTHS_ES[t.month]} de {t.year}" if lang=="es" else f"{t.strftime('%B')} {t.day}, {t.year}"

def generate_for_vacancy(vacancy_id, lang="es"):
    # Carga CV y vacante
    cv=json.load(open(os.path.join(BASE_DIR, f"data/cv_{lang}.json"), encoding="utf-8"))
    vacs=json.load(open(os.path.join(BASE_DIR, "data/vacancies.json"), encoding="utf-8-sig"))
    vac=next((v for v in vacs if v["id"]==vacancy_id), None)
    if not vac:
        print(f"[WARN] Vacante {vacancy_id} no encontrada"); return
    header=cv["header"]
    # Plantilla de carta personalizada por vacante (generada al vuelo)
    # En Pro, la IA generaría párrafos a partir de cv + jd_text; aquí usamos una base + JD
    paragraphs=[
        f"Me postulo a la posición de {vac['rol']} en {vac['empresa']}. Me llamó la atención la oportunidad y el enfoque descrito en la vacante.",
        f"Soy {header['title']} con experiencia en {', '.join(list(cv['skills'].values())[0][:3])}. Mi perfil combina {cv['summary'][:180]}...",
        f"La vacante menciona: \"{vac['jd_text'][:220]}\". Mi experiencia en {header['title']} me permite aportar valor directo en esos puntos, con enfoque en resultados medibles y colaboración con equipos de producto e ingeniería.",
        "Me entusiasma la posibilidad de conversar y explorar cómo mi experiencia puede aportar al equipo."
    ]
    letter={
        "lang": lang,
        "company": vac["empresa"],
        "file_tag": vac["id"],
        "subject": f"Carta de Presentación — {vac['rol']} — {vac['empresa']}",
        "recipient": f"Estimado equipo de {vac['empresa']},",
        "paragraphs": paragraphs,
        "closing": "Cordialmente,"
    }
    tmpl=Template(open(LETTER_TMPL, encoding="utf-8").read())
    rendered=tmpl.render(name=header["name"], title=header["title"], email=header["email"], phone=header["phone"], location=header["location"], linkedin=header["linkedin"], portfolio=header.get("portfolio",""), date=format_date(lang), subject=letter["subject"], recipient=letter["recipient"], paragraphs=letter["paragraphs"], closing=letter["closing"])
    out_dir=os.path.join(BASE_DIR, "letters", vac["id"])
    os.makedirs(out_dir, exist_ok=True)
    person="_".join(header["name"].split())
    suffix="" if lang=="es" else "_EN"
    out_name=f"Carta_Presentacion_{vac['id']}_{person}{suffix}.pdf"
    target=os.path.join(out_dir, out_name)
    try:
        HTML(string=rendered).write_pdf(target)
        print(f"[OK] Cover letter {vac['id']}/{out_name}")
        # Registrar en applications.json
        apps_path=os.path.join(BASE_DIR, "data/applications.json")
        apps=json.load(open(apps_path, encoding="utf-8-sig"))
        for a in apps:
            if a["vacancy_id"]==vacancy_id:
                a["cover_letter"]=f"letters/{vac['id']}/{out_name}"
        json.dump(apps, open(apps_path,"w",encoding="utf-8"), ensure_ascii=False, indent=2)
    except PermissionError:
        print(f"[WARN] No se pudo sobrescribir {out_name} (abierto)")

if __name__=="__main__":
    import argparse
    ap=argparse.ArgumentParser()
    ap.add_argument("--vacancy", required=True, help="ID de vacante (ej. vac_001)")
    ap.add_argument("--lang", default="es", choices=["es","en"])
    args=ap.parse_args()
    generate_for_vacancy(args.vacancy, args.lang)
