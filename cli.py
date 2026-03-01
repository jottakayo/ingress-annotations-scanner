import argparse 

def parse_args(): 
    parser = argparse.ArgumentParser( 
        description=(
            "Gera um relatório CSV com informações do objeto do kind Ingress do Kubernetes, "
            "incluindo nome, namespace, hosts, services e annotations. "
            "Permite filtrar por namespace e por prefixo de annotation."
        )
    )
    parser.add_argument( 
        "--namespace", 
        help=(
            "Namespace específico ou lista separada por vírgula "
            "(ex: prod,dev). Ignorado se --all for utilizado."
        )
    ) 
    parser.add_argument(
        "--all",
        action="store_true", 
        help="Consulta Ingress em todos os namespaces do cluster."
    )

    parser.add_argument(
        "--annotation-prefix", 
        help=(
            "Filtra apenas annotations cujo nome começa com o prefixo informado"
            "(Usado metodo startswith para filtrar)."
        )
    )
    parser.add_argument(
        "--output-file",
        default="ingress_report.csv", 
        help=(
            "Nome do arquivo CSV de saída (padrão: ingress_report.csv)."
        )
    )
    return parser.parse_args()