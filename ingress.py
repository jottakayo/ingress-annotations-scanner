def processar_ingress(dados, prefix=None):
    registros = [] 

    for ingress in dados.get("items", []):
        metadata = ingress.get("metadata", {})
        spec = ingress.get("spec", {})
        namespace = metadata.get("namespace", "")
        nome = metadata.get("name", "")
        annotations = metadata.get("annotations", {})
        filtradas = []
        
        for chave in annotations: 
            if prefix:
                if chave.startswith(prefix):
                    filtradas.append(chave)
            else:
                filtradas.append(chave)

        if filtradas: 
          possui_annotations = "Sim"
        else:
          possui_annotations = "Não"
        hosts = set()
        services = set()
        rules = spec.get("rules", [])

        for rule in rules:
            host = rule.get("host")
            if host:
                hosts.add(host)
            paths = rule.get("http", {}).get("paths", [])
            for path in paths:
                service = ( 
                    path.get("backend", {})
                        .get("service", {})
                        .get("name")
                )
                if service:
                    services.add(service)

        registros.append({
            "namespace": namespace, 
            "nome": nome,
            "hosts": "\n".join(sorted(hosts)), 
            "services": "\n".join(sorted(services)),
            "usa_annotation": possui_annotations,
            "annotations": "\n".join(sorted(filtradas))
        })
    return registros 