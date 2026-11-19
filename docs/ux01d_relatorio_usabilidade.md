# UX-01.D — Relatório consolidado de usabilidade e acessibilidade

**Projeto:** Citizen Assist AI — FIAP Global Solution 2026.2  
**Responsável:** Renato Nascimento  
**Branch:** `test/ux-01-usabilidade`  
**Data das avaliações registradas:** 17/11/2026  
**Status:** consolidação documental preparada para revisão; sem correções de código realizadas nesta etapa.

## 1. Objetivo e rastreabilidade

Avaliar usabilidade e acessibilidade da interface textual, preservando observações reais, resultados de navegação por teclado, leituras com VoiceOver e limitações. Atende à tarefa **UX-01** do `docs/BACKLOG.md` (teste com uma pessoa, teclado, leitor de tela, registro de dificuldades e pelo menos duas melhorias). **Não representa certificação de acessibilidade nem uma validação jurídica das orientações.**


**Fontes internas desta síntese:**

As execuções UX-01.A e UX-01.C foram realizadas com o mesmo participante, identificado anonimamente como P01, em duas sessões distintas. Os resultados foram documentados separadamente.

- `docs/ux01_roteiro_usabilidade.md` (UX-01.A):
  primeira execução, utilizando o modo `--simples`,
  com uma tarefa T04 sobre emissão de nota fiscal.
- `docs/ux01b_validacao_acessibilidade.md` (UX-01.B):
  sete testes de teclado e oito verificações com VoiceOver.
- `docs/ux01c_teste_participante.md` (UX-01.C):
  segunda execução, com uma tarefa T04 sobre
  aluguel de carro na Islândia.

Os resultados das duas execuções foram preservados
separadamente, sem agregação das métricas.

A UX-01.C foi utilizada como referência principal
para os indicadores consolidados.

## 2. Ambiente e método

### UX-01.A — Primeira execução

- Data: 17/11/2026.
- Horário registrado: 15h20.
- Sistema operacional: macOS Tahoe 26.4.
- Aplicativo: Terminal.
- Python: 3.13.5.
- Modo de execução: `--simples`.
- Identificador do participante: P01.
- Tarefas executadas: 4.
- Soma dos tempos das tarefas: 09:02.
- Tempo médio por tarefa: 02:15,5.
- Commit SHA avaliado: não registrado.

### UX-01.C — Segunda execução

- Data: 17/11/2026.
- Horário: 16:05.
- Sistema operacional: macOS Tahoe 26.4.
- Aplicativo: Terminal.
- Comando documentado: `python3 src/sistema.py`.
- Identificador do participante: P01.
- Tarefas executadas: 4.
- Soma dos tempos das tarefas: 08:20.
- Tempo médio por tarefa: 02:05.
- Tecnologias assistivas utilizadas pelo participante: não.
- Commit SHA avaliado: não registrado.

### UX-01.B — Avaliação de acessibilidade

- Data: 17/11/2026.
- Horário registrado: 16h05.
- Sistema operacional: macOS Tahoe 26.4.
- Leitor de tela: VoiceOver.
- Avaliação realizada separadamente pelo responsável.
- Testes de teclado: 7.
- Verificações com VoiceOver: 8.

### Limitações de rastreabilidade

As avaliações A e C correspondem a execuções distintas.
Seus tempos e indicadores foram mantidos separadamente.

O nome da branch não identifica uma versão imutável.
Como os commits exatos das execuções não foram registrados,
não é possível atribuir retrospectivamente um SHA
com segurança.

## 3. Execução de tarefas com participante (UX-01.C)

| ID | Objetivo | Resultado registrado | Tempo | Identificou a fonte? | Dificuldade anotada |
|---|---|---|---|---|---|
| T01 | Taxa de serviço (DB10) | Concluiu sem ajuda | 01:34 (94 s) | Sim | Muita informação no menu |
| T02 | Golpe no Pix (DB15) | Concluiu sem ajuda | 01:56 (116 s) | Não | Muita informação no menu |
| T03 | Meia-entrada e condições (DB14) | Concluiu sem ajuda | 01:48 (108 s) | Sim | Muita informação no menu |
| T04 | Pergunta fora da base (aluguel de carro na Islândia) | Concluiu sem ajuda | 03:02 (182 s) | Não se aplica | Muita informação no menu |

**Cálculos verificados:**

