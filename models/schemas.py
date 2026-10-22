
from pydantic import BaseModel, Field


class AvaliacaoEntrada(BaseModel):
    id: int
    nota: float = Field(ge=0, le=10)
    generos: list[int]
    comentario: str | None = None


class FavoritoEntrada(BaseModel):
    id: int
    generos: list[int]


class DadosUsuario(BaseModel):
    avaliacoes: list[AvaliacaoEntrada]
    favoritos: list[FavoritoEntrada]
