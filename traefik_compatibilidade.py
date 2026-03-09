from json import load

ARQUIVO_BASELINE_PADRAO = "data/traefik_nginx_annotations.json"
PREFIXO_ANNOTATION_NGINX = "nginx.ingress.kubernetes.io/"


def carregar_compatibilidade_traefik(caminho_baseline=ARQUIVO_BASELINE_PADRAO):
    try:
        with open(caminho_baseline, "r", encoding="utf-8") as arquivo:
            dados_baseline = load(arquivo)
    except Exception as e:
        raise RuntimeError(f"Erro ao ler baseline local: {e}")

    lista_suportadas = []
    if "suportadas" in dados_baseline:
        lista_suportadas = dados_baseline["suportadas"]
    elif "supported" in dados_baseline:
        lista_suportadas = dados_baseline["supported"]

    lista_nao_suportadas = []
    if "nao_suportadas" in dados_baseline:
        lista_nao_suportadas = dados_baseline["nao_suportadas"]
    elif "unsupported" in dados_baseline:
        lista_nao_suportadas = dados_baseline["unsupported"]
   
    annotations_suportadas = set(lista_suportadas)
    annotations_nao_suportadas = set(lista_nao_suportadas)

    return {
        "suportadas": annotations_suportadas,
        "nao_suportadas": annotations_nao_suportadas,
        "source": "local-baseline",
    }
