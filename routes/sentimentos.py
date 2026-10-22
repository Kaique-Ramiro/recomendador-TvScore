
from fastapi import APIRouter
from pydantic import BaseModel, Field
from services.sentimento_service import analisar_sentimento

router = APIRouter(prefix="/sentimentos", tags=["Sentimentos"])


class ComentarioEntrada(BaseModel):
    comentario: str = Field(min_length=1, max_length=3000)


@router.post("/analisar")
def analisar(dados: ComentarioEntrada):
    return analisar_sentimento(dados.comentario)
