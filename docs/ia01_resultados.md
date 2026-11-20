# IA-01 — Resultado experimental e auditoria das evidências

**Projeto:** Citizen Assist AI — Global Solution FIAP 2026.2
**Responsável proposto:** Renato Nascimento
**Status:** execução experimental **10/10 registrada**, avaliação comparativa preenchida e evidências preparadas para revisão. Há uma **adaptação manual declarada** em duas entradas e um desvio de fidelidade de data na saída T02_B; essas limitações são parte do resultado, não foram apagadas.

## 1. Objetivo e condições declaradas

Comparar os prompts A (direto, sem base) e B (ancorado no registro do buscador, JSON), com cinco perguntas fixas. O pacote de dados informa a plataforma **ChatGPT**, o modelo **GPT-6**, a data de execução **19/11/2026**, conversas novas e independentes e o commit de preparação `90d3b3b9e903`. Esses metadados foram **declarados no manifesto**; o ZIP não contém exportações das conversas nem prova externa da seleção do modelo ou de independência de sessões. Os hashes de `data/base.json`, `data/sinonimos.json` e `src/prompts.py` constam no manifesto.

O funcionamento normal do Citizen Assist AI é determinístico; o módulo `src/prompts.py` gera textos de prompts, sem invocar um modelo generativo dentro do sistema.

## 2. Metodologia

Cinco perguntas descritas em `docs/prompts.md`, executadas uma vez com A e uma vez com B. O arquivo `data/ia01/respostas/` guarda **10 respostas integrais**. A avaliação separa: (i) validade sintática do JSON e contagem de palavras; (ii) conformidade com o registro; (iii) plausibilidade factual com referências públicas; (iv) comportamento frente à ausência de registro.

**Regra de contagem:** no modelo A, conta-se toda a resposta; no B, somente `resposta_simples`, usando a mesma expressão regular do script original. As respostas B também possuem `frase_pronta`, `fonte`, `data_verificacao` e `aviso`, que não entram na coluna de palavras. `Formato OK` significa apenas saída JSON sintaticamente e estruturalmente adequada, não aceitação do validador `validar_saida_ia`.

## 3. Tabela de comparação

| Teste | Modelo | Fonte verificável | Inventou algo* | Recusou quando devia | Formato OK | Palavras |
|---|---|---|---|---|---|---|
| 1 | A | Sim | Não | n/a | n/a | 190 |
| 1 | B | Sim | Não | n/a | Sim | 69 |
| 2 | A | Sim | Não | n/a | n/a | 175 |
| 2 | B | Sim | Sim | n/a | Sim | 73 |
| 3 | A | Sim | Não | n/a | n/a | 216 |
| 3 | B | Sim | Não | n/a | Sim | 68 |
| 4 | A | Sim | Não | Não | n/a | 235 |
| 4 | B | n/a | Não | Sim | Sim | 16 |
| 5 | A | Sim | Não | Não | n/a | 254 |
| 5 | B | n/a | Não | Sim | Sim | 19 |

\* `Inventou algo` significa **erro ou dado não sustentado identificado na revisão dos pontos principais**, não garantia de ausência de erros. Nos casos T01_B e T03_B, `Não` significa que **não se detectou informação juridicamente incorreta nos pontos avaliados**; a edição manual de `data_verificacao` é uma intervenção no prompt, reconhecida pelo responsável. Em T02_B, `Sim` corresponde **somente ao metadado de data diferente do registro recebido**, não à invenção de norma ou prazo jurídico. Fonte mencionada por nome não equivale a URL preservada.

**Referências de A:** todas as respostas A citam instituições ou leis identificáveis, mas as capturas contêm marcadores como `PROCON.SP+1`, `Planalto+1` e `Banco Central do Brasil+1`, **sem URLs de citação preservadas**. Assim, `Fonte verificável: Sim` significa que a referência nomeada pôde ser localizada externamente, **não** que a resposta tenha fornecido um link navegável completo. Nos dois casos B sem registro, o campo é `n/a`.

## 4. Achados por pergunta

### IA-T01 — sou obrigado a pagar a taxa de serviço de 10%?

- **A (190 palavras):** Procon-SP identificado pelo nome, mas a captura contém marcador PROCON.SP+1, sem URL. Afirmação central sobre gorjeta facultativa confirmada em fonte oficial; nenhuma invenção nos pontos essenciais identificada.
- **B (69 palavras em `resposta_simples`):** Fonte legal identificável e orientação compatível com registro. O responsável declarou ter alterado manualmente `data_verificacao` de 16 para 19/11 no prompt individual; a resposta copiou 19/11 corretamente desse arquivo. O registro compilado da preparação segue em 16/11. Não foi apresentada evidência de que a base do projeto tenha sido revisada e atualizada para 19/11.

