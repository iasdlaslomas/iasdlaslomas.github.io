"""Genera escuela.json con la lección de Escuela Sabática (adultos) del trimestre en curso.

Fuente: API pública de Adventech, la misma que alimenta sabbath.school y la app oficial
"Sabbath School". Solo se guardan títulos, fechas, el versículo para memorizar, las
lecturas y los enlaces al material oficial (lectura, audio y videos): el texto completo
de la lección se lee en sabbath.school.

Lo corre la Action "Actualizar Escuela Sabática"; también se puede correr a mano:
    python .github/escuela.py
"""
import html
import json
import re
import urllib.request
from datetime import date, datetime, timedelta

API = "https://sabbath-school.adventech.io/api/v2/es"
LEER = "https://www.sabbath.school/Lesson?lang=2&year={a}&quarter={t}&lesson={n}"


def get(ruta):
    with urllib.request.urlopen(f"{API}/{ruta}", timeout=30) as r:
        return json.load(r)


def iso(s):
    return datetime.strptime(s, "%d/%m/%Y").date()


def texto(fragmento):
    sin_tags = re.sub(r"<[^>]+>", " ", fragmento)
    limpio = re.sub(r"\s+", " ", html.unescape(sin_tags)).strip()
    return re.sub(r"\s+([).,;])", r"\1", re.sub(r"\(\s+", "(", limpio))


MENORES = {"a", "al", "con", "de", "del", "el", "en", "la", "las", "lo", "los", "o", "para", "por", "que", "su", "sus", "un", "una", "y"}


def titulo_dia(t):
    # La API pone Mayúscula En Cada Palabra; artículos y preposiciones van en minúscula.
    palabras = t.split()
    return " ".join(p if i == 0 or p.lower() not in MENORES else p.lower() for i, p in enumerate(palabras))


def trimestre_actual(hoy):
    # Solo la edición para adultos (los ids con sufijo, como -cq, son de jóvenes).
    adultos = [q for q in get("quarterlies/index.json") if re.fullmatch(r"\d{4}-\d{2}", q["id"])]
    adultos.sort(key=lambda q: iso(q["start_date"]))
    # Sigue vigente hasta el sábado de su última clase (el día después de end_date).
    for q in adultos:
        if iso(q["end_date"]) + timedelta(days=1) >= hoy:
            return q["id"]
    return adultos[-1]["id"]


def main():
    hoy = date.today()
    qid = trimestre_actual(hoy)
    anio, num = int(qid[:4]), int(qid[5:])
    data = get(f"quarterlies/{qid}/index.json")
    q = data["quarterly"]

    audios = {a["target"]: a["src"] for a in get(f"quarterlies/{qid}/audio.json")}
    videos = {}
    for canal in get(f"quarterlies/{qid}/video.json"):
        for c in canal.get("clips", []):
            videos.setdefault(c["target"], []).append(
                {"autor": canal["artist"], "src": c["src"], "miniatura": c.get("thumbnail")})

    lecciones = []
    for l in data["lessons"]:
        n = int(l["id"])
        lec = get(f"quarterlies/{qid}/lessons/{l['id']}/index.json")
        portada = get(f"quarterlies/{qid}/lessons/{l['id']}/days/01/read/index.json")["content"]
        memo = re.search(r"Para memorizar</p>(.*?)</blockquote>", portada, re.S)
        lect = re.search(r"Lee para el estudio de esta semana</h3>\s*<p>(.*?)</p>", portada, re.S)
        fin = iso(l["end_date"])
        lecciones.append({
            "n": n,
            "titulo": l["title"],
            "inicio": iso(l["start_date"]).isoformat(),
            "fin": fin.isoformat(),
            "clase": (fin + timedelta(days=1)).isoformat(),
            "memorizar": texto(memo.group(1)) if memo else "",
            "lecturas": texto(lect.group(1)).rstrip(".") if lect else "",
            "leer": LEER.format(a=anio, t=num, n=n),
            "dias": [{
                "fecha": iso(d["date"]).isoformat(),
                "titulo": titulo_dia(d["title"]),
                "audio": audios.get(f"es/{qid}/{l['id']}/{d['id']}"),
            } for d in lec["days"]],
            "videos": videos.get(f"es/{qid}/{l['id']}", []),
        })

    salida = {
        "trimestre": {
            "id": qid,
            "anio": anio,
            "numero": num,
            "titulo": q["title"],
            "fechas": q["human_date"],
            "descripcion": q.get("description", ""),
            "portada": f"https://sabbath-school.adventech.io/api/v1/es/quarterlies/{qid}/cover.png",
        },
        "lecciones": lecciones,
    }
    with open("escuela.json", "w", encoding="utf-8") as f:
        json.dump(salida, f, ensure_ascii=False, indent=1)
    print(f"escuela.json: {qid} · {q['title']} · {len(lecciones)} lecciones")


if __name__ == "__main__":
    main()
