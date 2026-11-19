# UX-01.B — Validação de navegação por teclado e leitor de tela

**Projeto:** FIAP Global Solution 2026.2 — Citizen Assist AI  
**Responsável:** Renato Nascimento  
**Branch prevista:** `test/ux-01-usabilidade`  
**Status:** **planejado; execução manual executada**  
**Fonte do protocolo:** `docs/BACKLOG.md` (UX-01) e fluxos de `src/sistema.py`, examinados no ZIP-base da equipe. Revisar comandos se a versão do GitHub mudar.

## 1. Objetivo e critérios

Verificar se o usuário consegue iniciar o programa, consultar temas e orientações, navegar por assuntos relacionados, responder às condições e encerrar a aplicação **sem mouse**; e se um leitor de tela consegue comunicar essas ações, orientações, referências e limites de maneira compreensível.

**Não confundir:** (a) comandos aceitos pelo programa, (b) conteúdo de fato anunciado pelo leitor de tela e (c) compreensão pelo usuário. Esta etapa exige observação manual; testes automatizados não substituem o leitor de tela e o teste UX-01.C com uma pessoa real.

**Critérios:** (i) todas as ações essenciais executáveis somente por teclado; (ii) indicação compreensível do que digitar; (iii) saída importante e aviso não dependentes de sinais visuais; (iv) fonte e data acessíveis; (v) possibilidade de recuperar erro/entrada inválida; (vi) saída segura.

## 2. Ambiente da execução

| Campo | Informação |
|---|---|
| Data/hora | 17/11/2026 / 16:05 |
| Responsável pela execução | Renato Nascimento |
| Sistema operacional/versão | MacOS Tahoe (`26.4`) |
| Aplicativo de terminal e versão | Terminal e VSCode |
| Python | (`python 3.13.5`) |
| Branch utilizada | `test/ux-01-usabilidade` |
| Commit SHA da execução original | Não registrado |
| Leitor de tela/versão e idioma de voz | VoiceOver MacOS, inglês/português automático |
| Modo do programa | Normal; repetir casos críticos com `--simples` |
| Acessórios e ajustes relevantes | Concluído (teclado Mac, necessidade de Fn nas teclas F) |

Executar na **raiz do repositório**:

```bash
git branch --show-current
git rev-parse --short HEAD
sw_vers
python3 --version
python3 src/sistema.py
```

O projeto também documenta `python src/sistema.py`; use `python3` quando `python` não estiver configurado no macOS.

## 3. Navegação por teclado — executar SEM VoiceOver inicialmente

Para cada caso, observe se a tecla **Enter** conclui a entrada e se a tela fornece instruções suficientes para continuar. Não use o mouse.

| ID | Ação | Resultado esperado (observável) | Resultado real | Classificação |
|---|---|---|---|---|
| KB-01 | Abrir a aplicação | Aparecem título, aviso de não oficialidade, menu e `Sua dúvida ›` | Ok | Executado |
| KB-02 | Digitar `1`, Enter; depois `t3`, Enter; depois `s1`, Enter | Lista temas, situações de “Bares, restaurantes e lazer” e abre DB10 (“Taxa de serviço de 10%”) | Ok | Executado |
| KB-03 | Após DB10, digitar `r1`, Enter | Abre assunto relacionado (na base original: DB11, “Consumação mínima”) | Ok | Executado |
| KB-04 | Digitar `m`, Enter; depois escrever `golpe no pix`, Enter | Reexibe menu e apresenta orientação pertinente com fonte | Ok | Executado |
| KB-05 | Digitar `m`, Enter; digitar `99`, Enter; depois Enter em branco | Mostra mensagem de opção inexistente e trata entrada vazia, sem encerrar ou travar | Ok | Executado |
| KB-06 | Digitar `m`, Enter; escrever `tenho direito a meia entrada?`, Enter; acionar `v`, Enter; responder com `s`, `n` ou `?` nas perguntas | A checagem é acessível por teclado, informa condições e exibe aviso de que não é decisão oficial; caso a pergunta não encontre DB14, alcançar DB14 por `1` → `t3` → `s5` na base original | Ok | Executado |
| KB-07 | Digitar `0`, Enter | Encerramento com mensagem de despedida | Ok | Executado |

