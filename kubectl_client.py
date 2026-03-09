from subprocess import CalledProcessError, run
from json import load, loads


def executar_kubectl(namespace=None, all_namespaces=False):
    comando = ["kubectl", "get", "ingress"]

    if all_namespaces:
        comando.append("-A")
    elif namespace:
        comando.extend(["-n", namespace])
    else:
        raise ValueError("Você deve informar --all ou --namespace")
        
    comando.extend(["-o", "json"])
    try:  
        resultado = run(
            comando,
            capture_output=True,
            text=True,
            check=True
        )
    except CalledProcessError as e:
        raise RuntimeError(f"Erro ao executar kubectl:\n{e.stderr}")
    return loads(resultado.stdout)

def coletar_dados(namespaces=None, all_namespaces=False):
    dados_finais = {"items": []}

    if all_namespaces:
        return executar_kubectl(all_namespaces=True)

    for ns in namespaces:
        resultado = executar_kubectl(namespace=ns.strip())
        dados_finais["items"].extend(resultado.get("items", []))

    return dados_finais

def ler_dados_de_arquivo(caminho_arquivo_entrada):
    try:
        with open(caminho_arquivo_entrada, "r", encoding="utf-8") as arquivo:
            dados = load(arquivo)
    except Exception as e:
        raise RuntimeError(f"Erro ao ler JSON de entrada: {e}")

    eh_dicionario = isinstance(dados, dict)
    tem_chave_items = False
    if eh_dicionario:
        tem_chave_items = "items" in dados

    if not eh_dicionario or not tem_chave_items:
        raise RuntimeError("JSON inválido: esperado objeto com chave 'items'.")

    return dados
