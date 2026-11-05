from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def inicio():
    return {"mensagem": "Teste Render funcionando!"}

@app.get("/teste-imports")
def testar_imports():
    from transformers import pipeline
    from sentence_transformers import SentenceTransformer

    return {"mensagem": "Bibliotecas de IA importadas com sucesso!"}

@app.get("/teste-transformers")
def testar_transformers():
    from transformers import pipeline

    return {"mensagem": "Transformers importado com sucesso!"}