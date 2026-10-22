
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

        generos = filme.get("generos", [])
        nota_tmdb = filme.get("nota") or 0

        # Afinidade do usuário com os gêneros
        pontos_generos = sum(
            preferencias.get(genero, 0)
            for genero in generos
        )

        # Similaridade com o perfil de gêneros preferidos
        generos_preferidos = {
            genero
            for genero, pontos in preferencias.items()
            if pontos > 0
        }

        similaridade = (
            len(set(generos) & generos_preferidos)
            / len(set(generos) | generos_preferidos)
            if generos and generos_preferidos
            else 0
        )

        # Normalização dos pontos dos gêneros
        total_positivo = sum(
            max(0, pontos)
            for pontos in preferencias.values()
        )

        afinidade = (
            max(0, pontos_generos) / total_positivo
            if total_positivo > 0
            else 0
        )

        afinidade = min(1, afinidade)

        # Pontuação final entre 0 e 100
        score = (
            afinidade * 60
            + similaridade * 25
            + (nota_tmdb / 10) * 15
        )

        recomendacoes.append({
            **filme,
            "score_recomendacao": round(score, 2),
            "motivo_recomendacao": explicar_recomendacao(
                filme, preferencias
            )
        })

        return sorted(
        recomendacoes,
        key=lambda filme: filme["score_recomendacao"],
        reverse=True
    )
    


def explicar_recomendacao(filme, preferencias):
    nomes_generos = {
        28: "ação",
        12: "aventura",
        16: "animação",
        35: "comédia",
        80: "crime",
        18: "drama",
        14: "fantasia",
        27: "terror",
        9648: "mistério",
        10749: "romance",
        878: "ficção científica",
        53: "suspense",
        10752: "guerra",
        37: "faroeste"
    }

    generos_compativeis = [
        genero
        for genero in filme.get("generos", [])
        if preferencias.get(genero, 0) > 0
    ]

    generos_compativeis.sort(
        key=lambda genero: preferencias[genero],
        reverse=True
    )

    nomes = [
        nomes_generos.get(genero, f"gênero {genero}")
        for genero in generos_compativeis[:2]
    ]

    if len(nomes) == 2:
        return f"Recomendado porque você gosta de {nomes[0]} e {nomes[1]}."

    if len(nomes) == 1:
        return f"Recomendado porque você gosta de {nomes[0]}."

    return "Recomendado com base na avaliação do filme."