- Tarefas executadas: **4**; concluídas sem ajuda: **4**; com ajuda: **0**; não concluídas: **0**.
- Taxa de conclusão sem ajuda = `4 / 4 × 100 = 100%`.
- Taxa de conclusão total = `(4 + 0) / 4 × 100 = 100%`.
- Soma dos tempos = `94 + 116 + 108 + 182 = 500 s`.
- Tempo médio = `500 / 4 = 125 s = 02:05` por tarefa (inclui T04).
- Fonte identificada = `2 / 3 = 66,7%` das tarefas aplicáveis (T01–T03); T04 não exigia fonte.
- Notas de P01: navegação **4/5**; clareza **4/5**; localização de fontes **3/5**; facilidade geral **4/5**. Média descritiva das quatro notas: **3,75/5**, sem significância populacional.

**Interpretação:** todas as tarefas foram registradas como concluídas, mas houve uma dificuldade visual repetida. A localização das fontes aparece como fragilidade específica tanto na nota 3/5 quanto na não identificação da fonte em T02. A taxa de conclusão não mede qualidade da orientação, satisfação de uma população nem capacidade universal de utilização.

### Evidência complementar da tarefa T04

Em 19/11/2026, a tarefa T04 foi reproduzida
tecnicamente no commit `593f7c2`, nos modos
normal e `--simples`.

Nos dois modos, o assistente reconheceu a pergunta
fora do escopo, apresentou uma mensagem explicativa,
permitiu listar cinco temas pelo comando `1`
e encerrou normalmente pelo comando `0`.

Identificou-se como oportunidade de melhoria
a ausência de instrução explícita sobre como
continuar a navegação após a mensagem de limitação.

As reproduções foram realizadas pelo avaliador,
não pelo participante P01.

O formulário preenchido durante o teste original
não registrou a sequência de comandos. Entretanto,
o observador confirmou retrospectivamente que P01
digitou espontaneamente `1` após receber a mensagem
de limitação de escopo.

Assim, a T04 atendeu aos dois critérios definidos:
reconhecer a ausência de orientação confiável e
encontrar uma alternativa para continuar navegando.

A tarefa permanece classificada como
"Concluída sem ajuda", com tempo de 03:02.

## 4. Navegação por teclado e leitor de tela (UX-01.B)

| Dimensão | Resultado registrado | Interpretação |
|---|---:|---|
| Teclado, KB-01 a KB-07 | **7/7 marcados "Ok"** | Fluxos examinados puderam ser executados via teclado, conforme registro do avaliador. |
| VoiceOver, SR-01 a SR-08 | **2/8 aprovados sem ressalva** | SR-02 (temas) e SR-08 (modo simples) receberam avaliação textual "Aprovado". |
| VoiceOver com ressalvas | **6/8** | SR-01, SR-03, SR-04, SR-05, SR-06 e SR-07 indicam dificuldade, sem bloqueio total documentado. |

As notas informais 4 e 5 da tabela de VoiceOver **não possuem escala definida** no roteiro e, portanto, não são usadas como indicador quantitativo de acessibilidade.

A avaliação foi realizada com VoiceOver em configuração
automática de inglês/português. A versão específica do
leitor de tela, a configuração detalhada das vozes e os
trechos exatos anunciados não foram registrados.

As observações indicam dificuldades de compreensão
durante a leitura por VoiceOver, mas não permitem
determinar sua causa raiz (programa, terminal,
configurações ou leitor de tela).

Embora o caso SR-08 tenha sido classificado como
aprovado, não há evidências comparativas suficientes
para afirmar que o modo `--simples` apresenta
acessibilidade superior ao modo normal.

### Complementação documental — UX-01.R03

Foram revisados os seis casos de VoiceOver
classificados como "Aprovado com ressalva":
SR-01, SR-03, SR-04, SR-05, SR-06 e SR-07.

A observação geral registrada foi dificuldade
de compreensão da apresentação textual por meio
do leitor de tela.

Como as anotações originais não detalham
o comportamento individual de cada caso,
foram documentados os possíveis impactos
de usabilidade e as melhorias recomendadas.

Não foram produzidas novas evidências de execução,
transcrições de áudio ou diagnósticos de causa raiz.

O detalhamento dos incidentes permanece como
limitação metodológica para a aprovação final
da acessibilidade.

## 5. Problemas e melhorias priorizadas

