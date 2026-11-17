# VAL-01 — Evidências de validação de fluxos, condições e privacidade

**Responsável:** Renato Nascimento  
**Branch de trabalho:** `test/val-01-fluxos-privacidade`  
**Status:** Em andamento — resultados finais dependem de conferência na branch atualizada e de BUS-01  
**Escopo:** VAL-01 do `docs/BACKLOG.md`  
**Princípio:** não modificar as regras do produto nem registrar dados pessoais reais nas evidências.

## 1. Ambiente e versão sob teste

Preencher **no repositório local**, antes de publicar os resultados como oficiais:

- Data e horário da execução: **[preencher]**
- Branch: `test/val-01-fluxos-privacidade`
- Commit testado (`git rev-parse --short HEAD`): **[preencher]**
- Versão Python (`python --version`): **[preencher]**
- Sistema operacional/terminal: **[preencher]**
- PR BAS-01/BUS-01 incorporado? **[sim/não e referência]**
- Execução realizada por: **[preencher]**

> **Execução preliminar fora da branch do usuário:** os 25 testes automatizados passaram em 17/11/2026. Isso **não comprova** aprovação na branch local nem na versão do PR pendente. É obrigatório repetir e registrar a execução local.

## 2. Procedimento reprodutível

Na raiz do repositório:

```bash
python --version
git branch --show-current
git rev-parse --short HEAD
python -m unittest discover -s tests -p 'test_val01_*.py' -v
python src/avaliar.py
```

No terminal, **não utilize dados pessoais reais**. Use apenas as entradas fictícias definidas no teste.

## 3. Matriz dos cenários automatizados

| IDs | Área | Entradas e fluxo | Resultado esperado | Resultado na branch |
|---|---|---|---|---|
| 01–05 | Menu/navegação | Sair; temas; selecionar situação; DB01 → DB02 → DB05; atalhos inválidos | Navegação concluída e mensagens claras | [Ok] |
| 06–07 | Entradas inválidas | Vazia e apenas símbolos | Resposta compreensível sem inventar orientação | [Okr] |
| 08–09 | Ambiguidade | `cancelar`; opção `n` | Exibir alternativas; aceitar recusa | [Ok] |
| 10–11 | Ausência de orientação | Pergunta fora do tema e sem resposta confiável | Indicar limitação e alternativas | [Ok] |
| 12 | Informações ao usuário | Menu de explicação e avisos | Informar funcionamento e limites | [Ok] |
| 13–15 | Lógica computacional | `sim`, `não`, `não sei`, inválida; AND e OR | Três valores lógicos corretos | [Ok] |
| 16–19 | Condições | DB07, DB14, DB23; respostas sim/não/dúvida; resposta inválida | Mensagens coerentes, repete entrada inválida | [Ok] |
| 20–25 | Privacidade | CPF, telefone, e-mail e cartão **fictícios** | Dados mascarados, não reexibidos na saída | [Ok] |

**Resumo da execução na branch:**
- Quantidade de testes executados: **[25]**
- Aprovados: **[25]**
- Falhas: **[0]**
- Erros de execução: **[0]**
- Evidência de execução: **[Ran 25 tests in 0.650s - OK]**

## 4. Testes exploratórios e limitações já observadas na versão original

Estas observações foram feitas na cópia do ZIP original; devem ser reproduzidas e registradas na branch após atualização:

| Caso | Entrada fictícia/ação | Esperado | Observado no ZIP original | Situação |
|---|---|---|---|---|
| LIM-PRIV-01 | Telefone celular com 11 dígitos contíguos e contexto textual explícito de telefone | Mascarar sem exibir o número, com identificação adequada | Número mascarado, mas classificado como `CPF` | Limitação de classificação — confirmar após PR |
| LIM-PRIV-02 | CPF escrito com separadores `/` não usuais | Identificar/remover ou informar claramente que formatos não reconhecidos são possíveis | Não foi mascarado | Limitação da expressão regular — confirmar após PR |
| REG-BUS-01 | Pergunta sobre cancelamento de academia | Não apresentar orientação setorial de telecomunicações | Registro DB20 incorretamente selecionado | Correção descrita no PR BUS-01, ainda não conferida nesta execução |

**Nota:** O mascaramento cobre padrões, mas não garante ausência de dados pessoais em qualquer formato. Não afirmar proteção integral nem ausência de logs externos com base nesses testes. A execução local do programa não grava consultas intencionalmente, conforme implementação observada.

## 5. Regressão depois do merge de BAS-01/BUS-01

- [ ] Atualizar a branch incorporando a `main` aprovada.
- [ ] Repetir os 25 testes automatizados e anexar resumo.
- [ ] Executar `python src/avaliar.py` na versão integrada.
- [ ] Conferir o caso V15: academia não pode receber orientação de telecomunicações.
- [ ] Conferir os casos T41–T44 e V16–V18 mencionados no PR, usando os arquivos efetivamente integrados.
- [ ] Registrar números de teste/validação **efetivamente obtidos**, e não copiar apenas a descrição do PR.
- [ ] Registrar falhas pendentes e atribuir ao responsável adequado antes de encerrar VAL-01.

## 6. Problemas e encaminhamentos

| ID | Problema | Severidade | Responsável sugerido | Ação/PR |
|---|---|---|---|---|
| LIM-PRIV-01 | Telefone sem formatação identificado como CPF | Baixa/média (classificação imprecisa; dado mascarado) | Validar com a equipe | [preencher] |
| LIM-PRIV-02 | CPF em formato incomum não mascarado | Média (possível exposição se digitado) | Validar com a equipe | [preencher] |
| REG-BUS-01 | Associação setorial incorreta, já conhecida como V15 | Alta (orientação equivocada) | Responsável por BUS-01 | [preencher] |

## 7. Critério para conclusão

- [ ] Todos os cenários da VAL-01 executados sobre a versão definida e com resultados documentados.
- [ ] Falhas e limitações reportadas sem afirmar cobertura completa.
- [ ] Regressões de BUS-01 verificadas após integração.
- [ ] Evidências vinculadas no `docs/BACKLOG.md` (preferencialmente após a integração do PR que modifica esse arquivo).
- [ ] PR específico da VAL-01 revisado por outro integrante.

**Conclusão final:** **[preencher após executar na branch e conferir o PR]**