**Observações:** os códigos `t3`, `s1` e `s5` correspondem à ordem da base no ZIP inicial; confirmar a ordem na versão testada. O atalho `r1` só vale após exibir uma resposta que o ofereça. O atalho `v` só vale após um registro com condições.

## 4. Leitor de tela — VoiceOver (macOS)

1. Ative VoiceOver em **Ajustes do Sistema → Acessibilidade → VoiceOver**, ou pressione **Command + F5** (em alguns teclados pode ser preciso pressionar **Fn** também). Consulte o guia da Apple se o atalho variar.
2. Abra o Terminal.app, dê foco à janela de terminal, abra o programa com `python3 src/sistema.py` e **não use o mouse**.
3. Ouça a saída automática. Caso algum trecho não seja anunciado automaticamente, use os comandos de navegação/leitura do VoiceOver para reler a saída. Anote **se precisou reler manualmente**; não marque como “anúncio automático”.
4. `VO` é o modificador do VoiceOver, geralmente **Control + Option**. Execute os mesmos fluxos nos modos normal e `--simples` quando a pontuação/símbolos provocarem dificuldade.
5. Para encerrar, digite `0` quando o foco estiver na entrada. Desative o VoiceOver se desejar usando o mesmo atalho ou os Ajustes do Sistema.

| ID | Verificação de leitura | Critério esperado | Resultado real | Nota informal |
|---|---|---|---|---|
| SR-01 | Início | Leitura do nome, aviso de não oficialidade, opções e prompt de entrada, automaticamente ou por navegação de leitura | Aprovado com ressalva | 4 |
| SR-02 | Lista de temas (`1`) e situações (`t3`) | Os códigos `t1...` e `s1...` e rótulos são compreensíveis; sequência permite escolher | Aprovado | 5 |
| SR-03 | Resposta DB10 (`s1` em `t3`) | O leitor consegue chegar ao título, orientação, fonte, URL, data e avisos | Aprovado com ressalva | 4 |
| SR-04 | Assuntos relacionados (`r1`) | Lê “assuntos relacionados” e o código `r1`, associando-o ao título | Aprovado com ressalva | 4 |
| SR-05 | Checagem DB14 (`v`) | O leitor anuncia cada pergunta, aceita resposta e lê conclusão/aviso | Aprovado com ressalva | 4 |
| SR-06 | Opção inválida e entrada vazia | O leitor consegue comunicar o erro e o caminho de recuperação | Aprovado com ressalva | 4 |
| SR-07 | URL longa e marcadores (`»`, `(!)`, `─`) | Fonte e endereço são compreensíveis e podem ser recuperados mesmo que o terminal quebre linhas | Aprovado com ressalva | 4 |
| SR-08 | Modo simples | Repetir SR-01, SR-03 e SR-07 com `python3 src/sistema.py --simples` e comparar clareza | Aprovado | 4 |

**Nota importante:** se o leitor de tela não anunciar uma nova resposta automaticamente, registre isso separadamente de “não é possível reler o texto”. O comportamento varia conforme o terminal, versão do macOS e configurações do VoiceOver.

## 5. Registro de incidentes - UX-01.R03

**Origem:** avaliação manual realizada em 17/11/2026, utilizando VoiceOver no macOS Tahoe 26.4, com configuração automática de inglês/português.

**Observação geral:** durante a avaliação, foram percebidas dificuldades de compreensão da apresentação textual por meio do VoiceOver. Os fluxos examinados receberam classificação de aprovação com ressalvas, sem registro de bloqueio total.

As anotações originais não individualizaram os trechos efetivamente anunciados, as intervenções de releitura ou a origem técnica de cada dificuldade. Por esse motivo, os possíveis impactos relacionados abaixo são hipóteses de usabilidade, e não falhas específicas comprovadas.

