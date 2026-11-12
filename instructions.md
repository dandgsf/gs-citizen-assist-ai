# Global Solution — 2º Semestre de 2026 · CitizenTech: Citizen Assist AI

## Identificação

| Campo | Valor |
|---|---|
| Avaliação | Global Solution - 2º Semestre |
| Edição | 2º semestre de 2026 |
| Tema geral | CitizenTech |
| Case oficial | Citizen Assist AI |
| Fase | 7 |
| Tipo | Atividade em grupo (1 a 5 pessoas) |
| Modalidade | Remota |
| Peso | 14 pontos da nota anual (GS2), segundo o guia acadêmico |
| Grupo | Grupo 9 (Danilo Gustavo da Silva Fernandes) |
| Status no portal | ENTREGA PENDENTE / AVALIAÇÃO PENDENTE (consultado em 11/11/2026) |

## Fontes

- [Enunciado oficial no FIAP ON](https://on.fiap.com.br/mod/assign/view.php?id=684386)
- [Página de divulgação CitizenTech](https://experience.fiap.com.br/global-solution-citizen-tech) (não substitui o enunciado)
- [Modelo de repositório da coordenação](https://github.com/equipe1ccon/FIAP-PORTFOLIO-1CCON/tree/master)
- Guia acadêmico: `2026_guia_academico_on_cursos_novos.pdf`

## Prazos

- **Período de aplicação:** 04/11/2026 a 19/11/2026
- **Kick-off:** LIVE online em 04/11/2026, às 19h
- **Entrega:** quinta-feira, 19/11/2026, às 23h59 (a página não informa fuso horário)

## Desafio

> "A Global Solution – 2º Semestre de 2026 propõe o desafio CitizenTech: desenvolver tecnologias orientadas às necessidades reais das pessoas. O case Citizen Assist AI convida as equipes a construir um assistente digital introdutório que facilite o acesso a informações úteis sobre serviços, documentos, direitos e orientações comunitárias."

O objetivo é construir um protótipo funcional que organize informações verificadas sobre serviços, documentos, direitos e orientações comunitárias. A página de divulgação pede que o projeto identifique os ODS da ONU com que se conecta (2, 3, 4, 9, 10, 11 e 13), mas o case avaliativo é especificamente o Citizen Assist AI, não um tema aberto.

### Cuidados obrigatórios

- Não pedir dados pessoais desnecessários.
- Não se apresentar como canal oficial do governo.
- Avisar quando não houver informação suficiente, em vez de inventar a resposta.
- Tratar entrada vazia ou inválida.

## Requisitos funcionais

- Receber uma pergunta em texto livre ou uma escolha de menu.
- Consultar uma base de conhecimento em JSON, TXT ou CSV.
- Responder citando a fonte.
- Avisar quando a informação for insuficiente.
- Tratar entrada vazia, opção inexistente e dúvidas não previstas.
- Permitir editar a base sem alterar o código.
- Validar campos e tratar arquivo ausente ou vazio.
- Listar temas e permitir busca por pergunta ou assunto.
- Exibir a resposta, a fonte e o aviso de limitação.

## Requisitos técnicos

- **Linguagem:** Python
- **Execução:** `python src/sistema.py`
- **Interface:** textual é suficiente; GUI ou web são opcionais.
- **Não obrigatório:** APIs pagas, LangChain e n8n.

### Conteúdo das fases

| Fases | Papel | Conteúdos |
|---|---|---|
| 1 a 3 | Apoio | Python, algoritmos, listas e dicionários |
| 4 | Foco | Estruturas de dados; leitura e organização de dados; listas, tuplas e dicionários; grafos e redes; Dijkstra; regressão; limites e derivadas |
| 5 | Foco | Arquivos TXT e JSON; prompts; cadeias de prompts; saídas estruturadas; lógica booleana e De Morgan |
| 6 | Foco | Métricas de desempenho; chatbots e assistentes; busca e comparação de algoritmos; mapa de Karnaugh |

> A Fase 7 também é a fase Aurora/Marte (14/10 a 27/11/2026), mas o enunciado da Global Solution não trata de Marte.

### Estruturas e busca

- Usar listas e dicionários.
- Ler a base com Python.
- Buscar por pergunta ou assunto e explicar a estratégia, inclusive quando houver várias correspondências.
- Organizar os temas em hierarquia ou grafo simples.
- Permitir navegação entre pelo menos 3 assuntos relacionados.

### Prompts

- Documentar e comparar pelo menos 2 modelos de prompt.

## Conteúdo mínimo da base

- Pelo menos **15 registros** em pelo menos **3 temas**.
- Cada registro deve ter estes campos:
  - identificador
  - tema
  - pergunta ou palavras-chave
  - orientação resumida
  - referência
  - data de verificação

## Testes e indicadores

- Pelo menos **12 perguntas de teste**, incluindo perguntas diretas, reformulações e consultas fora do tema.
- Pelo menos **3 situações-limite**:
  - entrada vazia
  - consulta ambígua
  - pergunta sem resposta confiável
- Registro de cada teste com resposta esperada, resposta obtida, acerto ou erro e tempo da consulta.
- Indicadores: **taxa de acerto** e **tempo médio de consulta**.
- Teste de usabilidade com pelo menos **1 usuário**.
- Pelo menos **2 melhorias ou limitações** identificadas.

## Entrega no portal

Envie, pela [página da atividade](https://on.fiap.com.br/mod/assign/view.php?id=684386), **um único arquivo `.txt`** com apenas estes dois links:

1. Link direto do repositório GitHub público da equipe.
2. Link do vídeo de apresentação no YouTube, publicado como **Não Listado**.

> "Envie um arquivo .TXT pela plataforma FIAP ON contendo apenas os dois links abaixo: Link direto do repositório GitHub público da equipe; Link do vídeo de apresentação publicado no YouTube como “Não Listado”."

## Repositório

O repositório deve seguir o [modelo da coordenação](https://github.com/equipe1ccon/FIAP-PORTFOLIO-1CCON/tree/master).

| Arquivo | Conteúdo |
|---|---|
| `README.md` | Documentação principal |
| `src/sistema.py` | Programa principal, executado com `python src/sistema.py` |
| `data/base.json` ou `data/base.txt` | Base com pelo menos 15 orientações |
| `docs/relatorio.pdf` | Relatório de 4 a 8 páginas: problema, público, arquitetura, fontes, estratégias de prompts, resultados de testes, indicadores, limitações e impacto social |
| `docs/link_video.txt` | Link do vídeo de apresentação |
| `docs/uso_ia.md` | Obrigatório quando houver uso de IA |

### O README deve conter

- Nome da equipe e RMs
- Problema, público e temas
- Desenho da base, estruturas e estratégia de busca
- Regras de resposta, prompts e limitações
- Plano de testes e resultados
- Como executar
- Exemplos de perguntas e respostas
- Cuidados com clareza, acessibilidade, privacidade e com não se apresentar como informação oficial
- Link do vídeo
- Conclusões

## Checklist de entrega

- [ ] Repositório público
- [ ] `.txt` com os dois links corretos
- [ ] Vídeo no YouTube como Não Listado
- [ ] Código sem erros
- [ ] Perguntas e fontes documentadas
- [ ] Estratégia justificada
- [ ] Indicadores apresentados
- [ ] Entradas inválidas tratadas
- [ ] Avisos de limitação
- [ ] Uso de IA documentado, quando aplicável

## Observações

- A página da atividade não mostra critérios de avaliação, pesos nem política de atraso. Ela diz que prevalecem os prazos e links oficiais divulgados pela instituição, e que abertura e plantão de dúvidas serão comunicados pelos canais oficiais da FIAP.
- A página não tem PDF oficial anexado. As Tabelas 1 (conteúdo das fases) e 2 (arquivos do repositório) aparecem só como imagens.
- A página de divulgação apresenta o tema CitizenTech e algumas inspirações, mas o case avaliado é o Citizen Assist AI.
- A página antiga `https://www.fiap.com.br/graduacao/global-solution/` ainda trata da edição anterior (Space Connect) e não deve ser usada como enunciado desta edição.