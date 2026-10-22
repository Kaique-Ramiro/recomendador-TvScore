
from collections import defaultdict


from services.sentimento_service import analisar_sentimento


def identificar_preferencias(avaliacoes, favoritos):
    pontuacao = defaultdict(float)

    for avaliacao in avaliacoes:
        nota = avaliacao["nota"]
        comentario = avaliacao.get("comentario")

        # A nota continua sendo o fator principal
        pontos = nota - 5

        if comentario and comentario.strip():
            analise = analisar_sentimento(comentario)

            ajustes = {
                "POSITIVO": 1.5,
                "NEUTRO": 0,
                "NEGATIVO": -1.5
            }

            pontos += (
                ajustes.get(analise["sentimento"], 0)
                * analise["confianca"]
            )

        for genero in avaliacao["generos"]:
            pontuacao[genero] += pontos

    for favorito in favoritos:
        for genero in favorito["generos"]:
            pontuacao[genero] += 3

    return dict(
        sorted(
            pontuacao.items(),
            key=lambda item: item[1],
            reverse=True
        )
    )


def recomendar_filmes(filmes, preferencias, avaliados):
    recomendacoes = []

    for filme in filmes:
        if filme["id"] in avaliados:
            continue

        score = sum(
            preferencias.get(genero, 0)
            for genero in filme["generos"]
        )

        score += filme["nota"] * 0.2

        recomendacoes.append({
            **filme,
            "score_recomendacao": round(score, 2)
        })

    return sorted(
        recomendacoes,
        key=lambda filme: filme["score_recomendacao"],
        reverse=True
    )
