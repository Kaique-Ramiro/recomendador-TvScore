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

@app.get("/teste-modelo-sentimento")
def testar_modelo_sentimento():
    print("INICIANDO TESTE DE SENTIMENTOS", flush=True)

    from services.sentimento_service import analisar_sentimento

    print("IMPORT CONCLUIDO", flush=True)

    resultado = analisar_sentimento("Esse filme é incrível!")

    print("ANALISE CONCLUIDA", flush=True)

    return resultado