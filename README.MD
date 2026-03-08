# Kubernetes Ingress Annotation Tool

---

## Visão Geral

Ferramenta que gera um relatório CSV com informações do objeto do kind Ingress no cluster k8s, com foco na coleta e análise de **annotations**.

A ferramenta permite:

* Listar todos os Ingress do cluster ou filtrar por namespaces específicos
* Identificar e filtrar annotations por prefixo (flag `--annotation-prefix`)
* Gerar um relatório estruturado em CSV

Transforma json bruto da saida do comando:

```yaml
kubectl get ingress -o json
``` 
Em informação estruturada para análise em arquivo CSV.

---

## O que a ferramenta faz?

A ferramenta realiza um levantamento dos Ingress no Kubernetes e transforma essas informações em um relatório em .CSV.
Faz uma consulta no cluster via kubectl, trata os resultados (seja de um namespace específico ou de vários), processa cada Ingress individualmente e extrai informações como namespace, nome, hosts configurados, services vinculados e todas as annotations presentes.
Além disso, permite aplicar filtros por prefixo nas annotations (utilizando o metodo startswith da classe str).
Ao final, o processamento é convertido em um arquivo CSV.

---

## Pré-requisitos

* Python 3.14+
* `kubectl` instalado
* Acesso ao cluster
* Permissão para listar recursos Ingress

---

### Baixar o binário

A forma recomendada de uso é através do **binário já compilado**, disponível nas Releases do projeto.

Acesse:

https://github.com/jottakayo/ingress-annotations-scanner/releases

Baixe o binário e após baixar, conceda permissão de execução:

```bash
chmod +x ingress-annotations-scanner-*
```

---

## Configurar acesso ao cluster

A ferramenta depende do `kubectl`, que usa o arquivo **kubeconfig** para acessar o cluster.

Se necessário, exporte o kubeconfig do cluster:

```bash
export KUBECONFIG=/caminho/do/kubeconfig
```

Veja o contexto ativo:

```bash
kubectl config current-context
```

Isso garante que você está apontando para o cluster que quer antes da execução.

---

## Validar permissões

Antes de executar o script, valide se possui permissão para listar Ingress:

```bash
kubectl auth can-i get ingress -A
```

Resultado esperado:

* `yes` → Você pode continuar
* `no` → Solicite permissão antes de prosseguir

Também pode testar diretamente:

```bash
kubectl get ingress -A
```

Se esse comando funcionar, o script também funcionará.

---

## Visualizar opções disponíveis

A ferramenta possui argumentos configuráveis. Para visualizar todas as opções:

```bash
./ingress-annotations-scanner-* -h
```

ou

```bash
./ingress-annotations-scanner-* --help
```

Exibe todos os argumentos suportados.

---

## Executando a ferramenta

### Buscar em namespaces específicos

Use o argumento `--namespace` seguido da lista desejada:

```bash
./ingress-annotations-scanner-* --namespace ns1 ns2 ns3
```

---

### Buscar em todos os namespaces

Use o argumento `--all`:

```bash
./ingress-annotations-scanner-* --all
```
---

### Filtrar por annotations especificas

Use o argumento `--annotation-prefix`:

```bash
./ingress-annotations-scanner-* --annotation-prefix nginx
```

---

## Resultado da Execução

Após a execução, será gerado um arquivo CSV contendo:

* Namespace
* Nome do Ingress
* Hosts configurados
* Services vinculados
* Indicação de uso de annotations
* Lista de annotations encontradas

### Saída

O script gera um arquivo CSV(nome padrão: ingress_report.csv) com colunas:

| Namespace | Nome do Ingress | Hosts | Service | Usa Annotation? | Lista de Annotations |
| --------- | ---- | ----- | -------- | -------------- | ----------- |

>Esse arquivo pode ser aberto no Excel
