
import asyncio
import os
import httpx

from fastapi import HTTPException
from dotenv import load_dotenv

load_dotenv()

JAVA_API_URL = os.getenv(
    "JAVA_API_URL",
    "http://localhost:8080"
).rstrip("/")


async def buscar_dados_usuario(token: str):
    rotas = {
        "avaliacoes": "/api/avaliacoes/minhas",
        "favoritos": "/api/favoritos",
        "generos": "/api/usuarios/eu/generos",
        "preferidos": "/api/usuarios/eu/conteudos-preferidos"
    }

    try:
        async with httpx.AsyncClient(timeout=15) as client:

            async def consultar(chave, rota):
                resposta = await client.get(
                    JAVA_API_URL + rota,
                    headers={
                        "Authorization": f"Bearer {token}"
                    }
                )

                resposta.raise_for_status()
                return chave, resposta.json()

            resultados = await asyncio.wait_for(
                asyncio.gather(
                    *[
                        consultar(chave, rota)
                        for chave, rota in rotas.items()
                    ]
                ),
                timeout=20
            )

            return dict(resultados)

    except httpx.HTTPStatusError as erro:
        status = erro.response.status_code

        if status in (401, 403):
            raise HTTPException(
                status_code=status,
                detail="Acesso não autorizado pelo Java."
            )

        raise HTTPException(
            status_code=502,
            detail="Erro ao consultar o backend Java."
        )

    except (httpx.RequestError, asyncio.TimeoutError):
        raise HTTPException(
            status_code=502,
            detail="Não foi possível consultar o backend Java."
        )
