from fastapi import FastAPI
import requests
import os
from dotenv import load_dotenv

# Cargar variables de entorno (.env en local, Environment Variables en Render)
load_dotenv()

app = FastAPI()

GNEWS_API_KEY = os.getenv("GNEWS_API_KEY")


def link_activo(url: str) -> bool:
    try:
        r = requests.head(url, timeout=5, allow_redirects=True)
        return r.status_code == 200
    except:
        return False


@app.get("/")
def home():
    return {"status": "API funcionando"}


@app.get("/noticias/{equipo}")
def noticias_equipo(equipo: str):
    if not GNEWS_API_KEY:
        return {"error": "API key de GNews no configurada"}

    url = "https://gnews.io/api/v4/search"
    params = {
        "q": equipo,
        "lang": "es",
        "max": 10,  # pedimos más para filtrar links rotos
        "apikey": GNEWS_API_KEY
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return {
            "equipo": equipo,
            "total_noticias": 0,
            "noticias": []
        }

    data = response.json()
    noticias = []

    for n in data.get("articles", []):
        url_noticia = n.get("url")

        if url_noticia and link_activo(url_noticia):
            noticias.append({
                "titulo": n.get("title"),
                "url": url_noticia,
                "fuente": n.get("source", {}).get("name")
            })

        if len(noticias) == 4:
            break

    return {
        "equipo": equipo,
        "total_noticias": len(noticias),
        "noticias": noticias
    }
