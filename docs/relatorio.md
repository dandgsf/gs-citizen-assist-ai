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

**Busca.** Três estratégias implementadas e comparadas: (1) **palavras-chave e frases-chave**, com penalidade para palavras sem correspondência; (2) **TF-IDF com similaridade do cosseno** em Python puro, em que palavras desconhecidas recebem o peso máximo de IDF para não inflar notas; (3) **híbrida** (média). Para **múltiplas correspondências**, se o 2º colocado tiver pelo menos 85% da nota do 1º, ou se a pergunta for uma única palavra presente em vários registros, o sistema mostra até 3 opções e pergunta qual é. Os limiares foram **calibrados** no conjunto de teste, no ponto médio entre a menor nota correta e a maior nota de perguntas sem resposta. Adicionalmente, registros regulados por setor específico (`DB20`, telecomunicações/Anatel) passam por **checagem de contexto setorial** (`tem_servico_telecom` em `src/busca.py`) aplicada **antes** das decisões de ambiguidade e resposta, distinguindo o objeto/prestadora do contrato de saudações iniciais (`"oi, ..."`) e indicações de canal digital (`"pela internet"`, `"online"`), além de preservar consultas legítimas com menção incidental a outros contextos (como `"faculdade"` quando a operadora é explícita).

**Prompts.** Modelo A (direto, sem base) × Modelo B (ancorado no registro recuperado, regras de recusa e saída JSON), em uma **cadeia proposta** de 3 etapas: classificar → redigir → validar. O programa não chama IA generativa. O gerador de prompts e o validador existem separadamente: o validador aceita a saída somente se o JSON for válido, `status = ok` e fonte e data coincidirem com o registro. Essas verificações não comprovam fidelidade semântica. Há 5 testes do validador; a comparação experimental dos modelos permanece sem resultados registrados. Detalhes em [Estratégias de prompt](prompts.md).

**Lógica booleana.** Três situações têm checagem "isso vale para mim?" com respostas sim/não/não sei (lógica de Kleene). Regras `todas` (E) e `alguma` (OU). Quando o resultado é negativo, De Morgan identifica qual condição falhou.

## 7. Resultados dos testes

Plano: **60 perguntas de teste e regressão** (12 diretas, 16 reformulações informais, 5 fora do tema, 7 situações-limite e 20 casos de regressão setorial/ambiguidade `T41`–`T60`) e **19 perguntas no arquivo de validação** (`data/perguntas_validacao.json`), com **17 perguntas reservadas** e **2 regressões conhecidas** (`V15` e `V17`) que orientaram correções. Cada consulta registra esperado, obtido, candidatos exibidos, acerto/erro e tempo (média de 5 execuções). Detalhes completos em `docs/resultados_testes.md`.

| Estratégia | Acerto (teste + regressão) | Acerto (validação inédita) | Regressões `V15` e `V17` | Erros perigosos (corpus avaliado) | Tempo médio |
|---|---|---|---|---|---|
| Palavras-chave | 98,3% (59/60) | 82,4% (14/17) | 2/2 | 0 | < 0,1 ms |
| TF-IDF | 96,7% (58/60) | 70,6% (12/17) | 2/2 | 0 | < 0,3 ms |
| Híbrida (padrão) | 98,3% (59/60) | 82,4% (14/17) | 2/2 | 0 | < 0,3 ms |

**Indicadores:** taxa de acerto, tempo médio de consulta e **taxa de erro perigoso** (orientação errada ou opção explicitamente proibida oferecida ao usuário no corpus avaliado; não garante ausência de falhas fora dele). Na estratégia híbrida, os 4 erros restantes (1 no teste e 3 na validação reservada) foram *seguros*: o sistema não respondeu ou pediu esclarecimento sem oferecer candidatos proibidos. Também passaram os **14 testes de robustez**: 7 de leitura da base (arquivo ausente, vazio, JSON quebrado, sem registros, registro incompleto, relacionado inexistente, data inválida), 5 cenários do validador de IA e 2 verificações controladas da classificação de erro perigoso em `AMBIGUA` e `RESPOSTA`.

