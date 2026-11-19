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
- **Branch utilizada:** `test/ux-01-usabilidade`
- **Commit SHA da sessão original:** não registrado
- **Sistema operacional e terminal:** MacOS Tahoe 26.4 - Terminal
- **Modo de execução:** `python3 src/sistema.py` (modo normal).
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

| ID | Conclusão (sem ajuda / com ajuda / não concluiu) | Tempo (mm:ss) | Dificuldades observadas | Identificou a fonte? (sim/não/n.a.) |
|---|---|---:|---|---|
| T01 | Sem ajuda | 1:34 | Muita informação no menu | sim |
| T02 | Sem ajuda | 1:56 | Muita informação no menu | não |
| T03 | Sem ajuda | 1:48 | Muita informação no menu | sim |
| T04 (opcional) | Sem ajuda | 3:02 | Muita informação no menu | não aplicável |

**Ajuda fornecida pelo observador (quando e qual):**  Nenhuma
____________________________________________________________________

**Mensagens, comandos ou termos que causaram dúvida (trechos exatos, sem dados pessoais):**  Nenhuma
____________________________________________________________________

**Erros, travamentos ou comportamento inesperado:**  Nenhum
____________________________________________________________________

### Evidência complementar — T04

#### Teste original com participante P01

- Data: 17/11/2026.
- Pergunta: "Como alugar um carro na Islândia?"
- Tempo registrado: 03:02.
- Resultado registrado: concluído sem ajuda.
- Dificuldade observada: excesso de informações no menu.
- Ajuda fornecida: nenhuma.

**Complementação retrospectiva do teste original — T04**

No teste realizado em 17/11/2026, o participante P01
recebeu a mensagem de limitação de escopo e, sem
intervenção do avaliador, digitou o comando `1`
para consultar os temas disponíveis.

A tarefa foi concluída sem ajuda, em 03:02.

Essa informação foi confirmada posteriormente pelo
observador e complementa o registro original.
Não corresponde a uma nova execução com P01.

#### Reproduções técnicas posteriores

- Data: 19/11/2026.
- Commit: `593f7c2`.
- Responsável: avaliador.
- Modos: normal e `--simples`.

Em ambos os modos:

1. A pergunta sobre aluguel de carro na Islândia
   recebeu uma mensagem de limitação de escopo.
2. Nenhuma orientação específica ou fonte foi inventada.
3. O comando `1` apresentou os cinco temas disponíveis.
4. O comando `0` encerrou a aplicação normalmente.

A mensagem de limitação não indicou explicitamente
o comando `1` como alternativa de continuidade.

As reproduções técnicas confirmam o comportamento
do sistema no commit `593f7c2`, mas não constituem
registro automático da sessão original.

A utilização espontânea do comando `1` pelo
participante P01 foi confirmada retrospectivamente
pelo observador, conforme registrado acima.


**Mensagem registrada nas reproduções técnicas:**

> (i) Por enquanto eu só cubro situações de consumo
> do dia a dia (compras, lojas, bares, bancos e Pix,
> contas de luz e telefone, viagens). Para questões
> de trabalho, família, previdência, saúde ou crimes,
> procure a Defensoria Pública do seu estado ou um
> advogado. Em emergência, ligue 190.

Após essa mensagem, o comando `1` apresentou os
cinco temas disponíveis:

- t1 — Mercado e lojas
- t2 — Compras pela internet
- t3 — Bares, restaurantes e lazer
- t4 — Bancos, contas e telefone
- t5 — Viagens e transporte

Essas saídas foram registradas na reprodução
técnica de 19/11/2026, não na sessão original
do participante P01.


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
Tempo médio: 02:05 (125 segundos)

**Interpretação baseada nas observações:**

O participante P01 concluiu as quatro tarefas sem ajuda,
com tempo médio de 02:05. Apesar do êxito, relatou
dificuldade com o excesso de informações no menu,
o espaçamento dos textos e alguns caracteres especiais.

A localização das fontes mostrou-se uma oportunidade
de melhoria, com avaliação de 3/5. Na T02, o participante
não identificou a fonte, embora tenha concluído o
objetivo principal da tarefa.

Na T04, reconheceu a limitação de escopo e utilizou
espontaneamente o comando `1` para continuar
navegando, conforme confirmação posterior do observador.

Esses resultados indicam que os fluxos avaliados
foram utilizáveis pelo participante, mas não permitem
generalizar a experiência para outros usuários.
____________________________________________________________________

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

- Manter as evidências de usabilidade no repositório,
  sem dados pessoais do participante.
- Complementar as evidências de acessibilidade
  previstas na revisão UX-01.R03.
- Encaminhar os resultados consolidados à DOC-01,
  conforme a revisão UX-01.R04.
- Reexecutar as tarefas afetadas caso alterações
  relevantes sejam realizadas na interface.
- Submeter a documentação à revisão do responsável
  pela integração antes do merge.