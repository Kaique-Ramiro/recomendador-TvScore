
from fastapi import FastAPI
from routes.recomendacoes import router as recomendacoes_router

app = FastAPI(
    title="TVScore - Recomendações",
    version="1.0.0"
)

app.include_router(recomendacoes_router)

@app.get("/")
def inicio():
    return {"mensagem": "TVScore Recomendações funcionando!"}
