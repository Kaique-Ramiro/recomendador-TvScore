
import httpx
from fastapi import HTTPException
from config import TMDB_API_KEY, TMDB_URL


async def buscar_filmes(generos, quantidade=20, ordenar_por_nota=False):
    if not TMDB_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="Chave TMDB não configurada."
        )

    parametros = {
        "api_key": TMDB_API_KEY,
        "language": "pt-BR",
        "with_genres": "|".join(map(str, generos)),
        "vote_count.gte": 200,
        "include_adult": "false",
        "page": 1
    }

    if ordenar_por_nota:
        parametros["sort_by"] = "vote_average.desc"

    try:
        async with httpx.AsyncClient(timeout=15) as client:
            resposta = await client.get(
                f"{TMDB_URL}/discover/movie",
                params=parametros
            )
            resposta.raise_for_status()
            dados = resposta.json()

    except httpx.HTTPError:
        raise HTTPException(
            status_code=502,
            detail="Erro ao consultar o TMDB."
        )

    filmes = []

    for filme in dados.get("results", [])[:quantidade]:
        poster = filme.get("poster_path")

        filmes.append({
            "id": filme["id"],
            "titulo": filme.get("title"),
            "sinopse": filme.get("overview"),
            "nota": filme.get("vote_average") or 0,
            "generos": filme.get("genre_ids", []),
            "poster": (
                f"https://image.tmdb.org/t/p/w500{poster}"
                if poster else None
            )
        })

    return filmes


async def buscar_detalhes_filme(filme_id: int):
    if not TMDB_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="Chave TMDB não configurada."
        )

    url = f"{TMDB_URL}/movie/{filme_id}"

    parametros = {
        "api_key": TMDB_API_KEY,
        "language": "pt-BR"
    }

    try:
        async with httpx.AsyncClient(timeout=15) as client:
            resposta = await client.get(
                url,
                params=parametros
            )
            resposta.raise_for_status()

            dados = resposta.json()

            return {
                "id": dados["id"],
                "titulo": dados["title"],
                "sinopse": dados.get("overview", ""),
                "generos": [
                    genero["id"]
                    for genero in dados.get("genres", [])
                ]
            }

    except httpx.HTTPError:
        raise HTTPException(
            status_code=502,
            detail="Erro ao buscar detalhes do filme no TMDB."
        )