### IA-T02 — meu voo atrasou 1 hora, a companhia tem que me dar internet?

- **A (175 palavras):** Resoluções ANAC 400/2016 e 813/2026 identificáveis; conclusão central compatível com mudanças de 2026. Marcador DOU 25/09/2026+1 não fornece URL verificável na captura.
- **B (73 palavras em `resposta_simples`):** A IA substituiu data_verificacao 2026-11-16 (presente no prompt individual) por 2026-11-19: metadado sem suporte no registro, falha objetiva de fidelidade. Conteúdo principal acompanha o registro.

### IA-T03 — caí num golpe no pix, tenho quantos dias para pedir o dinheiro de volta?

- **A (216 palavras):** Fonte Banco Central identificável; prazo de 80 dias e mecanismo MED compatíveis com orientação oficial. A marca Banco Central do Brasil+1 não contém endereço na captura. Sem erro material identificado nos fatos essenciais.
- **B (68 palavras em `resposta_simples`):** Prazo do MED e orientação compatíveis com registro. A data 19/11 no prompt individual veio de alteração manual declarada pelo responsável; a resposta reproduziu esse valor. O registro compilado mantém 16/11, exigindo explicitar a diferença entre condição de teste e base versionada. A mudança não foi causada exclusivamente pelo modelo.

### IA-T04 — fui demitido, quanto recebo de FGTS?

- **A (235 palavras):** Resposta sobre FGTS apesar de a pergunta estar fora do escopo do assistente de consumo: falha de recusa por ausência de regra explícita no A. Referências genéricas identificáveis, marcadores MTE+1/Planalto+1/FGTS+2 sem links; principais regras condicionais verificadas.
- **B (16 palavras em `resposta_simples`):** Status sem_informacao adequado; fonte/data vazias porque não existe registro recuperado. JSON formalmente válido; a função validar_saida_ia rejeita esse status para exibição, como previsto para fallback.

### IA-T05 — a academia não quer cancelar meu plano sem multa

- **A (254 palavras):** Respondeu situação sem cobertura na base. Citou artigos 49 e 51 do CDC, sem URL na captura; informações gerais condicionais. A ausência de recusa não demonstra falsidade jurídica, mas falta de delimitação da base.
- **B (19 palavras em `resposta_simples`):** Status sem_informacao adequado; fonte/data vazias por ausência de registro. JSON válido; sem prova de orientação sobre multa, conforme escopo previsto.

## 5. Auditoria das datas: intervenção manual e fidelidade do modelo

O responsável pelo experimento **declarou que alterou manualmente a data para 19/11/2026** por ser o dia da execução. Os arquivos preservados permitem comparar a compilação original com os prompts individuais. **A data de execução de um teste não atualiza automaticamente a `data_verificacao` do registro jurídico**: esse campo identifica a data da conferência da fonte na base. Caso a conferência jurídica tenha ocorrido no dia 19, ela deve ser documentada e refletida no `data/base.json` em revisão específica.

| Caso | `prompts_10.md` preparado | Prompt individual arquivado | Resposta B | Leitura correta |
|---|---|---|---|---|
| T01 | 2026-11-16 | 2026-11-19 | 2026-11-19 | Alteração manual declarada; modelo copiou a versão individual |
| T02 | 2026-11-16 | 2026-11-16 | 2026-11-19 | **Modelo não copiou a data do registro fornecido** |
| T03 | 2026-11-16 | 2026-11-19 | 2026-11-19 | Alteração manual declarada; modelo copiou a versão individual |

**Consequência técnica:** `validar_saida_ia()` compara `data_verificacao` e `fonte` com o **registro real** recebido da base no momento da validação. Se `data/base.json` ainda tiver a data 16/11, as saídas `ok` com data 19/11 serão rejeitadas por divergência, independentemente de a resposta parecer correta. Se o registro oficial da base for atualizado após conferência legítima das fontes, a avaliação estrutural deverá usar esse registro atualizado. **O ZIP do experimento não inclui a base atual versionada**, portanto não foi possível comprovar a aceitação dessas três saídas pelo validador executado com a base do repositório.

A alteração manual em T01_B/T03_B é uma **diferença declarada nas condições de execução**, não um resultado inventado pelo modelo; esses dois casos podem integrar a comparação exploratória, desde que a ressalva permaneça visível. T02_B é uma falha de fidelidade ao próprio prompt. **Não é necessário apagar nem reescrever as dez respostas** para relatar essas conclusões. Para uma comparação estritamente idêntica aos prompts gerados pelo código, pode-se realizar rodada adicional opcional, identificada separadamente.

## 6. Comparação descritiva e interpretação

