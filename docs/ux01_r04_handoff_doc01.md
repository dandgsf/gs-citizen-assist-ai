# UX-01.R04 — Encaminhamento dos resultados para DOC-01

- **Projeto:** Citizen Assist AI — Global Solution FIAP 2026.2
- **Origem:** `test/ux-01-usabilidade` — Draft PR #5
- **Destino da informação:** DOC-01 (relatório técnico final, README e backlog, sob coordenação da equipe)
- **Estado:** síntese preparada para integração; **UX-01.R03 revisada documentalmente; evidências individuais ainda pendentes**
- **Natureza da entrega:** documentação e recomendações, sem alteração de código.

## 1. Evidências de origem

- `docs/ux01_roteiro_usabilidade.md` — execução UX-01.A, com registro de quatro tarefas e tempos individuais;
- `docs/ux01b_validacao_acessibilidade.md` — sete verificações por teclado e oito com VoiceOver;
- `docs/ux01c_teste_participante.md` — execução principal UX-01.C, tarefas e questionário de P01;
- `docs/ux01d_relatorio_usabilidade.md` — síntese, interpretações, prioridades e limitações.

## 2. Resumo para incorporar à seção de usabilidade do relatório final

Em 17/11/2026, o Citizen Assist AI foi avaliado em **duas sessões distintas** (UX-01.A e UX-01.C) com o **mesmo participante anonimizado P01**, sem experiência avançada com terminal. As sessões utilizaram cenários parcialmente diferentes e tiveram seus tempos registrados e analisados separadamente, sem comparação causal entre modos.

Na sessão **UX-01.A**, utilizando o modo `--simples`, as quatro tarefas foram registradas como concluídas sem ajuda, com **09min02s** de tempo acumulado e média de **02min15,5s** por tarefa. A tarefa complementar abordou nota fiscal.

Na sessão principal **UX-01.C**, as **quatro tarefas foram concluídas sem ajuda (4/4; 100%)**, com **08min20s** acumulados e média de **02min05s** por tarefa. Os temas foram taxa de serviço, golpe no Pix, meia-entrada/condições e um caso fora do escopo (aluguel de carro na Islândia). Nas três tarefas em que a identificação da fonte foi avaliada, a fonte foi localizada em **2/3 (66,7%)**. As notas de P01 foram: navegação **4/5**, clareza **4/5**, localização de fontes **3/5**, facilidade geral **4/5**. Foram relatados excesso de informações no menu, textos próximos e dificuldades com caracteres visuais.

A avaliação específica de acessibilidade (UX-01.B), realizada separadamente pelo avaliador, registrou **7/7 verificações por teclado com resultado “Ok”**. Com VoiceOver, **2/8** verificações receberam a classificação “Aprovado” e **6/8** “Aprovado com ressalva”. Esse resultado **não comprova acessibilidade universal**; a revisão UX-01.R03 organizou os registros existentes, mas as dificuldades individuais permanecem sem evidências específicas.

**Tarefa T04:** o observador confirmou retrospectivamente que P01, após a mensagem de limitação de escopo, digitou espontaneamente `1` para consultar os temas. Em reprodução técnica posterior (19/11/2026, commit `593f7c2`), o avaliador confirmou, nos modos normal e `--simples`, a mensagem de limitação, a listagem de cinco temas com `1` e o encerramento com `0`. A reprodução não é uma segunda observação de P01. A mensagem de limitação não indicava explicitamente `1` como caminho de continuidade.

**Limitações:** apenas um participante em duas sessões; observação do VoiceOver separada do participante; versões exatas dos commits dos testes originais não registradas; desempenho e experiência dependem do ambiente e da familiaridade do usuário; nenhuma melhoria de interface foi implementada/revalidada nesta entrega. Não extrapolar os resultados para a população nem afirmar conformidade com normas de acessibilidade.

## 3. Melhorias priorizadas para a equipe

| ID | Prioridade | Recomendação | Fundamentação |
|---|---|---|---|
| UX-M01 | Alta | Melhorar espaçamento, títulos, redução de ruído visual e sinalização de próximo comando | Excesso de informação relatado nas quatro tarefas da UX-01.C |
| UX-M02 | Alta | Tornar comandos e elementos do terminal mais lineares e compreensíveis para leitor de tela | Seis verificações VoiceOver com ressalvas; dificuldades individuais não comprovadas na R03 |
| UX-M03 | Alta | Destacar título, fonte, URL, data e avisos da orientação | Nota 3/5 para fontes e não localização na T02 |
| UX-M04 | Média | Explicar atalhos contextuais e orientar como continuar após mensagens de limite | Observação de atalhos na UX-01.A e reprodução técnica da T04 |

**Estado das melhorias:** propostas; nenhuma implementada ou revalidada por esta frente.

## 4. Encaminhamentos para DOC-01

1. **Relatório final:** incorporar síntese compacta da seção 2, distinguindo as duas sessões, métodos, indicadores, limitações e melhorias. A seção 8 de `docs/relatorio.md` do ZIP inicial era um formulário; verificar a estrutura da versão corrente antes de substituir qualquer trecho.
2. **README:** quando a revisão for aprovada, apontar para `docs/ux01d_relatorio_usabilidade.md` e informar que houve teste com participante, mas que as melhorias de acessibilidade são recomendações, não correções.
3. **Backlog:** manter UX-01 como **Em revisão/Aguardando integração** até aprovação do responsável; não assinalar como concluída por causa apenas deste resumo.
4. **PDF final:** preservar distinção entre resultados observados e limitações, compatibilizando texto e números com o README e com a versão definitiva do código.
5. **Pendências antes do aceite final:** completar R03 se houver evidências, avaliar fluxos afetados pela integração BAS-01/BUS-01 e confirmar a rastreabilidade de versão onde possível. Não inventar informações ausentes.

**Integração Git:** este documento é apenas um encaminhamento de UX-01. Evitar editar `docs/relatorio.md`, `README.md` ou `docs/BACKLOG.md` diretamente na branch UX-01 se outra frente for responsável pela consolidação; deixar a integração para DOC-01 e a revisão do Danilo.