| Caso | Resultado registrado | Possível impacto a investigar | Melhoria proposta |
|---|---|---|---|
| SR-01 — Menu inicial | Aprovado com ressalva; dificuldade específica não registrada | Dificuldade para distinguir avisos, opções e campo de entrada durante a leitura sequencial | Simplificar a apresentação e separar instruções por rótulos claros |
| SR-03 — Orientação DB10 | Aprovado com ressalva; dificuldade específica não registrada | Maior esforço para localizar orientação, fonte, URL e avisos | Organizar essas informações em blocos textuais identificáveis |
| SR-04 — Assuntos relacionados | Aprovado com ressalva; dificuldade específica não registrada | Possível dificuldade para relacionar o atalho `r1` ao assunto correspondente | Apresentar instruções por extenso junto aos atalhos |
| SR-05 — Verificação de condições | Aprovado com ressalva; dificuldade específica não registrada | Possível dificuldade para acompanhar perguntas, respostas e conclusão | Utilizar instruções lineares e identificar claramente cada etapa |
| SR-06 — Entradas inválidas | Aprovado com ressalva; dificuldade específica não registrada | Possível dificuldade para reconhecer o erro e identificar como continuar | Exibir mensagens de recuperação com comandos explícitos |
| SR-07 — URLs e símbolos | Aprovado com ressalva; dificuldade específica não registrada | Possível dificuldade para compreender referências e elementos com pontuação especial | Reduzir símbolos dispensáveis e melhorar a apresentação de URLs |

**Impacto observado:** dificuldade geral de compreensão da leitura pelo VoiceOver, conforme anotação original. O impacto individual de cada caso não foi medido.

**Causa técnica:** não determinada. Não há evidência suficiente para atribuir as dificuldades exclusivamente ao programa, ao Terminal, ao VoiceOver ou às configurações de idioma.

**Reexecução:** não realizada nesta revisão documental. As classificações originais foram preservadas.

**Limitação:** a ausência de transcrições ou de descrições individualizadas impede confirmar quais elementos específicos produziram cada ressalva. As melhorias propostas deverão ser verificadas em uma futura avaliação de acessibilidade.

A análise não equivale a uma certificação de acessibilidade nem comprova incompatibilidade geral com leitores de tela.

## 6. Resultado consolidado

| Indicador | Resultado |
|---|---|
| Navegação por teclado | 7/7 casos marcados como OK |
| VoiceOver sem ressalvas | 2/8 casos |
| VoiceOver com ressalvas | 6/8 casos |
| Bloqueio total documentado | Nenhum |
| Impacto individual dos casos | Não mensurado |
| Causa técnica das ressalvas | Não determinada |
| Comparação objetiva entre modos | Evidência insuficiente |
| Melhorias propostas | Organização textual, atalhos e fontes |
| Reexecução nesta revisão | Não realizada |

As classificações são referentes à avaliação
original de 17/11/2026.

A revisão UX-01.R03 organizou as evidências
existentes, sem executar novos testes e sem
atribuir causas não comprovadas.

## 7. Encaminhamento

1. Registrar observações reais em todos os casos executados e listar impedimentos.
2. Priorizar problemas que bloqueiem o acesso à orientação ou às referências.
3. Se houver correções, repetir os casos afetados e preservar antes/depois.
4. Consolidar os resultados da UX-01.B com o teste real do participante na UX-01.C e com a análise de melhorias na UX-01.D.
5. Evitar editar `docs/BACKLOG.md` ou `docs/relatorio.md` enquanto houver PRs concorrentes nesses arquivos, se isso gerar conflitos; manter evidências neste documento e referenciá-las no PR.

**Referência técnica:** Manual VoiceOver da Apple: https://support.apple.com/pt-br/guide/voiceover/voic010/mac ; comandos de uso: https://support.apple.com/pt-br/guide/voiceover/cpvokys07/mac .