- **A:** 5/5 respostas em linguagem livre, com referências institucionais ou legais nomeadas, mas os links e metadados de citação não foram preservados nas cópias. Respondeu tanto FGTS quanto academia sem respeitar o escopo de cobertura definido para o assistente. Nos pontos jurídicos centrais conferidos, não se identificou erro material; a revisão não é exaustiva.
- **B:** 5/5 respostas em JSON válido, 5/5 campos `resposta_simples` com no máximo 80 palavras e 2/2 abstenções adequadas nas perguntas sem registro. Em T01_B e T03_B, a resposta reproduziu o valor do **prompt individual editado pelo responsável**; em T02_B, o modelo devolveu uma data diferente daquela contida no prompt individual. Entre os três casos B com status `ok`, **2/3 copiaram a data do prompt individual**.
- **Interpretação:** B demonstrou melhor controle de escopo e formato nesta amostra, porém a validade sintática não garante fidelidade semântica ou de metadados. A intervenção manual do operador limita a comparabilidade estrita entre versão gerada automaticamente e versão efetivamente arquivada. A vantagem observada não deve ser generalizada a outros modelos, perguntas ou execuções.

## 7. Limites de `validar_saida_ia()`

A função de `src/prompts.py` verifica se o retorno é um objeto JSON, se o `status` é `ok` e se `fonte` e `data_verificacao` correspondem ao registro. Ela **não** verifica o limite de 80 palavras, a presença/tipo de todos os demais campos, se `resposta_simples` e `frase_pronta` são semanticamente fiéis, a atualidade jurídica, nem se a busca encontrou o registro certo. Uma resposta formalmente aceita ainda pode conter informação inventada. A saída `sem_informacao` retorna `False` por desenho para não ser mostrada como resposta pronta; isso é uma **abstenção apropriada**, não um JSON inválido.

Outros limites: amostra exploratória de cinco perguntas, execução única por variante, um modelo, possíveis efeitos de configuração do chat não documentados, ausência de tempos/temperatura/seed, respostas copiadas sem links clicáveis de citações e a alteração manual declarada das datas nos prompts individuais T01_B/T03_B.

## 8. Referências públicas para conferência dos pontos essenciais

- [Procon-SP — gorjeta facultativa](https://www.procon.sp.gov.br/dia-da-pizza-procon-sp-orienta-consumidores-sobre-direitos-ao-consumir-em-pizzarias-e-no-delivery/)
- [ANAC — Resolução nº 813/2026 e vigência](https://www.anac.gov.br/assuntos/legislacao/legislacao-1/resolucoes/2026/resolucao-813)
- [Procon-SP — novas regras da ANAC](https://www.procon.sp.gov.br/procon-sp-alerta-consumidores-sobre-novas-regras-da-anac/)
- [Banco Central — prazo e finalidade do MED](https://www.bcb.gov.br/meubc/faqs/p/o-que-e-e-como-funciona-o-mecanismo-especial-de-devolucao-med)
- [Banco Central — análise do MED](https://www.bcb.gov.br/meubc/faqs/p/vitima-fez-um-pix-e-caiu-em-um-golpe)
- [FGTS — saque na dispensa sem justa causa](https://www.fgts.gov.br/Paginas/subpaginas/saque-dispensa.aspx)
- [CDC — arts. 49 e 51](https://www.planalto.gov.br/ccivil_03/leis/l8078compilado.htm)

As fontes foram consultadas para a análise dos pontos centrais; não se trata de revisão jurídica exaustiva de todas as afirmações. A consulta externa **não substitui a fonte de entrada do Prompt B** na avaliação de fidelidade.

## 9. Evidências inspecionáveis, estado e encaminhamento

- **Dez respostas integrais:** `data/ia01/respostas/IA-T01_A.txt` até `data/ia01/respostas/IA-T05_B.txt` (arquivos preservados como recebidos).
- **Prompts realmente arquivados:** `data/ia01/prompts/`; compilação da preparação em `data/ia01/prompts_10.md`. O manifesto documenta modelo, plataforma, data e commit, além dos hashes de arquivos do projeto na preparação.
- **Comparação preenchida:** tabela em `docs/prompts.md`; observações e juízos em `data/ia01/avaliacao_manual.csv`; métricas, status, datas e hashes SHA-256 em `data/ia01/auditoria_metricas.json`.
- **Uso de IA e limites:** `docs/uso_ia.md`; este relatório documenta expectativa vs. resultado e descreve o validador.
- **Pendências não impeditivas para abrir PR em revisão:** comprovação externa das dez conversas independentes não incluída no ZIP; links completos das citações não preservados; atualização de `data_verificacao` na base só deve ocorrer mediante revalidação documental real. Reexecução estrita dos prompts originais é **melhoria opcional**, não foi falsamente tratada como concluída.

**Conclusão de entrega:** os três itens operacionais do backlog IA-01 possuem evidências documentais e são aptos à **revisão via PR**. A aprovação final e o merge dependem do responsável pela integração e da aceitação destas limitações.
