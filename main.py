from fastapi import FastAPI
from routes.recomendacoes import router as recomendacoes_router
from routes.sentimentos import router as sentimentos_router

app = FastAPI(
    title="TVScore - Sistema de Recomendação",
    version="1.0.0"
)

app.include_router(recomendacoes_router)
app.include_router(sentimentos_router)


@app.get("/")
def inicio():
    return {"mensagem": "TVScore funcionando!"}