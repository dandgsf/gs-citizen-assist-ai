# UX-01.A — Roteiro de avaliação de usabilidade do Citizen Assist AI

**Projeto:** FIAP Global Solution 2026.2 — Citizen Assist AI  
**Responsável:** Renato Nascimento  
**Branch de trabalho:** `test/ux-01-usabilidade`  
**Estado:** roteiro preparado; teste com participante **ainda não executado**  
**Base deste roteiro:** `docs/BACKLOG.md` (UX-01) e seção 8 de `docs/relatorio.md`, versão do ZIP inicial disponibilizado pela equipe. Atualizar se o PR pendente modificar os fluxos.

## 1. Objetivo e escopo

Observar se uma pessoa consegue usar a interface textual para localizar uma orientação de consumo, identificar a fonte, utilizar a verificação de condições e entender os limites da resposta. Este roteiro também prepara os campos de observação para navegação por teclado e leitor de tela, que serão executados e registrados na UX-01.B.

O teste de usabilidade com pelo menos **uma pessoa real**, sem identificá-la, é exigência do backlog. Este arquivo não representa evidência de execução nem certificação de acessibilidade.

## 2. Preparação do ambiente

- [X] Verificar a branch e usar a versão do sistema acordada com a equipe (anotar o commit abaixo).
- [X] Abrir um terminal com Python 3.10+ e executar `python src/sistema.py` na raiz do repositório.
- [X] Garantir que o programa não peça nome, CPF, telefone, e-mail, senha ou qualquer dado real.
- [X] Preparar cronômetro e planilha ou este formulário para registrar apenas resultados anônimos.
- [X] Explicar que o teste avalia **a interface**, não a habilidade do participante.
- [X] Solicitar concordância para participar, sem necessidade de gravar áudio, vídeo ou tela.
- [X] Não oferecer dicas de comandos durante a tentativa inicial; se for necessário ajudar, registrar a intervenção.

**Ambiente da execução (preencher posteriormente):**

| Campo | Registro |
|---|---|
| Data e horário | 17/11/2026 - 15:20h |
| Sistema operacional | MacOS Tahoe 26.4 |
| Terminal / versão | Terminal |
| Python | Python 3.13.5 |
| Versão do projeto (commit SHA) | Pendente |
| Interface (`normal` ou `--simples`) | `--simples` |
| Participante | `P01` |
| Perfil geral e experiência prévia com terminal, sem dados identificáveis | Experiêcia baixa |
| Ferramenta e versão do leitor de tela (UX-01.B) | Pendente |
| Duração total | Pendente |

## 3. Orientação inicial para o participante

> "Vamos testar um assistente de orientações para consumidores. Você pode usar o teclado para escolher opções ou digitar dúvidas. O objetivo é verificar se o programa é fácil de entender; não há resposta certa sobre como você deve navegar. Use apenas situações fictícias, sem dados pessoais reais. Caso não encontre uma opção, tente como faria normalmente e me diga o que está achando difícil."

Apresentar **uma tarefa por vez**. Não mostrar os identificadores DB nem a seção “resultado esperado” ao participante, pois isso influenciaria o teste.

## 4. Tarefas principais — alinhadas ao relatório da equipe

### T01 — Taxa de serviço de 10%

**Enunciado ao participante:** "Imagine que você foi a um restaurante e o garçom cobrou uma taxa de serviço de 10%. Descubra, usando o assistente, se essa cobrança é obrigatória. Mostre onde está a fonte da orientação."

**Observador — referência esperada:** orientação `DB10`, “Taxa de serviço de 10%”. Deve exibir explicação e fonte. O participante pode escolher um tema ou digitar a própria pergunta; **não exigir um caminho específico**.

**Critério de êxito:** localizar a orientação correta e conseguir apontar a seção da fonte, sem intervenção do avaliador (considerar “com ajuda” se houve intervenção).

### T02 — Golpe no Pix

**Enunciado ao participante:** "Imagine que uma pessoa fez um Pix após cair em um golpe. Encontre no assistente uma orientação sobre quais passos tomar e onde buscar ajuda."

**Observador — referência esperada:** orientação `DB15`, “Caí em um golpe no Pix”. A pessoa deve conseguir identificar ao menos um passo e o canal de orientação/reclamação exibidos. **Não usar chaves Pix, valores, nomes ou contas reais**.

**Critério de êxito:** localizar o assunto correto e identificar próximos passos e canal indicado, com ou sem ajuda conforme registro.

### T03 — Verificação de meia-entrada (`v`)

**Enunciado ao participante:** "Considere este personagem fictício: uma pessoa estudante, com Carteira de Identificação Estudantil válida, que não se enquadra nos demais grupos apresentados. Encontre a orientação de meia-entrada e use a função que verifica se a regra se aplica ao caso."

**Observador — referência esperada:** orientação `DB14`, “Meia-entrada em cinema, shows e eventos”; opção `[v]` após a resposta. No cenário hipotético, as respostas para a checagem são **sim** à condição de estudante e **não** às demais. Espera-se um resultado indicativo de enquadramento, com aviso de que não é decisão oficial. O participante deve receber o cenário, **não a sequência de teclas**.

**Critério de êxito:** encontrar a verificação, concluir as perguntas hipotéticas e compreender que a saída é orientação informativa, não decisão oficial.

### T04 — Sem resposta e continuidade (complementar / opcional)

**Enunciado ao participante:** "Imagine que uma loja se recusou a fornecer nota fiscal. Pergunte sobre isso. Caso o assistente não encontre uma resposta, procure a lista de assuntos que ele conhece."

