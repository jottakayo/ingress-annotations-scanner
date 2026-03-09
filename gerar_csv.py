import csv


def gerar_csv(registros, caminho_arquivo_saida, incluir_compatibilidade_traefik=False):
    with open(caminho_arquivo_saida, "w", newline="", encoding="utf-8") as arquivo:
        escritor_csv = csv.writer(arquivo)
        cabecalho = [
            "Namespace",
            "Nome do Ingress",
            "Host",
            "Service",
            "Usa Annotation?",
            "Lista de Annotations"
        ]
        if incluir_compatibilidade_traefik:
            cabecalho.append("Nginx Supported (Traefik)")
            cabecalho.append("Nginx Unsupported (Traefik)")

        escritor_csv.writerow(cabecalho)
        for registro in registros:
            linha = [
                registro["namespace"],
                registro["nome"],
                registro["hosts"],
                registro["services"],
                registro["usa_annotation"],
                registro["annotations"]
            ]
            if incluir_compatibilidade_traefik:
                linha.append(registro.get("nginx_supported_traefik", ""))
                linha.append(registro.get("nginx_unsupported_traefik", ""))
            escritor_csv.writerow(linha)
