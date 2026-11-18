import httpx
import asyncio

from recomendador import identificar_preferencias, recomendar_filmes
from services.tmdb_service import (
    buscar_series_diversificadas,
    buscar_detalhes_serie
)
from services.similaridade_service import gerar_embeddings_cloudflare


async def gerar_recomendacoes_series(avaliacoes, favoritos):
    # Calcula as preferências do usuário
    preferencias = await asyncio.to_thread(
        identificar_preferencias,
        avaliacoes,
        favoritos
    )

    generos = [
        genero
        for genero, pontos in preferencias.items()
        if pontos > 0
    ][:3]

    if not generos:
        generos = [18, 80]

    # Busca séries no TMDB
    series = await buscar_series_diversificadas(
        generos,
        quantidade=40
    )

    ids_excluidos = (
        {a["id"] for a in avaliacoes}
        | {f["id"] for f in favoritos}
    )

    # Reutiliza o algoritmo de recomendação
    resultado = recomendar_filmes(
        series,
        preferencias,
        ids_excluidos
    )

    # Séries avaliadas positivamente e favoritas
    ids_preferidos = {
        a["id"]
        for a in avaliacoes
        if a["nota"] >= 7
    }

    ids_preferidos.update(
        f["id"] for f in favoritos
    )

    sinopses_preferidas = []

    for serie_id in ids_preferidos:
        try:
            detalhes = await buscar_detalhes_serie(serie_id)

            if detalhes["sinopse"]:
                sinopses_preferidas.append(
                    detalhes["sinopse"]
                )
        except Exception:
            continue

    
    # Compara as sinopses usando IA da Cloudflare
    if sinopses_preferidas and resultado:
        textos = sinopses_preferidas + [
            serie.get("sinopse") or ""
            for serie in resultado
        ]

        try:
           embeddings = await gerar_embeddings_cloudflare(textos)

        except (httpx.HTTPError, RuntimeError, ValueError) as erro:
           print(f"Similaridade de séries indisponível: {erro}")

        recomendacoes = resultado[:10]

        return {
           "tipo_conteudo": "SERIE",
           "preferencias": preferencias,
           "total": len(recomendacoes),
           "recomendacoes": recomendacoes
        }


        quantidade_referencias = len(sinopses_preferidas)

        referencias = embeddings[:quantidade_referencias]
        candidatos = embeddings[quantidade_referencias:]

        # Calcula a similaridade do cosseno
        def similaridade_cosseno(vetor1, vetor2):
            produto = sum(
                a * b for a, b in zip(vetor1, vetor2)
            )

            norma1 = sum(a * a for a in vetor1) ** 0.5
            norma2 = sum(b * b for b in vetor2) ** 0.5

            if norma1 == 0 or norma2 == 0:
                return 0.0

            return produto / (norma1 * norma2)

        for serie, candidato in zip(resultado, candidatos):
            similaridade = max(
                0.0,
                max(
                    similaridade_cosseno(candidato, referencia)
                    for referencia in referencias
                )
            )

            serie["similaridade_sinopse"] = round(
                similaridade, 4
            )

            # Mantém os pesos originais do TVScore
            serie["score_recomendacao"] = round(
                serie["score_recomendacao"] * 0.8
                + similaridade * 100 * 0.2,
                2
            )

        resultado.sort(
            key=lambda serie: serie["score_recomendacao"],
            reverse=True
        )


    recomendacoes = resultado[:10]

    return {
        "tipo_conteudo": "SERIE",
        "preferencias": preferencias,
        "total": len(recomendacoes),
        "recomendacoes": recomendacoes
    }