**Observador — referência esperada na versão inicial:** mensagem de falta de informação confiável, sem orientação inventada, seguida de alternativa para listar temas com `[1]`. Confirmar novamente na versão utilizada, pois a busca pode mudar após PRs.

**Critério de êxito:** compreender que não houve resposta confiável e conseguir encontrar uma opção de continuidade.

## 5. Ficha de observação (preencher durante o teste)

**Convenções:**
- **Sem ajuda:** completou sem intervenção; pode explorar ou corrigir erros sozinho.
- **Com ajuda:** completou após explicação ou dica do avaliador.
- **Não concluiu:** não chegou ao objetivo mesmo após tempo ou desistência.
- **Tempo:** medir do término da leitura do enunciado até conclusão ou desistência, em segundos. Não incluir instrução inicial.

| Tarefa | Status (sem ajuda / com ajuda / não concluiu) | Tempo (s) | Caminho/pergunta digitada (sem dados pessoais) | Dificuldade observada | Ajuda oferecida? | Fonte/limite compreendido? |
|---|---|---:|---|---|---|---|
| T01 | Pendente | 01:50 | pergunta digitada | Nula | Não | Sim |
| T02 | Pendente | 01:53 | pergunta digitada | Nula | Não | Sim |
| T03 | Pendente | 01:47 | pergunta digitada | Terminal Poluído | Não | Sim |
| T04 (opcional) | Pendente | 03:32 | pergunta digitada | Terminal Poluído | Não | Sim |

**Registros complementares:**
- Mensagens/confusões notadas: terminal poluído dificultando leitura
- Problemas de apresentação da fonte e de quebras de linha: texto muito grudado e sem limpeza do terminal entre menu/submenu
- Problemas de entendimento dos atalhos `[m]`, `[r1]`, `[v]`, `[1]`: Precisa melhorar
- Falhas identificadas (versão, reprodução, esperado, obtido): Falha em visualização do usuário atrapalhando na experiência de navegação no terminal.

## 6. Perguntas finais e indicadores

Perguntar sem sugerir uma nota:

1. "De 1 a 5, quão fácil foi usar o assistente?" (1 = muito difícil; 5 = muito fácil)
2. "De 1 a 5, quão útil foi a orientação apresentada?" (1 = nada útil; 5 = muito útil)
3. "O que foi mais confuso ou difícil?"
4. "Você entendeu onde conferir a fonte e que este não é um atendimento oficial?"
5. "Que mudança deixaria o assistente mais fácil de usar?"

**Indicadores calculados depois do teste:**

- **Taxa de conclusão sem ajuda:** número de tarefas concluídas sem ajuda ÷ número de tarefas executadas × 100.
- **Taxa de conclusão total:** tarefas concluídas (com ou sem ajuda) ÷ número de tarefas executadas × 100.
- **Tempo médio:** soma dos tempos de tarefas com medição ÷ número de tarefas com tempo medido. Registrar também desistências, para não distorcer a interpretação.
- **Facilidade percebida:** nota informada na escala de 1 a 5. Com um participante, reportar a nota individual, não uma média populacional.
- **Utilidade percebida:** nota informada na escala de 1 a 5.
- **Dificuldades observadas:** resumo qualitativo das dificuldades concretas, com frequência por tarefa quando aplicável.

**Resultados (não preencher antecipadamente):**

| Indicador | Valor |
|---|---|
| Tarefas executadas | Pendente |
| Concluídas sem ajuda | Pendente |
| Concluídas com ajuda | Pendente |
| Não concluídas | Pendente |
| Taxa de conclusão sem ajuda | Pendente |
| Taxa de conclusão total | Pendente |
| Tempo médio | Pendente |
| Facilidade (1–5) | Pendente |
| Utilidade (1–5) | Pendente |

## 7. Preparação da UX-01.B — teclado e leitor de tela

Estes critérios serão efetivamente testados na etapa UX-01.B:

| Critério | Como observar | Resultado |
|---|---|---|
| Teclado | Completar T01–T03 sem mouse, navegando pelo terminal | Pendente |
| Leitura do menu | Verificar se os comandos e seus significados são anunciados | Pendente |
| Leitura da fonte | Verificar se a referência e URL são compreensíveis quando lidas pelo leitor | Pendente |
| Fluxo de condições | Verificar se cada pergunta e opções `s`, `n`, `?` são anunciadas | Pendente |
| Erros e limites | Verificar se mensagens de entrada inválida/sem resposta são perceptíveis | Pendente |

Anotar **sistema operacional, aplicativo de terminal, ferramenta de leitor de tela e versão**. Se nenhum leitor de tela puder ser testado, declarar a limitação; não registrar como aprovado.

## 8. Fechamento da UX-01 (após execução)

- [ ] Registrar observação **real** de pelo menos um participante sem identificá-lo.
- [ ] Completar a seção 8 de `docs/relatorio.md` com dados reais e síntese do teste.
- [ ] Descrever ao menos **duas melhorias ou limitações** justificadas por observações.
- [ ] Documentar a avaliação por teclado e leitor de tela, inclusive ferramentas e ambiente.
- [ ] Revalidar correções eventualmente implementadas.
- [ ] Relatar que a amostra é pequena e não permite concluir acessibilidade universal.
- [ ] Incorporar evidências ao PR da UX-01, sem atribuir resultados ainda não medidos.

**Nota:** este roteiro foi preparado com base no ZIP original de 16/11/2026. A equipe informou um PR BAS-01/BUS-01 ainda não integrado no momento do planejamento. Verificar o comportamento real da versão testada e registrar seu commit.
