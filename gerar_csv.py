import csv

def gerar_csv(registros, output_file): 
    
    with open(output_file, "w", newline="") as arquivo: 
        writer = csv.writer(arquivo)
        writer.writerow([ 
            "Namespace",
            "Nome do Ingress",
            "Host",
            "Service",
            "Usa Annotation?",
            "Lista de Annotations"
        ]) 
        for r in registros:
            writer.writerow([ 
                r["namespace"], 
                r["nome"],
                r["hosts"],
                r["services"],
                r["usa_annotation"],
                r["annotations"]
            ])
            