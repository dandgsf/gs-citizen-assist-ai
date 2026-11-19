# UX-01.C — Teste de usabilidade com participante real

**Projeto:** Citizen Assist AI — Global Solution FIAP 2026  
**Responsável:** Renato Nascimento  
**Branch:** `test/ux-01-usabilidade`  
**Status:** Executado

## 1. Objetivo

Verificar se um participante consegue utilizar a interface textual do Citizen Assist AI para localizar orientações cidadãs, identificar as fontes e compreender limites da resposta, sem receber instruções sobre os comandos antes da execução.

## 2. Preparação do teste

- **Participante:** P01 (não anotar nome nem dados pessoais).
- **Data:** 17/11/2026
- **Branch anotada:** `test/ux-01-usabilidade`. Commit efetivamente executado não registrado.
- **Sistema operacional e terminal:** MacOS Tahoe 26.4 - Terminal
- **Modo efetivamente usado:** não registrado. O roteiro indica `python3 src/sistema.py` como comando sugerido.
- **Observador:** Renato Nascimento
- **Uso de tecnologias assistivas?** Não
- **Participante concordou em realizar o teste?** Sim

Antes de começar, confirme que o programa está aberto no menu inicial e que o terminal está funcionando. Não use informações pessoais reais nas perguntas.

## 3. Instrução inicial ao participante

> “Este é um protótipo acadêmico de orientação cidadã, não um canal oficial. Vou pedir que você faça algumas tarefas usando o programa. Não estou avaliando você, e sim a facilidade de uso do sistema. Tente concluir cada tarefa com as informações apresentadas na tela. Pode pensar em voz alta e dizer o que estiver confuso. Caso precise de ajuda, peça; registrarei isso como uma observação do teste.”

Não explique previamente os comandos `tN`, `sN`, `rN` ou `v`; queremos observar se são compreendidos na interface.

## 4. Tarefas para o participante

Apresente uma tarefa por vez, utilizando apenas a coluna **Enunciado ao participante**. A coluna **Referência interna** é exclusiva do observador.

| ID | Enunciado ao participante | Referência interna para o observador | Critério de sucesso |
|---|---|---|---|
| T01 | “Descubra se a taxa de serviço de 10% em restaurantes é obrigatória. Mostre onde o programa informa a fonte da orientação.” | Registro esperado no projeto: DB10 | Localiza a orientação e identifica a fonte, sem confundir recomendação com obrigação. |
| T02 | “Imagine que alguém sofreu um golpe envolvendo Pix. Encontre uma orientação no programa e diga quais seriam os próximos passos sugeridos.” | Registro esperado no projeto: DB15 | Localiza uma orientação pertinente e explica o próximo passo com base na resposta apresentada. |
| T03 | “Procure informação sobre meia-entrada e descubra como verificar se a pessoa se enquadra nas condições apresentadas.” | Registro esperado no projeto: DB14, opção de verificação `v` | Localiza o tema e utiliza/compreende o fluxo de condições, sem ajuda ou com ajuda registrada. |
| T04 (opcional) | “Pergunte como alugar um carro na Islândia. Se não encontrar uma orientação, tente identificar como continuar a consulta.” | Pergunta intencionalmente fora do escopo; verificar se o sistema recusa responder sem base | Reconhece a ausência de resposta confiável e encontra alternativa de navegação, se oferecida. |

**Nota:** T01–T03 formam o núcleo do roteiro. T04 amplia a análise de limites, sem substituir as três tarefas anteriores.

## 5. Planilha de observação (preencher durante o teste)

Utilize cronômetro para medir o intervalo entre a apresentação da tarefa e a tentativa de conclusão. Registre como “não concluída” quando a tarefa não terminar, mesmo que tenha consumido tempo.

| ID | Conclusão (sem ajuda / com ajuda / não concluiu) | Tempo (s) | Dificuldades observadas | Identificou a fonte? (sim/não/n.a.) |
|---|---|---:|---|---|
| T01 | Sem ajuda | 1:34 | Muita informação no menu | sim |
| T02 | Sem ajuda | 1:56 | Muita informação no menu | não |
| T03 | Sem ajuda | 1:48 | Muita informação no menu | sim |
| T04 (opcional) | Sem ajuda | 3:02 | Muita informação no menu | não aplicável |

