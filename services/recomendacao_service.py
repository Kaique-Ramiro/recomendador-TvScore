import httpx
import asyncio

from recomendador import identificar_preferencias, recomendar_filmes
from services.tmdb_service import buscar_filmes_diversificados, buscar_detalhes_filme
from services.similaridade_service import gerar_embeddings_cloudflare


async def gerar_recomendacoes(avaliacoes, favoritos):
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
        generos = [28, 878]

    filmes = await buscar_filmes_diversificados(generos, quantidade=40)

    ids_excluidos = (
        {a["id"] for a in avaliacoes}
        | {f["id"] for f in favoritos}
    )

    resultado = recomendar_filmes(
        filmes, preferencias, ids_excluidos
    )

    # Filmes que o usuário avaliou positivamente
    filmes_preferidos = [
        a["id"] for a in avaliacoes if a["nota"] >= 7
    ]

    filmes_preferidos += [
        f["id"] for f in favoritos
    ]

    sinopses_preferidas = []

    for filme_id in set(filmes_preferidos):
        try:
            detalhes = await buscar_detalhes_filme(filme_id)
            if detalhes["sinopse"]:
                sinopses_preferidas.append(detalhes["sinopse"])
        except Exception:
            continue

    
    if sinopses_preferidas and resultado:
        textos = sinopses_preferidas + [
            filme.get("sinopse") or ""
            for filme in resultado
        ]

        # Gera embeddings usando a IA da Cloudflare
        try:
           embeddings = await gerar_embeddings_cloudflare(textos)

        except (httpx.HTTPError, RuntimeError, ValueError) as erro:
           print(f"Similaridade indisponível: {erro}")

           recomendacoes = resultado[:10]

           return {
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

        for filme, candidato in zip(resultado, candidatos):
            similaridade = max(
                0.0,
                max(
                    similaridade_cosseno(candidato, referencia)
                    for referencia in referencias
                )
            )

            filme["similaridade_sinopse"] = round(
                similaridade, 4
            )

            # Mantém os pesos originais do TVScore
            filme["score_recomendacao"] = round(
                filme["score_recomendacao"] * 0.8
                + similaridade * 100 * 0.2,
                2
            )

        resultado.sort(
            key=lambda filme: filme["score_recomendacao"],
            reverse=True
        )


    recomendacoes = resultado[:10]

    return {
        "preferencias": preferencias,
        "total": len(recomendacoes),
        "recomendacoes": recomendacoes
    }
