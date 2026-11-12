# Uso de Inteligência Artificial no projeto

Este documento é obrigatório quando há uso de IA (enunciado da Global Solution, Tabela 2).

## Ferramenta usada

| Item | Detalhe |
|---|---|
| Ferramenta | Claude (Anthropic), modelo Claude Opus 5.5, pelo app Claude |
| Período | 11/11/2026 a 19/11/2026 |
| Quem usou | Danilo Gustavo da Silva Fernandes (Grupo 9) |

## Em que a IA ajudou

1. **Escolha do problema.** Brainstorm de ideias dentro do case Citizen Assist AI. A escolha final (direitos do consumidor no dia a dia, para todas as idades) foi do integrante.
2. **Pesquisa e verificação das fontes.** Busca na web das normas usadas em cada registro, conferida em 11/11/2026. Exemplo de achado: a Resolução ANAC 813/2026, em vigor desde 26/10/2026, mudou a assistência em atrasos de voo. Isso foi incorporado ao registro DB22.
3. **Rascunho da base de conhecimento** (`data/base.json`), em linguagem simples.
4. **Rascunho do código** (`src/`): busca, validação, condições e interface textual.
5. **Plano de testes** e script de avaliação (`src/avaliar.py`).
6. **Rascunho da documentação** (README, prompts, relatório).

## O que NÃO foi delegado à IA

- **Decisão sobre o conteúdo jurídico.** Cada registro deve ser conferido por uma pessoa contra a fonte oficial (checklist abaixo).
- **Teste de usabilidade com usuário real.** É feito pessoalmente, e os resultados são registrados no relatório.
- **Execução da comparação de prompts** (`docs/prompts.md`). Os resultados vêm de execução real, com modelo e data informados.
- **Gravação do vídeo.**

## Como o sistema usa (ou não usa) IA em funcionamento

O programa entregue **não chama nenhuma IA** para responder: a resposta sai sempre da base, com fonte e data de verificação. A IA generativa aparece apenas como uma camada opcional e documentada (Modelo B em `docs/prompts.md`). Essa camada tem uma validação automática (`validar_saida_ia` em `src/prompts.py`) que descarta qualquer saída com fonte ou data diferente das do registro.

## Checklist de revisão humana

- [ ] Abri o link de cada um dos 23 registros e confirmei que a norma diz o que o registro afirma
- [ ] Revisei a linguagem de todas as respostas (clareza e tom)
- [ ] Rodei `python src/sistema.py` e `python src/avaliar.py` sem erros
- [ ] Fiz o teste de usabilidade e registrei os resultados no relatório
- [ ] Executei a comparação de prompts e preenchi a tabela em `docs/prompts.md`

## Atualização de documentação e versionamento — 12/11/2026

Codex (OpenAI) foi utilizado para consultar nomes e tópicos dos repositórios FIAP do integrante, incorporar o enunciado fornecido sem alterações em `instructions.md`, ajustar o README ao estado dos arquivos, documentar a nomenclatura `gs-citizen-assist-ai` e preparar o versionamento inicial. O RM570057 foi recuperado do README do projeto FIAP anterior do mesmo integrante.

Foram executados o avaliador existente (`python src/avaliar.py`) e uma consulta pela interface textual. Os indicadores foram reproduzidos, incluindo o erro conhecido V15. O código e o conteúdo jurídico da base foram preservados. Esta sessão não realizou revisão jurídica das fontes, teste com usuário, experimento com modelos de prompt nem submissão acadêmica. O histórico de ferramentas declarado nas seções anteriores foi herdado do material inicial.
