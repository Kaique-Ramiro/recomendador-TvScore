
from fastapi import FastAPI
from routes.sentimentos import router as sentimentos_router

app = FastAPI(
    title="TVScore - Análise de Sentimentos",
    version="1.0.0"
)

app.include_router(sentimentos_router)

@app.get("/")
def inicio():
    return {"mensagem": "TVScore Sentimentos funcionando!"}