**Análise.** As três estratégias acertaram as 20 regressões setoriais (T41–T60), V15 e V17. Na base do PR, T49 e T50 contavam como acertos ao exibir DB07 antes da confirmação. Agora a CLI pede o contexto e só apresenta a orientação após duas respostas afirmativas sobre o local e o prazo da contratação. T52 e T55 cobrem o celular usado como canal, T53 recupera a internet contratada como “net”, T54 preserva uma compra com contexto e T56 cobre o cancelamento de curso sem detalhes. T57–T60 comparam a academia e a internet contratada nos canais da Vivo. Quando a pessoa informa apenas o canal, a CLI pergunta qual serviço deseja cancelar. Em V17, a busca reconhece “banda larga” como uma expressão e recupera DB20 para o encerramento do contrato. No commit `45bff7e`, palavras-chave e híbrida se abstinham e TF-IDF indicava troca de produto (DB04). Das 237 combinações de pergunta e estratégia, somente as três linhas de V17 mudaram nos campos funcionais. Nas mesmas 17 perguntas reservadas, os acertos antes e depois foram 14 para palavras-chave e híbrida e 12 para TF-IDF.

## 8. Teste de usabilidade

Em 17/11/2026, um participante anonimizado (P01) realizou quatro tarefas no Terminal do macOS. A ficha registra conclusão sem ajuda nas quatro tarefas, com tempo médio de 2 min 05 s. P01 identificou a fonte em duas das três tarefas em que isso se aplicava e avaliou a facilidade geral em 4/5.

| Tarefa | Registro da sessão |
|---|---|
| Taxa de serviço de 10% | Concluiu em 1 min 34 s e identificou a fonte. |
| Golpe no Pix | Concluiu em 1 min 56 s. A fonte ficou sem identificação. |
| Verificação de meia-entrada | Concluiu em 1 min 48 s e identificou a fonte. |
| Consulta fora do escopo, sobre aluguel de carro na Islândia | Conclusão sem ajuda registrada em 3 min 02 s. A ficha original não documentou a mensagem nem o percurso de continuidade. Posteriormente, o observador confirmou que P01 digitou espontaneamente `1` para consultar os tópicos; uma reprodução técnica separada documentou a resposta do sistema. |

O participante relatou excesso de informação no menu e dificuldade com a proximidade dos textos e com caracteres especiais. As propostas incluem espaçar as seções e dar mais destaque à fonte. Em uma sessão separada, o avaliador registrou sete verificações de teclado como funcionais. Oito verificações com VoiceOver foram classificadas pelo avaliador, seis com ressalvas. Os trechos anunciados, as releituras e a comparação entre os modos ainda precisam de registro por caso. O modo efetivo e o SHA da sessão com P01 não foram registrados. A amostra descreve essa sessão.

[Registro do participante](ux01c_teste_participante.md) · [Validação de acessibilidade](ux01b_validacao_acessibilidade.md) · [Consolidado de usabilidade](ux01d_relatorio_usabilidade.md)

## 9. Limitações e melhorias

1. **Cobertura limitada:** 23 situações de consumo. Não cobre trabalho, família, saúde, previdência ou crimes; nesses casos, indica a Defensoria Pública.
2. **Regras locais:** fila de banco, consumação mínima em algumas leis estaduais e gratuidades municipais variam por cidade e estado e não são detalhadas.
3. **Busca por palavras:** o radical por prefixo e a lista de sinônimos não entendem sentido. Perguntas com vocabulário novo caem em "sem resposta" (validação inédita: 77,8%).
4. **Checagem setorial.** A busca depende de vocabulário e contexto explícitos. Os testes cobrem a diferença entre o serviço contratado e o canal de contato, inclusive para banda larga. Formulações fora do vocabulário avaliado ainda podem produzir abstenções ou respostas incorretas.
5. **Atualização das fontes:** as normas e orientações foram revisadas em 16/11/2026, mas exigem revisão humana periódica. *Melhoria:* revisão contínua guiada pelo aviso automático de 180 dias.
6. *Melhoria de alcance:* levar o mesmo núcleo ao **WhatsApp**, canal usado por pessoas de todas as idades.

## 10. Impacto social

O Citizen Assist AI busca facilitar o acesso à informação de consumo (ODS 10), aos canais oficiais de reclamação (conexão complementar com ODS 16) e a orientações sobre serviços urbanos essenciais (ODS 11). A frase pronta pretende ajudar a pessoa a comunicar sua solicitação. A sessão descrita na seção 8 oferece evidência inicial de usabilidade. O impacto social permanece como hipótese a avaliar com uma amostra maior.
