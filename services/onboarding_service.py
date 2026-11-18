
import asyncio
import re
import unicodedata
import httpx

from fastapi import HTTPException
from config import TMDB_API_KEY, TMDB_URL


def normalizar(nome):
    texto = unicodedata.normalize("NFKD", str(nome))
    return re.sub(
        r"[^a-z0-9]+",
        "-",
        "".join(
            c for c in texto
            if not unicodedata.combining(c)
        ).lower()
    ).strip("-")


async def preparar_onboarding(dados):
    saida = {
        "filmes": {"generos": [], "preferidos": []},
        "series": {"generos": [], "preferidos": []}
    }

    vistos = set()

    for item in dados.get("preferidos", {}).get("conteudos", []):
        tipo = item.get("tipoConteudo")

        if tipo == "SERIE":
            tipo = "TV"

        conteudo_id = item.get("id")
        chave = (tipo, conteudo_id)

        if (
            tipo not in ("MOVIE", "TV")
            or not isinstance(conteudo_id, int)
            or chave in vistos
        ):
            continue

        vistos.add(chave)

        destino = saida[
            "filmes" if tipo == "MOVIE" else "series"
        ]

        destino["preferidos"].append({
            "id": conteudo_id,
            "generos": [
                g["id"]
                for g in item.get("generos", [])
                if isinstance(g, dict)
                and isinstance(g.get("id"), int)
            ],
            "sinopse": item.get("sinopse") or ""
        })

    selecionados = dados.get("generos", {}).get("generos", [])

    if not selecionados:
        return saida

    if not TMDB_API_KEY:
        raise HTTPException(
            status_code=503,
            detail="TMDB não configurado."
        )

    async with httpx.AsyncClient(timeout=10) as client:

        async def resolver(tipo, destino):
            try:
                resposta = await client.get(
                    f"{TMDB_URL}/genre/{tipo}/list",
                    params={
                        "api_key": TMDB_API_KEY,
                        "language": "pt-BR"
                    }
                )

                resposta.raise_for_status()
                catalogo = resposta.json()["genres"]

                for genero in catalogo:
                    for selecionado in selecionados:
                        codigo = selecionado.get("codigo", "")

                        if (
                            codigo == f"tmdb-{genero['id']}"
                            or normalizar(selecionado.get("nome"))
                            == normalizar(genero["name"])
                        ):
                            destino["generos"].append(genero["id"])
                            break

            except (httpx.HTTPError, ValueError, KeyError, TypeError):
                raise HTTPException(
                    status_code=502,
                    detail="Erro ao consultar gêneros do TMDB."
                ) from None

        await asyncio.gather(
            resolver("movie", saida["filmes"]),
            resolver("tv", saida["series"])
        )

    return saida


def aplicar_sinais(preferencias, onboarding):
    pontos = dict(preferencias)

    # Cada gênero escolhido recebe 2 pontos
    for genero in set(onboarding.get("generos", [])):
        pontos[genero] = pontos.get(genero, 0) + 2

    # Cada título escolhido acrescenta 1 ponto por gênero
    for item in onboarding.get("preferidos", []):
        for genero in set(item.get("generos", [])):
            pontos[genero] = pontos.get(genero, 0) + 1

    return dict(
        sorted(
            pontos.items(),
            key=lambda item: (-item[1], item[0])
        )
    )