| ID | Prioridade | Evidência | Melhoria proposta (ainda não implementada) | Como revalidar |
|---|---|---|---|---|
| UX-M01 | Alta | Excesso de conteúdo no menu em T01–T04; comentário sobre textos próximos e caracteres especiais | Separar seções do terminal com títulos e espaçamento previsível; reduzir ruído visual e orientar claramente qual comando digitar | Repetir T01–T04, registrar compreensão, tempo e observações antes/depois |
| UX-M02 | Alta | 6/8 verificações SR com ressalvas e observação sobre escrita pouco adequada ao VoiceOver | Exibir descrições lineares para atalhos, anunciar rótulos em texto, simplificar separadores e testar leitura sequencial; não depender exclusivamente de símbolos | Reexecutar SR-01–SR-08 em Terminal.app e VoiceOver com versão/idioma anotados; registrar trechos literais anunciados |
| UX-M03 | Alta | Nota 3/5 para fontes; em T02 o participante não identificou a fonte | Dar maior destaque à seção “Fonte consultada”, com organização clara de título, URL, data e aviso; evitar que a quebra de URL prejudique sua leitura/cópia | Repetir identificação das fontes em T01–T03 e casos SR-03/SR-07 |
| UX-M04 | Média | UX-01.A relata dificuldade com atalhos `m`, `r1`, `v` e `1` | Incluir legenda contextual por extenso, instrução de retorno e exemplo de comando nos menus | Repetir navegação KB-02–KB-06 e tarefas com novo participante |

As melhorias acima são **recomendações**, não correções já executadas. Respeitar a divisão da equipe antes de alterar `src/sistema.py`.

## 6. Limitações da avaliação

1. Apenas **um participante (P01)**; não há representatividade estatística nem diversidade de habilidades comprovada.
2. O participante P01 **não utilizou tecnologia assistiva**. Os testes de VoiceOver foram observados separadamente pelo avaliador.
3. A avaliação do VoiceOver carece de trechos concretos de leitura, versão específica do leitor de tela, configuração detalhada das vozes e comparação documentada entre os modos normal e `--simples`.
4. A identificação do **commit SHA testado** está ausente; o nome da branch não identifica uma versão imutável.
5. As avaliações UX-01.A e UX-01.C foram realizadas em sessões distintas, com cenários e tempos diferentes. Por isso, seus indicadores não foram agregados nem utilizados para uma comparação direta de desempenho.
6. Tempo de execução de tarefa humana **não é** tempo de processamento da consulta usado em métricas de algoritmo.
7. Nenhuma melhoria de interface foi implementada ou revalidada neste relatório.
8. A amostra não autoriza concluir que a interface atende integralmente a padrões de acessibilidade.

## 7. Conclusão e estado da tarefa

A avaliação disponível **atende ao núcleo de evidências previsto para UX-01**: tarefas reais registradas com participante anônimo, navegação por teclado, observações de uso com VoiceOver, dificuldades e mais de duas propostas de melhoria. Na versão examinada, P01 concluiu as quatro tarefas sem ajuda (100%), enquanto a leitura por VoiceOver apresentou ressalvas em seis de oito verificações. Recomenda-se priorizar **clareza textual e de navegação, leitura por tecnologias assistivas e apresentação das referências**.

**Estado recomendado no backlog até revisão:** **Em revisão / Aguardando integração**, não marcar como concluído por conta própria. O critério de aceite permanece sujeito à conferência do Danilo, identificação da versão avaliada e decisão da equipe sobre revalidar ajustes. As limitações identificadas devem constar do relatório final, mesmo que não sejam corrigidas nesta entrega.

## 8. Checklist para o PR

- [x] Criar roteiros e registrar execução com P01, sem dados identificáveis.
- [x] Registrar sete casos de teclado e oito verificações VoiceOver.
- [x] Calcular e interpretar taxas, tempos e percepção do participante.
- [x] Apontar limitações e pelo menos duas melhorias fundamentadas.
- [ ] Acrescentar o SHA **da versão de fato testada**, caso recuperável.
- [ ] Se possível, completar idioma/versão do VoiceOver e descrever um exemplo verificável de dificuldade.
- [ ] Conferir se as alterações integradas pelo PR #3 afetam os fluxos avaliados na UX-01 e revalidar os casos impactados, quando necessário.
- [ ] Revisão do Danilo e merge.

**Nota de integração:** este PR adiciona apenas arquivos de `docs/ux01*`, evitando editar `docs/BACKLOG.md` ou `docs/relatorio.md` enquanto outros PRs podem modificá-los. O responsável pela documentação pode incorporar esta síntese ao relatório final.
