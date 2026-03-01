from sys import exit 
from cli import parse_args 
from kubectl_client import coletar_dados 
from ingress import processar_ingress 
from gerar_csv import gerar_csv 

def main():
    try: 
        args = parse_args() 
        if args.namespace and args.all: 
            raise ValueError("Use apenas --all OU --namespace") 
        if not args.namespace and not args.all:
            raise ValueError("Você deve informar --all ou --namespace") 
        if args.all:
            dados = coletar_dados(all_namespaces=True) 
        else:
            namespaces = args.namespace.split(",")
            dados = coletar_dados(namespaces=namespaces)
        registros = processar_ingress( 
            dados,
            prefix=args.annotation_prefix
        )

        gerar_csv(registros, args.output_file)
        print(f"CSV gerado: {args.output_file}")
    except Exception as e: 
        print(f"Erro: {e}")
        exit(1)
if __name__ == "__main__": 
    main()