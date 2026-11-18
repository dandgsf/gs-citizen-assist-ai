# UX-01.D — Relatório consolidado de usabilidade e acessibilidade

**Projeto:** Citizen Assist AI — FIAP Global Solution 2026.2  
**Responsável:** Renato Nascimento  
**Branch:** `test/ux-01-usabilidade`  
**Data das avaliações registradas:** 17/11/2026  
**Status:** consolidação documental preparada para revisão; sem correções de código realizadas nesta etapa.

## 1. Objetivo e rastreabilidade

Avaliar usabilidade e acessibilidade da interface textual, preservando observações reais, resultados de navegação por teclado, leituras com VoiceOver e limitações. Atende à tarefa **UX-01** do `docs/BACKLOG.md` (teste com uma pessoa, teclado, leitor de tela, registro de dificuldades e pelo menos duas melhorias). **Não representa certificação de acessibilidade nem uma validação jurídica das orientações.**

**Fontes internas desta síntese:**

- `docs/ux01_roteiro_usabilidade.md` (UX-01.A): roteiro e anotações auxiliares;
- `docs/ux01b_validacao_acessibilidade.md` (UX-01.B): sete casos KB e oito verificações SR;
- `docs/ux01c_teste_participante.md` (UX-01.C): execução e avaliação de P01. **Única fonte oficial dos indicadores de tarefas humanas** nesta síntese.

O roteiro A contém tempos diferentes e uma T04 sobre **nota fiscal**, enquanto o roteiro C usa T04 sobre **aluguel de carro na Islândia**. Pois foram feitos em tempos diferentes.

## 2. Ambiente e método

- Data: 17/11/2026.
- Plataforma registrada: macOS Tahoe 26.4; Terminal.app; Python 3.13.5 informado no roteiro A.
- Participante P01, experiência prévia baixa com terminal segundo roteiro A, consentimento informado registrado em C, sem dados pessoais identificáveis.
- Execução com P01: `python3 src/sistema.py`, conforme roteiro C; sem tecnologia assistiva e sem ajuda durante as tarefas.
- Teclado e leitor de tela: avaliação feita separadamente pelo responsável; VoiceOver foi utilizado do MacOS, idioma de inglês/português automático e descrição da diferença entre modo normal e `--simples` não foram registrados.
- **Branch identificada, mas SHA do commit não registrado.** Antes de publicar como evidência reprodutível, executar `git rev-parse --short HEAD` e preencher o hash do commit **efetivamente avaliado**, caso seja possível recuperá-lo. O HEAD atual não deve ser apresentado automaticamente como versão testada se houve commits posteriores.

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

## 4. Navegação por teclado e leitor de tela (UX-01.B)

| Dimensão | Resultado registrado | Interpretação |
|---|---:|---|
| Teclado, KB-01 a KB-07 | **7/7 marcados "Ok"** | Fluxos examinados puderam ser executados via teclado, conforme registro do avaliador. |
| VoiceOver, SR-01 a SR-08 | **2/8 aprovados sem ressalva** | SR-02 (temas) e SR-08 (modo simples) receberam avaliação textual "Aprovado". |
| VoiceOver com ressalvas | **6/8** | SR-01, SR-03, SR-04, SR-05, SR-06 e SR-07 indicam dificuldade, sem bloqueio total documentado. |

As notas informais 4 e 5 da tabela de VoiceOver **não possuem escala definida** no roteiro e, portanto, não são usadas como indicador quantitativo de acessibilidade.

A observação disponível indica **dificuldade na compreensão da leitura por VoiceOver**, mas **não traz transcrição do que foi falado**, versão exata do leitor, idioma de voz nem contraste descritivo entre modos. A causa raiz (programa, terminal, configurações ou leitor de tela) não foi comprovada. Apesar de o caso SR-08 ter sido classificado como aprovado, **não há evidência detalhada suficiente para afirmar que o modo `--simples` é superior**.

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
3. A avaliação de VoiceOver carece de trechos concretos de leitura, versão/idioma do leitor e comparação documentada entre modos.
4. A identificação do **commit SHA testado** está ausente; o nome da branch não identifica uma versão imutável.
5. Os registros de UX-01.A não são conciliáveis de maneira segura com UX-01.C; não foram agregados.
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
- [ ] Confirmar se o PR BAS-01/BUS-01 altera fluxos relevantes; repetir apenas os testes afetados após integração.
- [ ] Revisão do Danilo e merge.

**Nota de integração:** este PR adiciona apenas arquivos de `docs/ux01*`, evitando editar `docs/BACKLOG.md` ou `docs/relatorio.md` enquanto outros PRs podem modificá-los. O responsável pela documentação pode incorporar esta síntese ao relatório final.
