
from functools import lru_cache
from sentence_transformers import SentenceTransformer, util


@lru_cache(maxsize=1)
def carregar_modelo():
    return SentenceTransformer(
        "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )


def calcular_similaridade(sinopse1, sinopse2):
    modelo = carregar_modelo()

    embeddings = modelo.encode(
        [sinopse1, sinopse2],
        convert_to_tensor=True
    )

    similaridade = util.cos_sim(
        embeddings[0],
        embeddings[1]
    ).item()

    return round(similaridade, 4)
