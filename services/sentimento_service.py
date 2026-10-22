
from functools import lru_cache
from transformers import pipeline

MODELO = "cardiffnlp/twitter-xlm-roberta-base-sentiment"


@lru_cache(maxsize=1)
def carregar_modelo():
    return pipeline(
        task="text-classification",
        model=MODELO,
        device=-1
    )


def analisar_sentimento(comentario: str):
    resultado = carregar_modelo()(comentario, truncation=True)[0]

    sentimentos = {
        "negative": "NEGATIVO",
        "neutral": "NEUTRO",
        "positive": "POSITIVO"
    }

    return {
        "sentimento": sentimentos.get(
            resultado["label"].lower(),
            resultado["label"]
        ),
        "confianca": round(resultado["score"], 4)
    }
