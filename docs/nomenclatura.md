# Nomenclatura e tópicos do projeto

Consulta realizada em 12/11/2026 na conta GitHub `dandgsf`, incluindo os 61 repositórios retornados pela listagem autenticada.

## Evidências observadas

| Repositório | Tópicos observados | Convenção relevante |
|---|---|---|
| [gs-mission-control](https://github.com/dandgsf/gs-mission-control) | `fiap`, `global-solution`, `1st-semester` | Prefixo `gs-` seguido do nome do projeto em minúsculas, com hífens |
| [ncas-aurora-siger](https://github.com/dandgsf/ncas-aurora-siger) | `fiap`, `ncas`, `2nd-semester` | Semestre identificado por tópico, sem precisar entrar no nome |
| [sigic-aurora](https://github.com/dandgsf/sigic-aurora) | `fiap`, `1st-semester`, `fase-04-aurora-siger` | Sigla da atividade e identidade do projeto |
| [sicap-aurora-colony](https://github.com/dandgsf/sicap-aurora-colony) | `fiap`, `1st-semester`, `fase-03-aurora-siger` | Nome em minúsculas e palavras separadas por hífens |
| [enterprise-challenge-goodwe](https://github.com/dandgsf/enterprise-challenge-goodwe) | `fiap`, `goodwe`, `2st-semester` | Tipo de atividade e case; o tópico de semestre contém uma inconsistência de grafia |

`gs-mission-control` foi o único nome encontrado contendo `gs`. A busca por `topic:gs` não retornou repositórios; a busca por `topic:global-solution` retornou `gs-mission-control`. Portanto, `global-solution` é o tópico acadêmico observado para GS. Esse repositório usa a branch padrão `main` e não tinha tags Git na consulta. Nenhum conteúdo privado desse projeto foi copiado para esta análise.

## Decisão aplicada

- **Nome adotado nesta etapa:** Citizen Assist AI, conforme o case oficial; identidade própria será definida posteriormente.
- **Pasta e repositório:** `gs-citizen-assist-ai`.
- **Identificação acadêmica:** Global Solution 2026.2, CitizenTech, case Citizen Assist AI, Grupo 9.
- **Tópicos reaproveitados:** `fiap`, `global-solution`, `2nd-semester`.
- **Tópicos específicos adicionados:** `citizentech`, `citizen-assist-ai`, `python`, `knowledge-base`.
- **Branch principal:** `main`.
- **Primeira versão:** tag anotada `v0.1.0`, correspondente ao protótipo inicial e à documentação alinhada ao enunciado.

A decisão segue `gs-<nome-do-projeto>`, usando o nome do case oficial Citizen Assist AI nesta etapa. O semestre fica nos tópicos e no README. Usa-se `2nd-semester`, já presente em outro projeto do segundo semestre, em vez de reproduzir a grafia `2st-semester`. Os tópicos específicos e a versão inicial são decisões deste projeto; não são exigências da FIAP nem um padrão de versionamento comprovado nos projetos anteriores.

## Como reproduzir a consulta

```powershell
gh repo list dandgsf --limit 200 --json name,description,repositoryTopics,visibility,url,defaultBranchRef
gh api search/repositories -f q='user:dandgsf topic:gs' -X GET
gh api search/repositories -f q='user:dandgsf topic:global-solution' -X GET
gh api repos/dandgsf/gs-mission-control/tags
```

Tópicos do GitHub classificam o repositório. A tag Git `v0.1.0` identifica um commit no histórico; são mecanismos diferentes.
