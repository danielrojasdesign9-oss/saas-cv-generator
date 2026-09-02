#!/usr/bin/env python3
"""
Helper simple para el sistema de gestiÃ³n por vacante.
Uso:
  python manage.py add-vacancy --empresa "X" --rol "Y" --jd "..." 
  python manage.py list
  python manage.py update-status --app app_001 --estado entrevista
  python manage.py recommend --app app_001   # imprime recomendaciones (simuladas, la IA real las genera)
  python manage.py apply-one-click --app app_001  # marca como aplicado y sugiere regenerar CV
"""
import json, os, uuid, argparse
from datetime import date

BASE = os.path.dirname(os.path.abspath(__file__))
VAC = os.path.join(BASE, "data", "vacancies.json")
APP = os.path.join(BASE, "data", "applications.json")

def load(p): 
    return json.load(open(p, encoding='utf-8-sig')) if os.path.exists(p) else []

def save(p, data): 
    json.dump(data, open(p, "w", encoding='utf-8-sig'), ensure_ascii=False, indent=2)
    print(f"[OK] {p}")

def add_vacancy(empresa, rol, jd, url):
    vacs = load(VAC)
    vacs.append({"id": f"vac_{uuid.uuid4().hex[:6]}", "empresa": empresa, "rol": rol, "jd_text": jd, "url": url or "", "creada_en": str(date.today())})
    save(VAC, vacs)

def list_all():
    print("=== Vacantes ==="); print(json.dumps(load(VAC), ensure_ascii=False, indent=2))
    print("\n=== Aplicaciones ==="); print(json.dumps(load(APP), ensure_ascii=False, indent=2))

def update_status(app_id, estado):
    apps = load(APP)
    for a in apps:
        if a["id"] == app_id:
            a["estado"] = estado
            save(APP, apps)
            print(f"[OK] {app_id} -> {estado}")
            return
    print(f"[WARN] no se encontrÃ³ {app_id}")

def recommend(app_id):
    apps = load(APP)
    for a in apps:
        if a["id"] == app_id:
            print(f"Recomendaciones para {app_id} (ATS {a.get('ats_score')}):")
            for r in a.get("recomendaciones", []):
                print(" -", r)
            print("\nPara aplicar en 1 clic, edita data/cv_es.json y cv_en.json con estas recomendaciones y corre: python generate_cv.py")
            return
    print(f"[WARN] no se encontrÃ³ {app_id}")

def apply_one_click(app_id):
    apps = load(APP)
    for a in apps:
        if a["id"] == app_id:
            a["aplicado_1_clic"] = True
            save(APP, apps)
            print(f"[OK] {app_id} marcado como aplicado en 1 clic. Regenera el CV vinculado (cv_id={a['cv_id']}).")
            return
    print(f"[WARN] no se encontrÃ³ {app_id}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd")
    p1 = sub.add_parser("add-vacancy"); p1.add_argument("--empresa", required=True); p1.add_argument("--rol", required=True); p1.add_argument("--jd", required=True); p1.add_argument("--url", default="")
    sub.add_parser("list")
    p2 = sub.add_parser("update-status"); p2.add_argument("--app", required=True); p2.add_argument("--estado", required=True, choices=["enviado","visto","entrevista","rechazado","oferta"])
    p3 = sub.add_parser("recommend"); p3.add_argument("--app", required=True)
    p4 = sub.add_parser("apply-one-click"); p4.add_argument("--app", required=True)
    args = ap.parse_args()
    if args.cmd == "add-vacancy": add_vacancy(args.empresa, args.rol, args.jd, args.url)
    elif args.cmd == "list": list_all()
    elif args.cmd == "update-status": update_status(args.app, args.estado)
    elif args.cmd == "recommend": recommend(args.app)
    elif args.cmd == "apply-one-click": apply_one_click(args.app)
    else: ap.print_help()
