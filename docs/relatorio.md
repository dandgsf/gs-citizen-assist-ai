# Citizen Assist AI

### Relatório técnico — Global Solution 2026.2 (CitizenTech · Citizen Assist AI)

**FIAP — Ciência da Computação**

| Integrante | GitHub | Matrícula |
|---|---|---|
| Alexandre Niewelt | [@QTAlox](https://github.com/QTAlox) | RM 570614 |
| Danilo Fernandes | [@dandgsf](https://github.com/dandgsf) | RM 570057 |
| Renato Nascimento | [@renascience](https://github.com/renascience) | RM 570266 |
| Renato Valle | [@renatolvalle](https://github.com/renatolvalle) | RM 572352 |

## 1. Problema

Direitos básicos do consumidor são desrespeitados todos os dias porque a pessoa não sabe, **na hora**, o que pode exigir. Exemplos: pagar no caixa mais do que dizia a prateleira, pagar os 10% do garçom achando que é obrigatório, aceitar multa por perder a comanda, perder o prazo de 7 dias para devolver uma compra on-line, demorar a contestar um Pix de golpe. A informação existe, mas está espalhada em leis, resoluções de agências (ANEEL, Anatel, ANAC) e regulamentos do Banco Central, escrita em linguagem técnica e longe do momento em que a pessoa precisa agir.

## 2. Público

Pessoas de todas as idades em situações cotidianas de consumo, sem formação jurídica: idosos (passagem interestadual gratuita, golpe do "falso parente"), jovens (meia-entrada, balada, compras on-line), famílias (conta de luz, telefone, internet) e viajantes (atraso de voo).

## 3. Solução

Assistente em Python, interface textual, executado com `python src/sistema.py`. A pessoa escreve a situação com as próprias palavras e recebe: o direito em linguagem simples, uma **frase pronta para mostrar ou falar** (citando a norma), os passos, onde reclamar, a **fonte oficial com data de verificação** e o aviso de que não é canal oficial. Se não houver informação confiável, o sistema avisa em vez de inventar.

## 4. Arquitetura

```text
 entrada (texto livre ou menu)
        │
        ▼
 privacidade.py ── mascara CPF, telefone, e-mail, cartão
        │
        ▼
 texto.py ──────── normaliza · sinônimos · stopwords · radical
        │
        ▼
 busca.py ──────── palavras-chave | TF-IDF | híbrida  →  contexto setorial + regra de decisão
        │            (RESPOSTA, AMBIGUA, SEM_RESPOSTA, FORA_DO_TEMA, VAZIA, INVALIDA)
        ▼
 sistema.py ────── exibe resposta + fonte + aviso; navegação no grafo (r1, r2…);
        │            checagem de condições (condicoes.py: lógica de 3 valores + De Morgan)
        ▼
 base_conhecimento.py ── lê e valida data/base.json e data/sinonimos.json
```

Estruturas de dados: dicionário `id → registro`; hierarquia `tema → [ids]`; **grafo não direcionado** de assuntos relacionados (lista de adjacência), com BFS para o menor caminho entre dois assuntos; listas de tuplas `(nota, id)` no ranking; `Counter` no TF-IDF.

## 5. Fontes e base de conhecimento

23 registros em 5 temas, com referência, link e revisão humana concluída em 16/11/2026 contra as normas oficiais. A base reúne referências ao Código de Defesa do Consumidor, leis federais, resoluções de agências reguladoras (ANEEL, Anatel, ANAC), regulamento do Pix (BCB), súmulas do STJ e orientações do Idec e dos Procons.

A base é editável sem alterar o código (`data/base.json` e `data/sinonimos.json`). A leitura valida campos obrigatórios, formato de data (`AAAA-MM-DD`), temas, identificadores repetidos e relacionados inexistentes, e avisa quando um registro passa de 180 dias sem verificação.

### Registro de revisão humana das fontes (BAS-01 — 16/11/2026)

| ID | Tema | Norma oficial consultada | Data | Conclusão da revisão |
|---|---|---|---|---|
| DB01 | Mercado e lojas | Lei nº 10.962/2004, art. 5º | 16/11/2026 | Confirmado: prevalece o menor preço para o mesmo produto, ressalvado erro grosseiro. |
| DB02 | Mercado e lojas | Lei nº 13.455/2017; Lei nº 10.962/2004, art. 5º-A | 16/11/2026 | Confirmado: diferenciação por meio/prazo permitida mediante aviso prévio e visível. |
| DB03 | Mercado e lojas | CDC (Lei nº 8.078/1990), arts. 18 e 26 | 16/11/2026 | Confirmado: responsabilidade solidária, prazos de 30/90 dias e 30 dias para reparo. |
| DB04 | Mercado e lojas | CDC, arts. 30 e 49 | 16/11/2026 | Confirmado: troca em loja física sem defeito só obriga se ofertada; 7 dias vale fora da loja. |
| DB05 | Mercado e lojas | CDC, art. 39, inciso I | 16/11/2026 | Confirmado: vedação à venda casada e limite quantitativo sem justa causa. |
| DB06 | Mercado e lojas | Lei nº 10.048/2000, arts. 1º e 2º (Lei nº 14.626/2023) | 16/11/2026 | Confirmado: inclui TEA e doadores de sangue (120 dias); ressalva sobre leis locais em comércio. |
| DB07 | Compras pela internet | CDC, art. 49; Decreto nº 7.962/2013, art. 5º | 16/11/2026 | Confirmado: direito de arrependimento em 7 dias corridos e estorno no cartão. |
| DB08 | Compras pela internet | CDC, art. 35 | 16/11/2026 | Confirmado: alternativas ao consumidor em caso de descumprimento da oferta/prazo. |
| DB09 | Compras pela internet | CDC, art. 39, III e parágrafo único; Súmula 532 STJ | 16/11/2026 | Confirmado: equiparação a amostra grátis e vedação ao envio de cartão sem solicitação. |
| DB10 | Bares, restaurantes e lazer | Lei nº 13.419/2017; CDC, art. 6º, III | 16/11/2026 | Confirmado: gorjeta/taxa de serviço opcional com dever de informação clara. |
| DB11 | Bares, restaurantes e lazer | CDC, art. 39, I; orientação Idec/Procons | 16/11/2026 | Confirmado com ressalva: prática considerada abusiva; sinalizada variação em leis estaduais. |
| DB12 | Bares, restaurantes e lazer | CDC, art. 39, V; orientação Procon-SP/Idec | 16/11/2026 | Confirmado: ônus do controle de consumo é do fornecedor; multa arbitrária é abusiva. |
| DB13 | Bares, restaurantes e lazer | CDC, art. 39, III e parágrafo único; art. 6º, III | 16/11/2026 | Confirmado: couvert não pedido é amostra grátis; couvert artístico exige aviso prévio. |
| DB14 | Bares, restaurantes e lazer | Lei nº 12.933/2013; Lei nº 10.741/2003, art. 23 | 16/11/2026 | Confirmado: beneficiários, cota de 40% e exclusão de cursos livres. |
| DB15 | Bancos, contas e telefone | Regulamento do Pix – MED (Banco Central) | 16/11/2026 | Confirmado: prazo de até 80 dias para contestação por fraude/golpe e análise em 7 dias. |
| DB16 | Bancos, contas e telefone | CDC, art. 42, parágrafo único | 16/11/2026 | Confirmado: repetição do indébito em dobro sobre valor pago, salvo engano justificável. |
| DB17 | Bancos, contas e telefone | CDC, arts. 42 (caput) e 71 | 16/11/2026 | Confirmado: proibição de exposição ao ridículo, ameaça ou constrangimento na cobrança. |
| DB18 | Bancos, contas e telefone | CDC, art. 43, §2º; Súmulas 359 e 548 STJ | 16/11/2026 | Confirmado: comunicação prévia pelo órgão mantenedor e baixa em 5 dias úteis após quitação. |
| DB19 | Bancos, contas e telefone | Resolução Normativa ANEEL nº 1.000/2021 | 16/11/2026 | Confirmado: aviso prévio de 15 dias, horário útil (seg-qui) e religação em até 4h se indevido. |
| DB20 | Bancos, contas e telefone | Resolução Anatel nº 765/2023 (RGC), arts. 83 e 84 | 16/11/2026 | Corrigido e confirmado: incluída distinção entre efeito imediato com atendente (art. 83) e prazo de até 2 dias úteis no canal automático sem atendente, com cobrança pelos serviços usufruídos nesse período (art. 84, §1º). |
| DB21 | Bancos, contas e telefone | Plataforma Não Me Perturbe / Prefixo 0303 (Anatel) | 16/11/2026 | Confirmado: bloqueio em até 30 dias para telecom e consignado; ressalva para cobranças/fraudes. |
| DB22 | Viagens e transporte | Resolução ANAC nº 400/2016 (alt. Res. 813/2026 e 819/2026) | 16/11/2026 | Confirmado: assistência material (2h alimentação, 4h hospedagem) e atualização da Res. 813/2026. |
| DB23 | Viagens e transporte | Estatuto da Pessoa Idosa (Lei nº 10.741/2003), art. 40 | 16/11/2026 | Confirmado: 60+ anos, renda até 2 SM, 2 vagas gratuitas ou 50% de desconto no convencional. |

## 6. Estratégias de busca e de prompt

**Busca.** Três estratégias implementadas e comparadas: (1) **palavras-chave e frases-chave**, com penalidade para palavras sem correspondência; (2) **TF-IDF com similaridade do cosseno** em Python puro, em que palavras desconhecidas recebem o peso máximo de IDF para não inflar notas; (3) **híbrida** (média). Para **múltiplas correspondências**, se o 2º colocado tiver pelo menos 85% da nota do 1º, ou se a pergunta for uma única palavra presente em vários registros, o sistema mostra até 3 opções e pergunta qual é. Os limiares foram **calibrados** no conjunto de teste, no ponto médio entre a menor nota correta e a maior nota de perguntas sem resposta. Adicionalmente, registros regulados por setor específico (como `DB20`, telecomunicações/Anatel) passam por **checagem de contexto setorial** (`CONTEXTO_SETOR` e `_sinais_consulta` em `src/busca.py`) aplicada **antes** das decisões de ambiguidade e resposta, reconhecendo operadoras mesmo quando coincidem com stopwords (como `"oi"`) e preservando consultas legítimas com menção incidental a outros contextos (como `"faculdade"` quando a prestadora é explícita).

**Prompts.** Modelo A (direto, sem base) × Modelo B (ancorado no registro recuperado, regras de recusa e saída JSON), em uma **cadeia proposta** de 3 etapas: classificar → redigir → validar. O programa não chama IA generativa. O gerador de prompts e o validador existem separadamente: o validador aceita a saída somente se o JSON for válido, `status = ok` e fonte e data coincidirem com o registro. Essas verificações não comprovam fidelidade semântica. Há 5 testes do validador; a comparação experimental dos modelos permanece sem resultados registrados. Detalhes em [Estratégias de prompt](prompts.md).

**Lógica booleana.** Três situações têm checagem "isso vale para mim?" com respostas sim/não/não sei (lógica de Kleene). Regras `todas` (E) e `alguma` (OU). Quando o resultado é negativo, De Morgan identifica qual condição falhou.

## 7. Resultados dos testes

Plano: **47 perguntas de teste e regressão** (12 diretas, 16 reformulações informais, 5 fora do tema, 7 situações-limite e 7 casos de regressão setorial/ambiguidade) e **19 perguntas no arquivo de validação** (`data/perguntas_validacao.json`), separando explicitamente a **regressão conhecida `V15`** (1 caso que orientou a correção de `BUS-01`) das **18 perguntas de validação inédita** (14 originais + 4 novas perguntas reservadas após os ajustes). Cada consulta registra esperado, obtido, acerto/erro e tempo (média de 5 execuções). Detalhes completos em `docs/resultados_testes.md`.

| Estratégia | Acerto (teste + regressão) | Acerto (validação inédita) | Regressão `V15` | Erros perigosos (corpus avaliado) | Tempo médio |
|---|---|---|---|---|---|
| Palavras-chave | 97,9% (46/47) | 77,8% (14/18) | 1/1 | 0 | < 0,1 ms |
| TF-IDF | 95,7% (45/47) | 66,7% (12/18) | 1/1 | 1 | < 0,2 ms |
| Híbrida (padrão) | 97,9% (46/47) | 77,8% (14/18) | 1/1 | 0 | < 0,2 ms |

**Indicadores:** taxa de acerto, tempo médio de consulta e **taxa de erro perigoso** (orientação errada dada com confiança no corpus avaliado; não garante ausência de falhas fora dele). Na estratégia híbrida, todos os 5 erros restantes (1 no teste e 4 na validação inédita) foram *seguros*: o sistema não respondeu ou pediu esclarecimento. Também passaram os **12 testes de robustez**: arquivo ausente, vazio, JSON quebrado, sem registros, registro incompleto, relacionado inexistente, data inválida e 5 cenários do validador de IA.

**Análise.** A diferença entre teste/regressão (97,9%) e validação inédita (77,8%) reflete o comportamento esperado de um sistema lexical diante de vocabulário inédito ("queimou", "falso neto", "8,99"). Com a implementação da checagem de contexto setorial antes das decisões de ambiguidade e resposta (`BUS-01`), o erro na regressão conhecida `V15` foi corrigido e os 7 cenários de regressão (`T41`–`T47`) passaram integralmente: consultas de academia não recebem nem oferecem `DB20` nas opções de ambiguidade, enquanto consultas legítimas de telecomunicações (incluindo `"Oi"` e menção incidental a `"faculdade"` com operadora explícita) retornam `DB20`. Nas perguntas inéditas reservadas, o único erro em `V17` ("quero encerrar meu contrato de banda larga residencial") foi *seguro* (`SEM_RESPOSTA`), mantendo a integridade da validação sem calibragem retroativa.

## 8. Teste de usabilidade

> **Preencher após o teste com pelo menos 1 pessoa real do público-alvo.**

| Item | Registro |
|---|---|
| Participante (sem nome; apenas perfil) | ex.: mulher, 58 anos, usa celular, nunca usou terminal |
| Data e duração | |
| Tarefas pedidas | 1) descobrir se é obrigada a pagar os 10%; 2) achar o que fazer num golpe de Pix; 3) usar a checagem "v" da meia-entrada |
| Concluiu sem ajuda? | |
| Perguntas que digitou (texto exato) | |
| O sistema acertou? | |
| O que achou confuso | |
| Nota de 1 a 5 (facilidade / utilidade) | |
| Melhoria feita a partir do teste | |

## 9. Limitações e melhorias

1. **Cobertura limitada:** 23 situações de consumo. Não cobre trabalho, família, saúde, previdência ou crimes; nesses casos, indica a Defensoria Pública.
2. **Regras locais:** fila de banco, consumação mínima em algumas leis estaduais e gratuidades municipais variam por cidade e estado e não são detalhadas.
3. **Busca por palavras:** o radical por prefixo e a lista de sinônimos não entendem sentido. Perguntas com vocabulário novo caem em "sem resposta" (validação inédita: 77,8%).
4. **Checagem setorial explícita:** a validação de contexto setorial (`CONTEXTO_SETOR`) eliminou a confusão entre academia e telecomunicações no corpus avaliado, mas depende de termos explícitos do setor regulado; sinônimos não mapeados (como "encerrar" no lugar de "cancelar" em `V17`) levam o sistema a abster-se de forma segura (`SEM_RESPOSTA`). *Melhoria:* expandir o mapeamento de sinônimos e entidades setoriais.
5. **Atualização das fontes:** as normas e orientações foram revisadas em 16/11/2026, mas exigem revisão humana periódica. *Melhoria:* revisão contínua guiada pelo aviso automático de 180 dias.
6. *Melhoria de alcance:* levar o mesmo núcleo ao **WhatsApp**, canal usado por pessoas de todas as idades.

## 10. Impacto social

O Citizen Assist AI busca facilitar o acesso à informação de consumo (ODS 10), aos canais oficiais de reclamação (conexão complementar com ODS 16) e a orientações sobre serviços urbanos essenciais (ODS 11). A frase pronta pretende ajudar a pessoa a comunicar sua solicitação. Esse impacto ainda precisa ser avaliado com usuários; o formulário de usabilidade não contém resultados.
