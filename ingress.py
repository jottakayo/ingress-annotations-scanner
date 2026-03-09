from traefik_compatibilidade import PREFIXO_ANNOTATION_NGINX


def filtrar_annotations_por_prefixo(annotations, prefixo):
    annotations_filtradas = []
    if not prefixo:
        for chave in annotations:
            annotations_filtradas.append(chave)
    else:
        for chave in annotations:
            if chave.startswith(prefixo):
                annotations_filtradas.append(chave)
    return sorted(annotations_filtradas)


def coletar_hosts_e_services(spec):
    hosts = set()
    services = set()
    regras = spec.get("rules", [])

    for regra in regras:
        host = regra.get("host")
        if host:
            hosts.add(host)

        paths = regra.get("http", {}).get("paths", [])
        for path in paths:
            service = (
                path.get("backend", {})
                .get("service", {})
                .get("name")
            )
            if service:
                services.add(service)

    return sorted(hosts), sorted(services)


def coletar_annotations_nginx(annotations):
    annotations_nginx = []
    for chave in annotations:
        if chave.startswith(PREFIXO_ANNOTATION_NGINX):
            annotations_nginx.append(chave)
    return sorted(annotations_nginx)


def separar_annotations_nginx_por_compatibilidade(lista_annotations, compatibilidade):
    annotations_suportadas = []
    annotations_nao_suportadas = []

    for annotation in sorted(lista_annotations):
        if annotation in compatibilidade["suportadas"]:
            annotations_suportadas.append(annotation)
        elif annotation in compatibilidade["nao_suportadas"]:
            annotations_nao_suportadas.append(annotation)

    return annotations_suportadas, annotations_nao_suportadas


def processar_ingress(dados, prefix=None, compatibilidade_traefik=None):
    registros = []

    for item_ingress in dados.get("items", []):
        metadata = item_ingress.get("metadata", {})
        spec = item_ingress.get("spec", {})
        namespace = metadata.get("namespace", "")
        nome = metadata.get("name", "")
        annotations = metadata.get("annotations", {})

        annotations_filtradas = filtrar_annotations_por_prefixo(annotations, prefix)
        possui_annotations = "Não"
        if annotations_filtradas:
            possui_annotations = "Sim"
        hosts_ordenados, services_ordenados = coletar_hosts_e_services(spec)

        registro = {
            "namespace": namespace,
            "nome": nome,
            "hosts": "\n".join(hosts_ordenados),
            "services": "\n".join(services_ordenados),
            "usa_annotation": possui_annotations,
            "annotations": "\n".join(annotations_filtradas),
        }

        if compatibilidade_traefik:
            annotations_nginx = coletar_annotations_nginx(annotations)
            suportadas, nao_suportadas = separar_annotations_nginx_por_compatibilidade(
                annotations_nginx,
                compatibilidade_traefik,
            )
            registro["nginx_supported_traefik"] = "\n".join(suportadas)
            registro["nginx_unsupported_traefik"] = "\n".join(nao_suportadas)

        registros.append(registro)
    return registros
