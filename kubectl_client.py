from subprocess import run, CalledProcessError
from json import loads

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