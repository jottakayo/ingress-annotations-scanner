from sys import exit
from cli import parse_args
from kubectl_client import coletar_dados, ler_dados_de_arquivo
from ingress import processar_ingress
from gerar_csv import gerar_csv
from traefik_compatibilidade import carregar_compatibilidade_traefik


def main():
    try:
        args = parse_args()
        if args.input_file and args.all:
            raise ValueError("Use --input-file OU --all, não ambos.")
        if args.input_file and args.namespace:
            raise ValueError("Use --input-file OU --namespace, não ambos.")
        if not args.input_file and not args.all and not args.namespace:
            raise ValueError("Informe --input-file ou --all ou --namespace.")
        if args.all and args.namespace:
            raise ValueError("Use apenas --all OU --namespace.")

        dados = {}
        if args.input_file:
            dados = ler_dados_de_arquivo(args.input_file)
        else:
            if args.all:
                dados = coletar_dados(all_namespaces=True)
            else:
                namespaces = args.namespace.split(",")
                dados = coletar_dados(namespaces=namespaces)

        compatibilidade_traefik = None
        if args.traefik_nginx_compat:
            compatibilidade_traefik = carregar_compatibilidade_traefik()
            print(f"Compatibilidade Traefik: fonte={compatibilidade_traefik['source']}")

        incluir_compatibilidade_traefik = False
        if compatibilidade_traefik:
            incluir_compatibilidade_traefik = True

        registros = processar_ingress(
            dados,
            prefix=args.annotation_prefix,
            compatibilidade_traefik=compatibilidade_traefik,
        )
        gerar_csv(
            registros,
            args.output_file,
            incluir_compatibilidade_traefik=incluir_compatibilidade_traefik,
        )
        print(f"CSV gerado: {args.output_file}")
    except Exception as e:
        print(f"Erro: {e}")
        exit(1)


if __name__ == "__main__":
    main()
