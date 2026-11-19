# VAL-01 — Evidências de validação de fluxos, condições e privacidade

**Projeto:** Citizen Assist AI — FIAP Global Solution 2026.2  
**Responsável:** Renato Nascimento  
**Branch:** `test/val-01-fluxos-privacidade`  
**Status:** revalidação pós-merge executada no macOS; aguardando revisão e confirmação no Windows.  
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
| SHA da revisão publicada | **Pendente.** Registrar o SHA do commit na descrição do PR após a publicação; evitar colocar no próprio commit o seu hash. |
| Execução no Windows | **Pendente**, sob responsabilidade de revalidação na revisão; não usar `PYTHONUTF8=1`. |

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
| Robustez do avaliador | **14/14** tratados |
| Regressões T41–T44 e V15–V18 | **24/24** combinações corretas |

### 2.1 Matriz dos 25 cenários da VAL-01

| IDs | Área | Verificação | Resultado |
|---|---|---|---|
| 01–05 | Menu e navegação | Menu, assuntos e três orientações distintas DB01 → DB02 → DB05 | OK |
| 06–07 | Entradas inválidas | Entrada vazia e apenas símbolos | OK |
| 08–09 | Ambiguidade | Consulta ambígua e recusa de sugestões | OK |
| 10–11 | Falta de orientação | Fora do tema e falta de informação confiável | OK |
| 12 | Aviso | Explicação de funcionamento e limites | OK |
| 13–15 | Condições lógicas | `sim`/`não`/`não sei`, inválida, AND e OR | OK |
| 16–19 | Verificações de condições | DB07, DB14, DB23 e resposta inválida | OK |
| 20–25 | Privacidade | Padrões previstos de CPF, telefone, e-mail e cartão fictícios | OK; não cobre todos os formatos |

### 2.2 Revisões do PR #4

| Revisão | Correção | Evidência |
|---|---|---|
| R01 | `encoding="utf-8"` em duas chamadas de `subprocess.run()` | VAL-01 25/25 e suíte integrada 34/34 no macOS |
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
- [ ] Criar o commit das revisões, revalidar a versão commitada e informar o SHA na descrição do PR #4.
- [ ] Solicitar ao Danilo a confirmação no Windows sem `PYTHONUTF8=1`.
- [ ] Vincular esta evidência à VAL-01 no backlog pelo responsável pela documentação.
- [ ] Obter revisão e integração do PR #4.

**Conclusão provisória:** as verificações automatizadas e as regressões selecionadas foram aprovadas no macOS, com ressalvas de privacidade explicitamente documentadas. O aceite final depende da revisão do PR e da checagem no Windows.