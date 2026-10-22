
from fastapi import APIRouter, Query

from models.schemas import DadosUsuario
from services.tmdb_service import buscar_filmes
from services.recomendacao_service import gerar_recomendacoes

router = APIRouter(prefix="/recomendacoes", tags=["Recomendações"])


@router.get("")
async def recomendar(
    generos: list[int] = Query(default=[878, 28]),
    quantidade: int = Query(default=10, ge=1, le=20)
):
    filmes = await buscar_filmes(
        generos,
        quantidade,
        ordenar_por_nota=True
    )

    return {
        "generos_selecionados": generos,
        "total": len(filmes),
        "recomendacoes": filmes
    }


@router.get("/personalizadas")
async def recomendacoes_personalizadas():
    # Dados simulados para testes
    avaliacoes = [
        {"id": 157336, "nota": 10, "generos": [878, 12, 18]},
        {"id": 27205, "nota": 9, "generos": [28, 878, 12]},
        {"id": 550, "nota": 2, "generos": [18]}
    ]

    favoritos = [
        {"id": 603, "generos": [28, 878]}
    ]

    return await gerar_recomendacoes(
        avaliacoes, favoritos
    )


@router.post("/usuario")
async def recomendar_usuario(dados: DadosUsuario):
    avaliacoes = [
        a.model_dump() for a in dados.avaliacoes
    ]

    favoritos = [
        f.model_dump() for f in dados.favoritos
    ]

    return await gerar_recomendacoes(
        avaliacoes, favoritos
    )
