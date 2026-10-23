
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
    
async def buscar_filmes_diversificados(generos, quantidade=40):
    if not TMDB_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="Chave TMDB não configurada."
        )

    filmes_encontrados = {}

    # Busca filmes dos gêneros favoritos e filmes populares
    buscas = [
        {"with_genres": "|".join(map(str, generos))},
        {"sort_by": "popularity.desc"},
        {"sort_by": "vote_average.desc", "vote_count.gte": 500}
    ]

    async with httpx.AsyncClient(timeout=15) as client:
        for filtros in buscas:
            parametros = {
                "api_key": TMDB_API_KEY,
                "language": "pt-BR",
                "include_adult": "false",
                "page": 1,
                **filtros
            }

            try:
                resposta = await client.get(
                    f"{TMDB_URL}/discover/movie",
                    params=parametros
                )
                resposta.raise_for_status()
            except httpx.HTTPError:
                continue

            for filme in resposta.json().get("results", []):
                if not filme.get("overview"):
                    continue

                poster = filme.get("poster_path")

                filmes_encontrados[filme["id"]] = {
                    "id": filme["id"],
                    "titulo": filme.get("title"),
                    "sinopse": filme.get("overview"),
                    "nota": filme.get("vote_average") or 0,
                    "generos": filme.get("genre_ids", []),
                    "poster": (
                        f"https://image.tmdb.org/t/p/w500{poster}"
                        if poster else None
                    )
                }

    return list(filmes_encontrados.values())[:quantidade]


async def buscar_series_diversificadas(generos, quantidade=40):
    if not TMDB_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="Chave TMDB não configurada."
        )

    series_encontradas = {}

    buscas = [
        {"with_genres": "|".join(map(str, generos))},
        {"sort_by": "popularity.desc"},
        {
            "sort_by": "vote_average.desc",
            "vote_count.gte": 500
        }
    ]

    async with httpx.AsyncClient(timeout=15) as client:
        for filtros in buscas:
            parametros = {
                "api_key": TMDB_API_KEY,
                "language": "pt-BR",
                "include_adult": "false",
                "page": 1,
                **filtros
            }

            try:
                resposta = await client.get(
                    f"{TMDB_URL}/discover/tv",
                    params=parametros
                )
                resposta.raise_for_status()
            except httpx.HTTPError:
                continue

            for serie in resposta.json().get("results", []):
                if not serie.get("overview"):
                    continue

                poster = serie.get("poster_path")

                series_encontradas[serie["id"]] = {
                    "id": serie["id"],
                    "titulo": serie.get("name"),
                    "sinopse": serie.get("overview"),
                    "nota": serie.get("vote_average") or 0,
                    "generos": serie.get("genre_ids", []),
                    "poster": (
                        f"https://image.tmdb.org/t/p/w500{poster}"
                        if poster else None
                    ),
                    "tipo_conteudo": "SERIE"
                }

    return list(series_encontradas.values())[:quantidade]


async def buscar_detalhes_serie(serie_id: int):
    if not TMDB_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="Chave TMDB não configurada."
        )

    try:
        async with httpx.AsyncClient(timeout=15) as client:
            resposta = await client.get(
                f"{TMDB_URL}/tv/{serie_id}",
                params={
                    "api_key": TMDB_API_KEY,
                    "language": "pt-BR"
                }
            )

            resposta.raise_for_status()
            dados = resposta.json()

            return {
                "id": dados["id"],
                "titulo": dados.get("name"),
                "sinopse": dados.get("overview", ""),
                "generos": [
                    genero["id"]
                    for genero in dados.get("genres", [])
                ],
                "tipo_conteudo": "SERIE"
            }

    except httpx.HTTPError:
        raise HTTPException(
            status_code=502,
            detail="Erro ao buscar detalhes da série no TMDB."
        )




