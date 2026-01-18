from fastapi import FastAPI
from typing import List
import feedparser
from urllib.parse import quote


app = FastAPI(
    title="Noticias Fútbol Femenino",
    version="1.0.0"
)

EQUIPOS_POR_PAIS = {
    "espana": [
        "Barcelona Femenino",
        "Real Madrid Femenino",
        "Atlético de Madrid Femenino",
        "Levante Femenino",
        "Real Sociedad Femenino",
        "Athletic Club Femenino",
        "Sevilla Femenino",
        "Valencia Femenino",
        "Granada Femenino",
        "Real Betis Femenino"
    ],
    "inglaterra": [
        "Chelsea Women",
        "Arsenal Women",
        "Manchester City Women",
        "Manchester United Women",
        "Tottenham Women",
        "Aston Villa Women",
        "Everton Women",
        "West Ham Women",
        "Brighton Women",
        "Leicester City Women"
    ],
    "estados-unidos": [
        "Portland Thorns",
        "OL Reign",
        "San Diego Wave",
        "Angel City FC",
        "North Carolina Courage",
        "Orlando Pride",
        "Chicago Red Stars",
        "Washington Spirit",
        "Racing Louisville",
        "Kansas City Current"
    ]
}

def buscar_noticias(equipo: str, limite: int = 4):
    try:
        query = quote(f"{equipo} fútbol femenino")
        rss_url = f"https://news.google.com/rss/search?q={query}&hl=es&gl=ES&ceid=ES:es"

        feed = feedparser.parse(rss_url)

        noticias = []
        if not feed.entries:
            return noticias

        for entry in feed.entries[:limite]:
            noticias.append({
                "titulo": entry.get("title", ""),
                "url": entry.get("link", ""),
                "fuente": entry.get("source", {}).get("title", "Google News")
            })

        return noticias

    except Exception:
        return []



@app.get("/")
def home():
    return {
        "mensaje": "API de noticias de fútbol femenino activa",
        "uso": "/ranking/{pais}/{numero_equipos}"
    }


@app.get("/ranking/{pais}/{numero_equipos}")
def ranking_noticias(pais: str, numero_equipos: int):
    pais = pais.lower()

    if pais not in EQUIPOS_POR_PAIS:
        return {"error": "País no soportado"}

    equipos = EQUIPOS_POR_PAIS[pais][:numero_equipos]

    resultado = []
    for equipo in equipos:
        noticias = buscar_noticias(equipo)
        resultado.append({
            "equipo": equipo,
            "total_noticias": len(noticias),
            "noticias": noticias
        })

    if not resultado:
        return {
            "mensaje": "La API no devolvió noticias para los equipos seleccionados."
        }

    return {
        "pais": pais,
        "ranking_equipos": numero_equipos,
        "equipos": resultado
    }
