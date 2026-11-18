
import httpx
import asyncio

from recomendador import identificar_preferencias, recomendar_filmes
from services.tmdb_service import (
    buscar_filmes_diversificados,
    buscar_detalhes_filme
)
from services.similaridade_service import gerar_embeddings_cloudflare
from services.onboarding_service import aplicar_sinais


async def gerar_recomendacoes(
    avaliacoes,
    favoritos,
    onboarding=None
):
    onboarding = onboarding or {
        "generos": [],
        "preferidos": []
    }

    # Calcula as preferências pelas avaliações e favoritos
    preferencias = await asyncio.to_thread(
        identificar_preferencias,
        avaliacoes,
        favoritos
    )

    # Adiciona as preferências escolhidas no cadastro
    preferencias = aplicar_sinais(
        preferencias,
        onboarding
    )

    generos = [
        genero
        for genero, pontos in preferencias.items()
        if pontos > 0
    ][:3]

    if not generos:
        generos = [28, 878]

    # Busca filmes no TMDB
    filmes = await buscar_filmes_diversificados(
        generos,
        quantidade=40
    )

    # Evita recomendar conteúdos já conhecidos
    ids_excluidos = (
        {a["id"] for a in avaliacoes}
        | {f["id"] for f in favoritos}
        | {
            item["id"]
            for item in onboarding["preferidos"]
        }
    )

    resultado = recomendar_filmes(
        filmes,
        preferencias,
        ids_excluidos
    )

    # Filmes avaliados positivamente e favoritos
    ids_preferidos = {
        a["id"]
        for a in avaliacoes
        if a["nota"] >= 7
    }

    ids_preferidos.update(
        f["id"] for f in favoritos
    )

    sinopses_preferidas = []

    for filme_id in ids_preferidos:
        try:
            detalhes = await buscar_detalhes_filme(filme_id)

            if detalhes["sinopse"]:
                sinopses_preferidas.append(
                    detalhes["sinopse"]
                )

        except Exception:
            continue

    # Inclui os filmes escolhidos no cadastro
    for item in onboarding["preferidos"]:
        sinopse = item.get("sinopse")

        if sinopse:
            sinopses_preferidas.append(sinopse)

    # Compara sinopses usando a IA da Cloudflare
    if sinopses_preferidas and resultado:
        textos = sinopses_preferidas + [
            filme.get("sinopse") or ""
            for filme in resultado
        ]

        try:
            embeddings = await gerar_embeddings_cloudflare(
                textos
            )

            quantidade_referencias = len(
                sinopses_preferidas
            )

            if len(embeddings) != len(textos):
                raise ValueError(
                    "Quantidade de embeddings inválida."
                )

            referencias = embeddings[:quantidade_referencias]
            candidatos = embeddings[quantidade_referencias:]

            def similaridade_cosseno(vetor1, vetor2):
                produto = sum(
                    a * b for a, b in zip(vetor1, vetor2)
                )

                norma1 = sum(a * a for a in vetor1) ** 0.5
                norma2 = sum(b * b for b in vetor2) ** 0.5

                if norma1 == 0 or norma2 == 0:
                    return 0.0

                return produto / (norma1 * norma2)

            for filme, candidato in zip(
                resultado,
                candidatos
            ):
                similaridade = max(
                    0.0,
                    max(
                        similaridade_cosseno(
                            candidato,
                            referencia
                        )
                        for referencia in referencias
                    )
                )

                filme["similaridade_sinopse"] = round(
                    similaridade, 4
                )

                # 80% algoritmo + 20% similaridade da IA
                filme["score_recomendacao"] = round(
                    filme["score_recomendacao"] * 0.8
                    + similaridade * 100 * 0.2,
                    2
                )

            resultado.sort(
                key=lambda filme: filme["score_recomendacao"],
                reverse=True
            )

        except (httpx.HTTPError, RuntimeError, ValueError) as erro:
            print(
                f"Similaridade de filmes indisponível: {erro}"
            )

    recomendacoes = resultado[:10]

    return {
        "preferencias": preferencias,
        "total": len(recomendacoes),
        "recomendacoes": recomendacoes
    }
