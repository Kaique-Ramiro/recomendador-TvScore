
from recomendador import (
    identificar_preferencias,
    recomendar_filmes
)
from services.tmdb_service import buscar_filmes


async def gerar_recomendacoes(avaliacoes, favoritos):
    preferencias = identificar_preferencias(
        avaliacoes, favoritos
    )

    generos = [
        genero
        for genero, pontos in preferencias.items()
        if pontos > 0
    ][:3]

    if not generos:
        generos = [28, 878]

    filmes = await buscar_filmes(generos)

    ids_excluidos = (
        {a["id"] for a in avaliacoes}
        | {f["id"] for f in favoritos}
    )

    resultado = recomendar_filmes(
        filmes,
        preferencias,
        ids_excluidos
    )

    return {
        "preferencias": preferencias,
        "total": len(resultado[:10]),
        "recomendacoes": resultado[:10]
    }
