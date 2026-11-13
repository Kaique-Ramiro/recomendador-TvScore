
from functools import lru_cache
import json

import numpy as np
import onnxruntime as ort
from huggingface_hub import hf_hub_download
from tokenizers import Tokenizer


MODELO = "Horizon-Labs/multilingual-sentiment-small"


@lru_cache(maxsize=1)
def carregar_modelo():
    print("Carregando modelo ONNX quantizado...")

    caminho_modelo = hf_hub_download(
        repo_id=MODELO,
        filename="onnx/model_quantized.onnx"
    )

    caminho_tokenizer = hf_hub_download(
        repo_id=MODELO,
        filename="tokenizer.json"
    )

    caminho_config = hf_hub_download(
        repo_id=MODELO,
        filename="config.json"
    )

    tokenizer = Tokenizer.from_file(caminho_tokenizer)
    tokenizer.enable_truncation(max_length=256)

    with open(caminho_config, encoding="utf-8") as arquivo:
        config = json.load(arquivo)

    labels = config.get("id2label", {})

    sessao = ort.InferenceSession(
        caminho_modelo,
        providers=["CPUExecutionProvider"]
    )

    print("Modelo ONNX carregado!")

    return sessao, tokenizer, labels


def analisar_sentimento(comentario: str):
    sessao, tokenizer, labels = carregar_modelo()

    entrada = tokenizer.encode(comentario)

    dados = {
        "input_ids": np.array(
            [entrada.ids], dtype=np.int64
        ),
        "attention_mask": np.array(
            [entrada.attention_mask], dtype=np.int64
        ),
        "token_type_ids": np.array(
            [entrada.type_ids], dtype=np.int64
        )
    }

    entradas_modelo = {
        item.name: dados[item.name]
        for item in sessao.get_inputs()
    }

    logits = sessao.run(
        None, entradas_modelo
    )[0][0]

    logits = logits - np.max(logits)
    probabilidades = np.exp(logits)
    probabilidades /= probabilidades.sum()

    indice = int(np.argmax(probabilidades))
    label = labels.get(str(indice), "").lower()

    sentimentos = {
        "negative": "NEGATIVO",
        "neutral": "NEUTRO",
        "positive": "POSITIVO",
        "negativo": "NEGATIVO",
        "neutro": "NEUTRO",
        "positivo": "POSITIVO"
    }

    if label not in sentimentos:
        raise ValueError(
            f"Rótulo do modelo não reconhecido: {label!r}. "
            f"Configuração: {labels}"
        )

    return {
        "sentimento": sentimentos[label],
        "confianca": round(
            float(probabilidades[indice]), 4
        )
    }
