# Uso de Inteligência Artificial no projeto

Este documento registra o uso de IA no desenvolvimento, conforme os requisitos acadêmicos.

## Ferramentas e participação

| Ferramenta | Uso declarado |
|---|---|
| Claude (Anthropic), modelo Claude Opus 5.5 pelo app Claude | Apoio inicial declarado por Danilo Fernandes, no material recebido |
| Codex (OpenAI) | Apoio à documentação, organização do repositório, validação local e revisão da apresentação |

O registro de uso do Claude foi herdado do material inicial; não constitui verificação independente do modelo ou das pesquisas realizadas. Os integrantes do projeto estão identificados no [README](../README.md).

## Atividades apoiadas por IA

- Exploração de ideias e escolha do recorte de direitos do consumidor.
- Pesquisa inicial de referências e rascunho da base de conhecimento.
- Rascunho de código, testes, prompts, relatório e demais documentos.
- Revisão do README e consolidação dos requisitos acadêmicos na [proposta do projeto](projeto.md).
- Remoção de emojis da interface e do gerador de resultados, com preservação dos algoritmos e da base.

A pesquisa inicial não substitui a revisão humana contra as fontes oficiais. As datas cadastradas na base não comprovam que essa revisão foi concluída.

## Uso em funcionamento

O programa não chama modelos de linguagem para responder. As orientações são recuperadas da base, com referência e data cadastrada de verificação.

O Modelo B documenta uma possível integração futura, ancorada no registro recuperado. O gerador de prompts e o validador JSON existem separadamente; conferir formato, fonte e data não comprova a fidelidade do conteúdo à fonte.

## Responsabilidade humana e limites

A equipe é responsável por revisar fontes e linguagem, avaliar o sistema com usuários e conferir os resultados dos testes. A revisão humana integral das fontes permanece necessária; o experimento IA-01 está registrado abaixo, com ressalvas. A situação do teste de usabilidade é documentada separadamente.

A [documentação de prompts](prompts.md) contém o protocolo de comparação; o [relatório técnico](relatorio.md) contém o formulário de usabilidade. Resultados não executados não devem ser apresentados como evidência.

<!-- IA01_AUDITORIA_2026_INICIO -->
## IA-01 — Experimento real de comparação de prompts

- **Data e modelo informados pelo manifesto:** 2026-11-19; GPT-6, ChatGPT. Conversas independentes declaradas, não verificadas externamente.
- **Procedimento:** cinco perguntas iguais nos modelos A (direto) e B (com registro), 10 respostas originais em `data/ia01/respostas/`.
- **Achados:** B produziu 5/5 JSON válidos e respeitou o limite de 80 palavras em 5/5; recusou apropriadamente 2/2 casos sem registro. A respondeu as cinco perguntas, inclusive duas fora da cobertura. Contudo, T01_B e T03_B têm arquivos de prompt com data alterada, e T02_B devolveu data diferente do próprio prompt. **Não aprovar automaticamente as três saídas B com `status=ok` contra a base original.**
- **Limite do validador:** `validar_saida_ia()` verifica JSON, `status`, fonte e data; não comprova fidelidade semântica, atualidade jurídica, adequação da busca, completude dos campos ou o limite de 80 palavras. `sem_informacao` é rejeitado deliberadamente na saída final, levando ao fallback.
- **Evidências, comparação e fontes oficiais:** [Relatório detalhado IA-01](ia01_resultados.md). Estado: **execução registrada, revisão do protocolo pendente** em T01_B e T03_B.
<!-- IA01_AUDITORIA_2026_FIM -->

<!-- IA01_PR2026_INICIO -->
## IA-01 — Comparação experimental real de prompts

- **Condições informadas:** 19/11/2026; ChatGPT; modelo GPT-6; 10 conversas novas e independentes declaradas. O ZIP comprova os textos capturados, não comprova externamente a configuração nem o isolamento das conversas.
- **Procedimento:** cinco perguntas, prompt A (livre) e prompt B (ancorado no registro), com dez saídas originais preservadas em `data/ia01/respostas/`.
- **Observações:** B produziu 5/5 JSONs válidos, 5/5 textos `resposta_simples` de até 80 palavras e 2/2 abstenções esperadas sem registro. A respondeu a 5/5 perguntas, inclusive duas sem cobertura na base. O operador declarou editar manualmente as datas em T01_B/T03_B; em T02_B a IA mudou a data recebida.
- **Limite de validação:** `validar_saida_ia()` verifica JSON, `status`, `fonte` e `data_verificacao`; **não** confere adequação do registro recuperado, fidelidade semântica, veracidade jurídica, completude de todos os campos ou o limite de palavras. `sem_informacao` é rejeitado para uso da saída gerada, acionando o retorno ao texto da base (fallback).
- **Integridade:** data do teste e `data_verificacao` da fonte são conceitos distintos. A edição manual de prompts é declarada, e a atualização da base só pode ser reivindicada com conferência efetiva das normas. A saída T02_B falha ao copiar a data do prompt individual. Nenhuma evidência foi corrigida retroativamente.
- **Evidências:** [comparação, análise e fontes](ia01_resultados.md) · [protocolo e tabela preenchida](prompts.md).
<!-- IA01_PR2026_FIM -->
