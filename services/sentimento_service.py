
import os
import re

import httpx
from dotenv import load_dotenv

load_dotenv()

ACCOUNT_ID = os.getenv("CLOUDFLARE_ACCOUNT_ID")
API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN")

MODELO = "@cf/qwen/qwen3.8-27b"


def analisar_sentimento(comentario: str):
    if not ACCOUNT_ID or not API_TOKEN:
        raise RuntimeError(
            "Credenciais da Cloudflare não configuradas no .env"
        )

    url = (
        "https://api.cloudflare.com/client/v4/accounts/"
        f"{ACCOUNT_ID}/ai/run/{MODELO}"
    )

    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }

    dados = {
        "messages": [
            {
                "role": "system",
                "content": (
                    "Você é um classificador de sentimentos "
                    "de comentários sobre filmes e séries. "
                    "Classifique o sentimento do comentário "
                    "como POSITIVO, NEGATIVO ou NEUTRO. "
                    "Responda exclusivamente com uma dessas "
                    "três palavras, sem explicações."
                )
            },
            {
                "role": "user",
                "content": comentario
            }
        ],
        "temperature": 0,
        "max_tokens": 100
    }

    with httpx.Client(timeout=120) as cliente:
        resposta = cliente.post(
            url,
            headers=headers,
            json=dados
        )
        resposta.raise_for_status()

    resultado = resposta.json()

    if not resultado.get("success", False):
        raise RuntimeError(
            f"Erro na Cloudflare: {resultado.get('errors')}"
        )

    conteudo = resultado.get("result", {})

    texto = conteudo.get("response", "")

    if not texto and conteudo.get("choices"):
        texto = conteudo["choices"][0]["message"]["content"]

    texto = str(texto).strip().upper()

    # Aceita somente uma classificação válida
    correspondencia = re.fullmatch(
        r"(POSITIVO|NEGATIVO|NEUTRO)[.!]?",
        texto
    )

    if not correspondencia:
        raise RuntimeError(
            f"Classificação inesperada da IA: {texto}"
        )

    
    return {
        "sentimento": correspondencia.group(1)
    }

