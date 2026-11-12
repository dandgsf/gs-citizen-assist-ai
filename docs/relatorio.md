# Citizen Assist AI
### Relatório técnico — Global Solution 2026.2 (CitizenTech · Citizen Assist AI)
**FIAP — Ciência da Computação**

| Integrante | GitHub | Matrícula |
|---|---|---|
| Alexandre Niewelt | [@QTAlox](https://github.com/QTAlox) | RM 570614 |
| Danilo Fernandes | [@dandgsf](https://github.com/dandgsf) | RM 570057 |
| Renato Nascimento | [@renascience](https://github.com/renascience) | RM 570266 |
| Renato Valle | [@renatolvalle](https://github.com/renatolvalle) | RM 572352 |

---

## 1. Problema

Direitos básicos do consumidor são desrespeitados todos os dias porque a pessoa não sabe, **na hora**, o que pode exigir. Exemplos: pagar no caixa mais do que dizia a prateleira, pagar os 10% do garçom achando que é obrigatório, aceitar multa por perder a comanda, perder o prazo de 7 dias para devolver uma compra on-line, demorar a contestar um Pix de golpe. A informação existe, mas está espalhada em leis, resoluções de agências (ANEEL, Anatel, ANAC) e regulamentos do Banco Central, escrita em linguagem técnica e longe do momento em que a pessoa precisa agir.

## 2. Público

Pessoas de todas as idades em situações cotidianas de consumo, sem formação jurídica: idosos (passagem interestadual gratuita, golpe do "falso parente"), jovens (meia-entrada, balada, compras on-line), famílias (conta de luz, telefone, internet) e viajantes (atraso de voo).

## 3. Solução

Assistente em Python, interface textual, executado com `python src/sistema.py`. A pessoa escreve a situação com as próprias palavras e recebe: o direito em linguagem simples, uma **frase pronta para mostrar ou falar** (citando a norma), os passos, onde reclamar, a **fonte oficial com data de verificação** e o aviso de que não é canal oficial. Se não houver informação confiável, o sistema avisa em vez de inventar.

## 4. Arquitetura

```
 entrada (texto livre ou menu)
        │
        ▼
 privacidade.py ── mascara CPF, telefone, e-mail, cartão
        │
        ▼
 texto.py ──────── normaliza · sinônimos · stopwords · radical
        │
        ▼
 busca.py ──────── palavras-chave | TF-IDF | híbrida  →  regra de decisão
        │            (RESPOSTA, AMBIGUA, SEM_RESPOSTA, FORA_DO_TEMA, VAZIA, INVALIDA)
        ▼
 sistema.py ────── exibe resposta + fonte + aviso; navegação no grafo (r1, r2…);
        │            checagem de condições (condicoes.py: lógica de 3 valores + De Morgan)
        ▼
 base_conhecimento.py ── lê e valida data/base.json e data/sinonimos.json
```

Estruturas de dados: dicionário `id → registro`; hierarquia `tema → [ids]`; **grafo não direcionado** de assuntos relacionados (lista de adjacência), com BFS para o menor caminho entre dois assuntos; listas de tuplas `(nota, id)` no ranking; `Counter` no TF-IDF.

## 5. Fontes e base de conhecimento

23 registros em 5 temas, com referência, link e data cadastrada de verificação (11/11/2026). A base reúne referências ao Código de Defesa do Consumidor, leis, resoluções de agências, regulamento do Pix, súmulas e orientações de entidades de defesa do consumidor. O cadastro dessas referências não comprova a revisão humana do conteúdo.

**Atualidade:** as fontes precisam de revisão humana contra as páginas oficiais. O aviso de idade do registro ajuda a organizar essa revisão, mas não verifica alterações nas normas nem a fidelidade das orientações.

A base é editável sem alterar o código. A leitura valida campos obrigatórios, formato de data, temas, ids repetidos e relacionados inexistentes, e avisa quando um registro passa de 180 dias sem verificação.

## 6. Estratégias de busca e de prompt

**Busca.** Três estratégias implementadas e comparadas: (1) **palavras-chave e frases-chave**, com penalidade para palavras sem correspondência; (2) **TF-IDF com similaridade do cosseno** em Python puro, em que palavras desconhecidas recebem o peso máximo de IDF para não inflar notas; (3) **híbrida** (média). Para **múltiplas correspondências**, se o 2º colocado tiver pelo menos 85% da nota do 1º, ou se a pergunta for uma única palavra presente em vários registros, o sistema mostra até 3 opções e pergunta qual é. Os limiares foram **calibrados** no conjunto de teste, no ponto médio entre a menor nota correta e a maior nota de perguntas sem resposta.

**Prompts.** Modelo A (direto, sem base) × Modelo B (ancorado no registro recuperado, regras de recusa e saída JSON), em uma **cadeia proposta** de 3 etapas: classificar → redigir → validar. O programa não chama IA generativa. O gerador de prompts e o validador existem separadamente: o validador aceita a saída somente se o JSON for válido, `status = ok` e fonte e data coincidirem com o registro. Essas verificações não comprovam fidelidade semântica. Há 5 testes do validador; a comparação experimental dos modelos permanece sem resultados registrados. Detalhes em [Estratégias de prompt](prompts.md).

**Lógica booleana.** Três situações têm checagem "isso vale para mim?" com respostas sim/não/não sei (lógica de Kleene). Regras `todas` (E) e `alguma` (OU). Quando o resultado é negativo, De Morgan identifica qual condição falhou.

## 7. Resultados dos testes

Plano: **40 perguntas de teste** (12 diretas, 16 reformulações informais, 5 fora do tema, 7 situações-limite: vazia, inválida, ambígua, sem resposta confiável) e **15 perguntas de validação** inéditas, escritas após a calibração e não usadas para ajustes. Cada consulta registra esperado, obtido, acerto/erro e tempo (média de 5 execuções). Detalhes completos em `docs/resultados_testes.md`.

| Estratégia | Acerto teste | Acerto validação | Erros perigosos | Tempo médio |
|---|---|---|---|---|
| Palavras-chave | 97,5% | 73,3% | 1 | < 0,1 ms |
| TF-IDF | 95,0% | 60,0% | 1 | < 0,1 ms |
| Híbrida (padrão) | 97,5% | 73,3% | 1 | < 0,2 ms |

**Indicadores:** taxa de acerto, tempo médio de consulta e **taxa de erro perigoso** (orientação errada dada com confiança). Na híbrida, 4 dos 5 erros foram *seguros*: o sistema não respondeu ou pediu esclarecimento. Também passaram os **12 testes de robustez**: arquivo ausente, vazio, JSON inválido, sem registros, registro incompleto, relacionado inexistente, data inválida e 5 cenários do validador de IA.

**Análise.** A diferença entre teste (97,5%) e validação (73,3%) indica que o vocabulário ficou ajustado às perguntas usadas na calibração. É o comportamento esperado de um sistema baseado em palavras, e por isso ele foi medido separadamente. Os erros de validação vêm de palavras que a base não conhece ("queimou", "falso neto", "8,99"). O único erro perigoso foi "a academia não quer cancelar meu plano", respondido com a regra de telecomunicações.

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
3. **Busca por palavras:** o radical por prefixo e a lista de sinônimos não entendem sentido. Perguntas com vocabulário novo caem em "sem resposta" (validação: 73,3%).
4. **Erro perigoso residual:** assunto parecido com outro setor (academia × telecom). *Melhoria:* checagem de "entidade" (quem é o fornecedor) antes de responder.
5. **Atualização das fontes:** as normas e orientações precisam de revisão humana. *Melhoria:* revisão periódica guiada pelo aviso de 180 dias.
6. *Melhoria de alcance:* levar o mesmo núcleo ao **WhatsApp**, canal usado por pessoas de todas as idades.

## 10. Impacto social

O Citizen Assist AI busca facilitar o acesso à informação de consumo (ODS 10), aos canais oficiais de reclamação (conexão complementar com ODS 16) e a orientações sobre serviços urbanos essenciais (ODS 11). A frase pronta pretende ajudar a pessoa a comunicar sua solicitação. Esse impacto ainda precisa ser avaliado com usuários; o formulário de usabilidade não contém resultados.
