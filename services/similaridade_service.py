async def gerar_embeddings_cloudflare(textos):
    import os
    import httpx
    from dotenv import load_dotenv

    load_dotenv()

    account_id = os.getenv("CLOUDFLARE_ACCOUNT_ID")
    api_token = os.getenv("CLOUDFLARE_API_TOKEN")

    if not account_id or not api_token:
        raise RuntimeError(
            "Credenciais da Cloudflare não configuradas"
        )

    if not textos:
        return []

    url = (
        "https://api.cloudflare.com/client/v4/accounts/"
        f"{account_id}/ai/run/@cf/qwen/qwen3-embedding-0.6b"
    )

    textos_validos = [
        texto.strip() if texto and texto.strip()
        else "Sinopse indisponível"
        for texto in textos
    ]

    async with httpx.AsyncClient(timeout=120) as cliente:
        resposta = await cliente.post(
            url,
            headers={
                "Authorization": f"Bearer {api_token}"
            },
            json={"text": textos_validos}
        )

        resposta.raise_for_status()

    dados = resposta.json()

    if not dados.get("success", False):
        raise RuntimeError(
            f"Erro ao gerar embeddings: {dados.get('errors')}"
        )

    embeddings = dados.get("result", {}).get("data")

    if not isinstance(embeddings, list):
        raise RuntimeError("Resposta de embeddings inválida")

    if len(embeddings) != len(textos):
        raise RuntimeError(
            "Quantidade de embeddings diferente da esperada"
        )

    return embeddings