Em T02, a tarefa foi registrada como concluída e a fonte ficou sem identificação. Em T04, a ficha registra conclusão sem ajuda, mas não contém o texto da consulta digitada, a saída exibida nem a ação usada para continuar. Essas etapas ficam sem comprovação no registro da sessão.

**Ajuda fornecida pelo observador (quando e qual):**  Nenhuma
____________________________________________________________________

**Mensagens, comandos ou termos que causaram dúvida (trechos exatos, sem dados pessoais):**  Nenhuma
____________________________________________________________________

**Erros, travamentos ou comportamento inesperado:**  Nenhum
____________________________________________________________________

## 6. Perguntas finais ao participante

Peça notas de **1 (muito ruim/difícil)** a **5 (muito bom/fácil)**.

1. Facilidade para encontrar assuntos e navegar: 4/5.
2. Clareza das instruções e mensagens: 4/5.
3. Facilidade para localizar e entender as fontes: 3/5.
4. Facilidade geral de uso: 4/5.

**Pergunta aberta:** “O que você mudaria primeiro para facilitar o uso?”  
**Resposta (sem identificação pessoal):** Melhorar a experiência do usuário, os textos estão muito juntos e alguns carácteres especiais atrapalham a visualização.

## 7. Indicadores e interpretação

- **Taxa de conclusão sem ajuda:** número de tarefas concluídas sem ajuda ÷ número de tarefas executadas × 100.
- **Taxa de conclusão total:** número de tarefas concluídas com ou sem ajuda ÷ número de tarefas executadas × 100.
- **Tempo médio das tarefas:** soma dos tempos medidos ÷ número de tarefas com tempo registrado. Informar quais tarefas entraram no cálculo.
- **Notas subjetivas:** apresentar cada nota e, se pertinente, a média. **Uma única pessoa não permite generalização estatística.**

**Resultados reais:**  
Total de tarefas executadas: 4  
Concluídas sem ajuda: 4  
Concluídas com ajuda: 0  
Não concluídas: 0  
Taxa de conclusão sem ajuda: 100%  
Taxa de conclusão total: 100%  
Tempo médio: 02:05s  

**Interpretação baseada nas observações.** P01 concluiu as quatro tarefas sem ajuda segundo a ficha. O excesso de informação no menu apareceu em todas as tarefas. A fonte foi identificada em duas das três tarefas aplicáveis.

## 8. Registro de acessibilidade já sinalizado (UX-01.B)

**Observação relatada anteriormente:** dificuldade ao utilizar VoiceOver; a apresentação textual precisa ser avaliada e possivelmente adaptada para leitura por tecnologia assistiva.

**Situação:** questão aberta; não afirmar que a interface é compatível com leitor de tela até concluir a avaliação.

**Detalhes a completar, se possível:** versão do macOS, terminal utilizado, modo normal/`--simples`, exemplos concretos de texto anunciado incorretamente e impacto sobre a navegação.

## 9. Melhorias candidatas (hipóteses, não resultados do teste)

1. Revisar separadores, rótulos e instruções para leitura linear com VoiceOver, testando o modo simples.
2. Tornar os comandos de navegação e as fontes mais explícitos e fáceis de identificar.

Após o teste, manter apenas melhorias sustentadas pelas evidências observadas e justificar a prioridade.

## 10. Limitações do procedimento

- Amostra mínima de um participante, sem representatividade estatística.
- Experiência pode variar conforme familiaridade com terminal e computador.
- Alterações no código após o teste podem exigir repetição do procedimento.
- Este teste não substitui auditoria profissional de acessibilidade nem verifica a exatidão jurídica das fontes.

## 11. Próximos passos

- Complementar T04 se houver anotações da sessão. Repetir a tarefa se a equipe precisar verificar o caminho percorrido.
- Salvar evidências no repositório sem dados pessoais.
- Consolidar UX-01.B + UX-01.C em UX-01.D e propor pelo menos duas melhorias fundamentadas.
- Reexecutar tarefas afetadas por correções relevantes antes de concluir a etapa.
