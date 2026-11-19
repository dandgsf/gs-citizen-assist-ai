# VAL-01 — Evidências de validação de fluxos, condições e privacidade

**Projeto:** Citizen Assist AI — FIAP Global Solution 2026.2  
**Responsável:** Renato Nascimento  
**Branch:** `test/val-01-fluxos-privacidade`  
**Status:** revalidação concluída no macOS e no Windows.
**Escopo:** VAL-01 de `docs/BACKLOG.md`; somente entradas fictícias nos testes.

## 1. Ambiente e versão sob teste

| Campo | Registro |
|---|---|
| Data | 19/11/2026 |
| Sistema operacional | macOS 26.4, build 25E246 |
| Python | 3.13.5 (`python3`) |
| Branch | `test/val-01-fluxos-privacidade` |
| `HEAD` antes do commit da revisão | `db5b717` |
| `origin/main` incorporada | `4be451f`; verificado por `git merge-base --is-ancestor origin/main HEAD` |
| Alterações testadas sem commit | R01 (UTF-8), R02 (títulos distintos), R03 (mensagem fora do escopo) |
| Commit revalidado no Windows | [`f0186a9`](https://github.com/dandgsf/gs-citizen-assist-ai/commit/f0186a92832b6b7c5d403adb7c6f88dd4de801b5) |
| Ambiente Windows | Python 3.12.10, codificação local cp1252, modo UTF-8 desabilitado e `PYTHONUTF8` ausente na execução da suíte |

BAS-01/BUS-01 já estava incorporado na `main` utilizada como base local. O commit acima registra o estado na data dos testes, não um estado futuro do remoto.

## 2. Testes automatizados e avaliador

Executar na raiz do repositório:

```bash
python3 -m unittest discover -s tests -p "test_val01_*.py" -v
python3 -m unittest discover -s tests -v
python3 src/avaliar.py
```

| Verificação | Resultado observado |
|---|---|
| VAL-01 | **25/25**, `Ran 25 tests in 0.666s` — OK |
| Suíte integrada | **34/34**, `Ran 34 tests in 8.548s` — OK |
| VAL-01 no Windows | **25/25**, sem `PYTHONUTF8` |
| Suíte integrada no Windows | **34/34**, sem `PYTHONUTF8` |
| Robustez do avaliador | **14/14** tratados |
| Regressões T41–T44 e V15–V18 | **24/24** combinações corretas |

### 2.1 Matriz dos 25 cenários da VAL-01

| ID | Esperado | Obtido no Windows | Resultado |
|---|---|---|---|
| 01 | Título, aviso de não oficialidade e saída normal | Título e aviso exibidos. O comando 0 encerrou com despedida. | OK |
| 02 | Listar temas | Atalho t1 e tema Mercado e lojas exibidos. | OK |
| 03 | Abrir situação com fonte e relacionados | Atalho s1, fonte e seção de assuntos relacionados exibidos. | OK |
| 04 | Abrir DB01 → DB02 → DB05 em ordem | Os três títulos esperados apareceram nessa ordem, com pelo menos três fontes. | OK |
| 05 | Recusar atalhos inválidos | A CLI apresentou aviso para os cinco atalhos e encerrou normalmente. | OK |
| 06 | Pedir uma entrada quando vazia | Exibiu a mensagem de entrada vazia e retornou sem atalhos. | OK |
| 07 | Recusar entrada só de símbolos | Exibiu a mensagem de entrada incompreensível e retornou sem atalhos. | OK |
| 08 | Pedir desambiguação | Exibiu a mensagem de múltiplas situações, com atalhos a e n. | OK |
| 09 | Aceitar recusa das sugestões | A opção n exibiu instrução para reformular a consulta. | OK |
| 10 | Explicar o limite de escopo | Exibiu a mensagem de escopo, sem fonte nem atalhos. | OK |
| 11 | Avisar quando falta informação confiável | Informou a limitação, indicou a lista de situações e retornou sem atalhos de resposta. | OK |
| 12 | Exibir ajuda e permitir ativar explicação | Exibiu Como funciona e confirmou Modo explicação ligado. | OK |
| 13 | Distinguir sim, não, dúvida e entrada inválida | Retornou verdadeiro, falso, indeterminado e inválida conforme os exemplos. | OK |
| 14 | Avaliar AND nos três estados | Retornou verdadeiro com todas verdadeiras, falso quando uma era falsa e indeterminado no caso restante. | OK |
| 15 | Avaliar OR nos três estados | Retornou verdadeiro quando uma era verdadeira, falso com todas falsas e indeterminado no caso restante. | OK |
| 16 | Verificar DB07 com sim, não e dúvida | Indicou aplicação, não aplicação e resultado indeterminado nos três cenários. | OK |
| 17 | Verificar DB14 com sim, não e dúvida | Indicou enquadramento, não enquadramento e resultado indeterminado nos três cenários. | OK |
| 18 | Verificar DB23 com sim, não e dúvida | Indicou gratuidade, não aplicação e resultado indeterminado nos três cenários. | OK |
| 19 | Pedir de novo após resposta inválida | Avisou que a resposta não foi reconhecida e concluiu a checagem após respostas válidas. | OK |
| 20 | Mascarar o CPF no formato testado | Identificou CPF e removeu o valor do texto retornado. | OK |
| 21 | Mascarar telefone com separadores | Identificou telefone e removeu o valor do texto retornado. | OK |
| 22 | Mascarar e-mail fictício | Identificou e-mail e removeu o valor do texto retornado. | OK |
| 23 | Mascarar cartão com espaços | Identificou cartão e removeu o valor do texto retornado. | OK |
| 24 | Mascarar os quatro tipos na mesma entrada | Identificou os quatro tipos e removeu todos os valores de teste. | OK |
| 25 | Avisar sobre e-mail sem reexibi-lo na CLI | Exibiu o aviso de dado digitado e omitiu o endereço na saída. | OK |

### 2.2 Revisões do PR #4

| Revisão | Correção | Evidência |
|---|---|---|
| R01 | `encoding="utf-8"` em duas chamadas de `subprocess.run()` | VAL-01 25/25 e suíte integrada 34/34 no macOS e no Windows |
| R02 | Teste 04 confirma títulos distintos na ordem DB01 → DB02 → DB05 | Isolado 1/1 (0.086s), VAL-01 25/25 |
| R03 | Teste 10 exige mensagem `Por enquanto eu só cubro` | Isolado 1/1 (0.009s), VAL-01 25/25 |
| R04 | Revalidar versão integrada e documentar regressões e limitações | Evidências das seções seguintes |

### 2.3 Desempenho do avaliador

| Estratégia | Teste/regressão | Validação inédita | Tempo médio |
|---|---:|---:|---:|
| Palavras | 59/60 (98,3%) | 14/17 (82,4%) | 0,082 ms |
| TF-IDF | 58/60 (96,7%) | 12/17 (70,6%) | 0,147 ms |
| Híbrida | 59/60 (98,3%) | 14/17 (82,4%) | 0,188 ms |

As divergências listadas pelo avaliador foram classificadas como **erros seguros**. Os tempos medem processamento do algoritmo naquele ambiente, não tempo de uso humano. Não se deve inferir ausência de erros fora do corpus avaliado.

## 3. Regressões pós-merge — T41–T44 e V15–V18

Os oito casos foram conferidos nas três estratégias (`palavras`, `tfidf` e `hibrida`): **24/24 combinações corretas**.

| ID | Esperado | Palavras (obtido) | TF-IDF (obtido) | Híbrida (obtido) | Acertos |
|---|---|---|---|---|---|
| T41 | `SEM_RESPOSTA` | `SEM_RESPOSTA` | `SEM_RESPOSTA` | `SEM_RESPOSTA` | 3/3 |
| T42 | `DB16` | `DB16` | `DB16` | `DB16` | 3/3 |
| T43 | `DB20` | `DB20` | `DB20` | `DB20` | 3/3 |
| T44 | `DB20` | `DB20` | `DB20` | `DB20` | 3/3 |
| V15 | `SEM_RESPOSTA` | `SEM_RESPOSTA` | `SEM_RESPOSTA` | `SEM_RESPOSTA` | 3/3 |
| V16 | `SEM_RESPOSTA` | `SEM_RESPOSTA` | `SEM_RESPOSTA` | `SEM_RESPOSTA` | 3/3 |
| V17 | `DB20` | `DB20` | `DB20` | `DB20` | 3/3 |
| V18 | `SEM_RESPOSTA` | `SEM_RESPOSTA` | `SEM_RESPOSTA` | `SEM_RESPOSTA` | 3/3 |

**REG-BUS-01 (V15):** a pergunta de academia passou a retornar `SEM_RESPOSTA`, e não uma orientação indevida de telecomunicações. A verificação foi positiva nas três estratégias avaliadas.

## 4. Privacidade — limitações reproduzidas

Verificação direta da função `privacidade.mascarar()` em 19/11/2026, com valores **fictícios**:

| Caso | Entrada de teste | Tipo identificado | Saída observada | Análise |
|---|---|---|---|---|
| LIM-PRIV-01 | `Meu telefone é 11987654321` | `['CPF']` | `Meu telefone é [removido]` | Valor mascarado, mas classificado equivocadamente como CPF. |
| LIM-PRIV-02 | `Meu CPF é 123/456/789-00` | `[]` | `Meu CPF é 123/456/789-00` | Formato com `/` não reconhecido; valor permaneceu visível. |

O primeiro achado é de **classificação incorreta** apesar do mascaramento. O segundo é uma **falha de cobertura** que pode ocasionar exposição de entrada sensível em formato não previsto. Não há evidência de que o mascaramento proteja todos os dados pessoais, todos os formatos ou eventuais logs externos.

**Encaminhamento:** registrar as limitações e discutir prioridade/correção com o responsável pelo módulo `src/privacidade.py`; este PR acrescenta validação e evidências, não altera a regra de mascaramento.

## 5. Critério de fechamento da VAL-01

- [x] Incorporar `origin/main` com BAS-01/BUS-01 na branch de trabalho.
- [x] Reexecutar a suíte específica VAL-01 (25/25).
- [x] Reexecutar a suíte integrada (34/34).
- [x] Executar o avaliador (estratégias e 14/14 de robustez).
- [x] Conferir T41–T44 e V15–V18 (24/24).
- [x] Reproduzir e registrar LIM-PRIV-01 e LIM-PRIV-02.
- [x] Validar R01–R03 no macOS.
- [x] Revalidar o commit publicado no Windows sem `PYTHONUTF8`.
- [x] Vincular a evidência à VAL-01 no backlog.
- [x] Conferir as correções do PR #4 nas duas chamadas de subprocesso e nos testes de navegação e fora do escopo.

As verificações automatizadas da VAL-01 passaram nos dois ambientes. O avaliador confirmou as regressões selecionadas e as verificações de robustez. Os limites de mascaramento permanecem registrados na seção 4.
