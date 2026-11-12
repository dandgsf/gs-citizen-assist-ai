# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href="https://www.fiap.com.br/">
  <img src="https://www.fiap.com.br/svg/fiap.svg"
       alt="FIAP - Faculdade de Informática e Administração Paulista"
       width="40%">
</a>
</p>

<br>

# Citizen Assist AI

**Global Solution 2026.2 · CitizenTech · case Citizen Assist AI**

**Repositório:** [`dandgsf/gs-citizen-assist-ai`](https://github.com/dandgsf/gs-citizen-assist-ai) · **Versão atual:** `v0.1.1` (protótipo em desenvolvimento).

**Tópicos:** `fiap`, `global-solution`, `2nd-semester`, `citizentech`, `citizen-assist-ai`, `python`, `knowledge-base`.

O enunciado fornecido integra o projeto em [`instructions.md`](instructions.md), preservado integralmente. A nomenclatura segue o projeto anterior `gs-mission-control`; a análise está em [`docs/nomenclatura.md`](docs/nomenclatura.md).

**Entrega:** 19/11/2026, às 23h59; o enunciado não informa o fuso horário. Consulte os prazos e links oficiais da FIAP.

**Estado da entrega:** código e indicadores disponíveis; teste com usuário, comparação experimental de prompts, revisão humana das fontes, PDF final e vídeo ainda pendentes. Esta versão não representa a entrega acadêmica concluída.

## Grupo 9

## 👨‍🎓 Integrantes:
- [Danilo Gustavo da Silva Fernandes](https://github.com/dandgsf) — **RM570057** (conforme o projeto FIAP anterior).

## 👩‍🏫 Professores:

### Tutor(a)
- A confirmar para esta atividade.

### Coordenador(a)
- <a href="https://www.linkedin.com/in/andregodoichiovato/">André Godoi Chiovato</a>

---

## 📜 Descrição

### O problema

Todo dia alguém paga mais caro no caixa do que estava na prateleira, aceita os 10% do garçom achando que é obrigatório, paga multa por perder a comanda, desiste de devolver uma compra feita pela internet ou demora dias para contestar um Pix de golpe. Os direitos existem e estão em lei. Mas a informação está espalhada em códigos, resoluções de agências e sites diferentes, e **ninguém consulta uma lei na fila do caixa**.

### A solução

O **Citizen Assist AI** é um assistente textual em Python. A pessoa descreve a situação do jeito dela ("passaram as compras e o arroz deu mais caro do que tava na gôndola") e recebe, em segundos:

1. **o direito**, em linguagem simples;
2. **uma frase pronta para mostrar na tela ou falar** ao atendente, já citando a lei. Esse é o diferencial: a informação vira ação na hora;
3. **o passo a passo** e **onde reclamar** se não resolverem;
4. **a fonte oficial** com a **data em que foi verificada**;
5. **o aviso de limitação**: não é canal oficial e não substitui Procon, Defensoria ou advogado.

Quando a busca não encontra correspondência acima do limiar, o sistema **avisa que não tem informação suficiente**. A busca pode selecionar um registro incorreto; o caso conhecido está documentado nos resultados de testes.

### Público

Pessoas de **todas as idades** em situações de consumo do dia a dia: a pessoa idosa no ônibus interestadual ou no golpe do "falso parente", o jovem na balada ou com a meia-entrada, quem compra pela internet, quem tem a luz cortada numa sexta-feira. Não é preciso saber nenhum termo jurídico.

### Temas e situações (23 situações em 5 temas)

| Tema | Situações |
|---|---|
| Mercado e lojas | preço diferente na prateleira e no caixa · preço diferente no cartão/Pix/dinheiro · produto com defeito · troca por gosto ou tamanho · venda casada · fila e atendimento prioritário |
| Compras pela internet | arrependimento em 7 dias · entrega atrasada · produto ou serviço que não pedi |
| Bares, restaurantes e lazer | taxa de 10% · consumação mínima · perda de comanda · couvert não pedido · meia-entrada |
| Bancos, contas e telefone | golpe no Pix (MED) · cobrança indevida (devolução em dobro) · cobrador constrangendo · nome negativado · corte de luz · cancelar internet/celular/TV · telemarketing |
| Viagens e transporte | voo atrasado ou cancelado · passagem interestadual para pessoa idosa |

### ODS da ONU

- **ODS 10 – Redução das desigualdades:** a informação jurídica chega a quem não tem advogado.
- **ODS 16 – Paz, justiça e instituições eficazes (conexão complementar):** acesso à informação e aos canais de reclamação. ODS 10 e 11 fazem parte da lista indicada na divulgação CitizenTech transcrita nas instructions; ODS 16 é uma associação do projeto.
- **ODS 11 – Cidades sustentáveis:** serviços urbanos essenciais (energia, transporte, telecom).

---

## 🧱 Desenho da base, estruturas de dados e estratégia de busca

### Base de conhecimento (`data/base.json`)

Cada registro tem os 6 campos mínimos exigidos e campos extras:

| Campo | Uso |
|---|---|
| `identificador` | DB01…DB23 |
| `tema` | um dos 5 temas (hierarquia) |
| `pergunta_ou_palavras_chave` | `perguntas_exemplo` + `palavras_chave` (base da busca) |
| `orientacao_resumida` | o direito, em linguagem simples |
| `referencia` | `norma` + `url` oficial |
| `data_de_verificacao` | AAAA-MM-DD (o sistema avisa quando passa de 180 dias); data declarada no cadastro, sem verificação automática da fonte |
| `frase_pronta`, `passos`, `prazo`, `onde_reclamar`, `limitacoes` | a parte "acionável" da resposta |
| `relacionados` | arestas do grafo de assuntos |
| `condicoes` (opcional) | perguntas sim/não para checar se o direito vale para o caso |

**A base pode ser editada sem alterar o código.** Também é editável `data/sinonimos.json` (ex.: "gôndola" → "prateleira", "zap" → "whatsapp"). Na leitura, cada registro é **validado**: campo ausente, data em formato errado, tema inexistente ou id repetido fazem o registro ser ignorado com um aviso claro. Arquivo ausente, vazio ou JSON quebrado gera mensagem amigável, e o programa termina com código 1.

### Estruturas de dados (Fase 4)

- **Dicionário** `id → registro` (acesso O(1)).
- **Hierarquia** `tema → [ids]` (menu "ver temas").
- **Grafo não direcionado** de assuntos relacionados (lista de adjacência com `set`). Cada situação liga-se a 3 ou mais outras, e a pessoa navega por elas com `r1`, `r2`… Há também **busca em largura (BFS)** para achar o menor caminho entre dois assuntos (`Base.caminho`).
- **Listas e tuplas** no ranking `(nota, id)` e **`Counter`** no TF-IDF.

### Estratégia de busca (Fases 5 e 6)

Pipeline de texto: minúsculas → sem acentos → sinônimos → descarte de palavras vazias (mantendo "não" e "sem", que mudam o sentido) → **radical de 6 letras** ("cancelamento"/"cancelar" → "cancel").

Foram implementadas **3 estratégias**, comparadas com métricas:

1. **Palavras-chave/frases:** frase-chave inteira presente na pergunta vale mais. Palavras soltas do título e dos exemplos valem menos. Palavras da pergunta que não casam com nada penalizam a nota.
2. **TF-IDF + cosseno:** em Python puro. Palavras raras ("comanda") pesam mais que comuns. Palavras desconhecidas pela base também entram, com peso máximo, para não inflar notas.
3. **Híbrida (padrão):** média das duas.

**Regra de decisão** (o que fazer com as notas):

| Situação | Comportamento |
|---|---|
| entrada vazia | pede para escrever a dúvida, com exemplo |
| só símbolos / saudação | explica como perguntar |
| nenhuma palavra conhecida, ou assunto fora do escopo (trabalho, família, saúde…) | diz que não cobre e indica Defensoria ou advogado |
| melhor nota abaixo do limiar (calibrado) | **não chuta**: diz que não tem informação confiável |
| **múltiplas correspondências** (2º colocado ≥ 85% da nota do 1º) ou pergunta de uma palavra que aparece em vários registros ("cobrança", "cancelar") | mostra até 3 opções e pergunta qual é |
| caso contrário | responde com a situação de maior nota |

### Lógica booleana e De Morgan: "isso vale para mim?"

Três situações têm `condicoes` com perguntas de **sim / não / não sei**: arrependimento, meia-entrada e passagem para pessoa idosa. As regras são `todas` (E) ou `alguma` (OU), em **lógica de três valores**. Quando o resultado é negativo, o sistema usa **De Morgan** para explicar *por quê*:
- ¬(A ∧ B) = ¬A ∨ ¬B → basta uma falhar, e o sistema mostra qual.
- ¬(A ∨ B) = ¬A ∧ ¬B → nenhuma foi atendida.

Nenhuma resposta é guardada.

---

## 🛡️ Regras de resposta, prompts e limitações

- A resposta **sempre** sai da base, com fonte e data de verificação. O programa **não chama IA** para responder.
- **Dois modelos de prompt** documentados e comparados conceitualmente em [`docs/prompts.md`](docs/prompts.md): A (direto) × B (ancorado na base com saída JSON), numa **cadeia proposta** classificar → redigir → **validar**. O script gera os prompts, sem chamar um modelo. A comparação experimental ainda está pendente. O validador (`validar_saida_ia`) confere JSON, status, fonte e data; seus 5 testes passam, mas ele não verifica se o conteúdo da resposta é fiel à fonte.
- **Limitações conhecidas:** cobre 23 situações de consumo, e não temas trabalhistas, de família, de saúde ou criminais. Regras estaduais e municipais (fila de banco, consumação em algumas leis estaduais) não são detalhadas. O radical por prefixo pode confundir palavras com o mesmo início. A taxa de acerto em perguntas inéditas é menor que no conjunto de calibração (veja abaixo).

---

## 🧪 Plano de testes e resultados

`python src/avaliar.py` roda tudo e gera [`docs/resultados_testes.md`](docs/resultados_testes.md) e `data/resultados_testes.csv`. Cada pergunta registra: resposta esperada, resposta obtida, acerto/erro e tempo da consulta.

- **Conjunto de teste:** 40 perguntas (12 diretas, 16 reformulações informais, 5 fora do tema e 7 situações-limite: vazia, inválida, ambígua, sem resposta confiável). Usado para calibrar.
- **Conjunto de validação:** 15 perguntas **novas**, escritas depois da calibração e **não usadas para ajustes**.
- **12 testes de robustez:** arquivo ausente, vazio, JSON quebrado, registro inválido, relacionado inexistente, data errada, e 5 testes do validador de saída da IA.

Resultados reproduzidos em 12/11/2026, com Python 3.12.10:

| Estratégia | Acerto (teste) | Acerto (validação) | Erros perigosos* | Tempo médio |
|---|---|---|---|---|
| Palavras-chave | 97,5% (39/40) | 73,3% (11/15) | 1 | 0,034 ms |
| TF-IDF | 95,0% (38/40) | 60,0% (9/15) | 1 | 0,073 ms |
| **Híbrida (padrão)** | **97,5% (39/40)** | **73,3% (11/15)** | **1** | 0,086 ms |

\* *Erro perigoso* = orientação errada dada com confiança. *Erro seguro* = o sistema não respondeu ou pediu esclarecimento. Dos 5 erros da estratégia híbrida, **4 são seguros**: o sistema preferiu não responder. O único erro perigoso (V15, "a academia não quer cancelar meu plano") foi respondido com a regra de telecomunicações. Esse é o principal ponto de melhoria.

**Leitura honesta dos números:** a queda de 97,5% para 73,3% mostra que o vocabulário foi ajustado às perguntas de teste. Em perguntas inéditas, o sistema erra mais, mas erra **para o lado seguro**. A estratégia híbrida empatou com a de palavras-chave e ficou como padrão por combinar dois sinais independentes. A diferença de tempo é de frações de milissegundo.

**Robustez:** 12/12 situações tratadas na execução local. O avaliador também registra divergências de busca; portanto, esses 12 sucessos não significam que todas as respostas estão corretas. Tempos variam conforme o ambiente.

**Teste de usabilidade:** pendente com pelo menos 1 usuário real do público-alvo. A seção 8 de [`docs/relatorio.md`](docs/relatorio.md) contém o formulário ainda não preenchido. O PDF de 4 a 8 páginas exigido nas instructions também está pendente.

---

## 🔧 Como executar o código

**Pré-requisito:** Python 3.10 ou superior. **Nenhuma biblioteca externa** (só a biblioteca padrão).

```bash
git clone https://github.com/dandgsf/gs-citizen-assist-ai.git
cd gs-citizen-assist-ai
python src/sistema.py
```

Opções úteis:

```bash
python src/sistema.py --simples                 # sem emojis (terminais antigos do Windows)
python src/sistema.py --explicar                # mostra as notas e o tempo de cada busca
python src/sistema.py --estrategia palavras     # palavras | tfidf | hibrida
python src/sistema.py --pergunta "perdi a comanda"   # responde e encerra
python src/avaliar.py                           # roda testes e gera os indicadores
python src/prompts.py "sua pergunta"            # gera os prompts A e B preenchidos
```

Dentro do programa: escreva a dúvida ou use `1` (temas), `2` (como funciona e avisos), `3` (modo explicação), `m` (menu), `0` (sair). Depois de uma resposta: `r1`, `r2`… (assuntos relacionados) e `v` (verificar se vale para o seu caso).

---

## 💬 Exemplos de perguntas e respostas

**Pergunta:** `passaram as compras e o arroz deu mais caro do que tava na gondola`

```
⚖️  PREÇO DIFERENTE NA PRATELEIRA E NO CAIXA   (Mercado e lojas)
✅ O QUE VOCÊ PRECISA SABER
   Se o MESMO produto aparece com dois preços na loja (prateleira, etiqueta,
   cartaz ou leitor de preço) e no caixa sai mais caro, você paga o MENOR. [...]
🗣️  MOSTRE NA TELA OU FALE:
   “A Lei 10.962/2004, art. 5º, diz que, havendo divergência de preço para o
   mesmo produto, o consumidor paga o menor. Peço que registre pelo preço da
   prateleira.”
👣 O QUE FAZER
   1. Antes de pagar, tire uma foto da etiqueta ou do cartaz. [...]
📚 FONTE: Lei nº 10.962/2004, art. 5º — planalto.gov.br — Verificado em 11/11/2026.
⚠️  Orientação informativa e gratuita. NÃO é canal oficial do governo [...]
🔗 ASSUNTOS RELACIONADOS: [r1] Preço diferente no cartão… [r2] Venda casada… [r3] Cobrança indevida…
```

| Pergunta | O que o sistema faz |
|---|---|
| "o garçom botou os dez por cento sem me perguntar" | Responde **Taxa de serviço de 10%** (opcional) com a frase pronta para pedir a retirada |
| "mandei dinheiro pro golpista que se passou pelo meu filho no zap" | Busca a orientação cadastrada sobre **Golpe no Pix**, com referência e limitações |
| "cobrança" | **Ambígua:** pergunta se é cobrança indevida, cobrador constrangendo ou preço no cartão |
| "fui demitido, quanto recebo de FGTS?" | **Fora do escopo:** explica que não cobre e indica Defensoria ou advogado |
| "a loja não quis me dar nota fiscal" | **Sem resposta confiável:** não chuta e indica Procon ou consumidor.gov.br |
| "meu CPF é 123.456.789-00 e cortaram minha luz na sexta" | Avisa que não precisa de CPF, **remove o dado** e responde **Corte de luz** |

---

## ♿ Clareza, acessibilidade, privacidade e caráter não oficial

- **Clareza:** linguagem simples, sem juridiquês. Cada resposta tem a mesma estrutura (direito → frase pronta → passos → onde reclamar → fonte → aviso).
- **Acessibilidade:** normaliza acentos e alguns termos informais ("tava", "gondola", "zap"). O modo `--simples` substitui emojis, e o texto quebra em linhas de 78 caracteres. A interface é textual; uso com leitores de tela ainda precisa de validação com usuários.
- **Privacidade:** a interface não pede dados pessoais nem persiste as consultas. Padrões reconhecidos de CPF, telefone, e-mail e cartão são mascarados antes da busca (`src/privacidade.py`); essa detecção não garante remover todos os dados sensíveis. Não informe dados pessoais nos argumentos da linha de comando, pois eles podem permanecer no histórico do terminal.
- **Não oficial:** o aviso aparece na abertura e em **todas** as respostas. O sistema nunca se apresenta como canal do governo e sempre aponta os canais oficiais (Procon, consumidor.gov.br, ANEEL, Anatel, ANAC, ANTT, Banco Central).

**Fontes jurídicas:** as datas da base foram herdadas do material inicial. O checklist de revisão humana em [`docs/uso_ia.md`](docs/uso_ia.md) permanece aberto; os testes verificam o comportamento do software, não a vigência ou a exatidão jurídica das orientações.

---

## 📁 Estrutura de pastas

```
gs-citizen-assist-ai/
├── README.md
├── instructions.md           # enunciado fornecido, preservado integralmente
├── CHANGELOG.md              # histórico de versões
├── src/
│   ├── sistema.py            # programa principal (interface textual)
│   ├── base_conhecimento.py  # leitura, validação, hierarquia e grafo
│   ├── busca.py              # 3 estratégias de busca + regra de decisão
│   ├── texto.py              # normalização, sinônimos e radicais
│   ├── condicoes.py          # lógica de 3 valores + De Morgan
│   ├── privacidade.py        # mascaramento de dados pessoais
│   ├── prompts.py            # prompts A e B + validação da saída da IA
│   └── avaliar.py            # plano de testes e indicadores
├── data/
│   ├── base.json             # 23 orientações com fontes (revisão humana pendente)
│   ├── sinonimos.json        # vocabulário popular → base (editável)
│   ├── perguntas_teste.json  # 40 perguntas de teste
│   ├── perguntas_validacao.json  # 15 perguntas inéditas
│   └── resultados_testes.csv # gerado pelo avaliar.py
└── docs/
    ├── relatorio.md          # rascunho; PDF final de 4 a 8 páginas pendente
    ├── nomenclatura.md       # análise do padrão dos repositórios FIAP
    ├── resultados_testes.md  # gerado pelo avaliar.py
    ├── prompts.md            # comparação dos 2 modelos de prompt
    ├── uso_ia.md             # uso de IA no projeto
    └── link_video.txt        # aguardando link do vídeo
```

## 📎 Links e Observações

### 🔗 Links do Projeto

* **Vídeo de apresentação:** pendente. Após gravar e publicar no YouTube como **Não Listado**, inserir o link em [`docs/link_video.txt`](docs/link_video.txt) e neste README.
* **Enunciado:** [`instructions.md`](instructions.md).
* **Relatório em elaboração:** [`docs/relatorio.md`](docs/relatorio.md).
* **Uso de IA:** [`docs/uso_ia.md`](docs/uso_ia.md).

### Entrega no FIAP ON

Enviar pela [página oficial da atividade](https://on.fiap.com.br/mod/assign/view.php?id=684386) **um único arquivo `.txt` contendo somente dois links**, um por linha: o repositório GitHub público da equipe e o vídeo no YouTube como Não Listado. `docs/link_video.txt` é um artefato do repositório e não substitui esse arquivo de submissão.

### Pendências para concluir a entrega

- [ ] Tornar o repositório público antes da submissão, após autorização do integrante.

- [ ] Realizar e registrar o teste de usabilidade com pelo menos 1 usuário.
- [ ] Executar o experimento de comparação dos prompts e preencher a tabela.
- [ ] Concluir a revisão humana das 23 fontes e das orientações.
- [ ] Gerar e conferir `docs/relatorio.pdf` com 4 a 8 páginas.
- [ ] Publicar o vídeo como Não Listado e preencher seus links.
- [ ] Preparar o `.txt` com somente os dois links e enviar no FIAP ON.

### 🧠 Decisões Técnicas

> **Python puro, sem dependências:** roda em qualquer computador do laboratório com `python src/sistema.py`, sem instalar nada.
> **Busca determinística em vez de IA generativa no núcleo:** o requisito central do case é não inventar. Toda resposta tem fonte e data. A IA fica como camada opcional e validada.
> **Duas medições separadas (teste × validação):** evita apresentar um número inflado pela calibração.
> **Erro seguro > erro perigoso:** os limiares foram calibrados para o sistema preferir "não sei" a uma orientação errada.

### 📢 Observações Gerais

* **Participação na competição:** a confirmar pelo integrante; este repositório não registra aceite.

---

## ✅ Conclusões

O Citizen Assist AI mostra que um assistente cidadão útil não precisa de API paga nem de IA generativa no núcleo. Precisa de **informação verificada, bem organizada e entregue no momento em que a pessoa precisa agir**. A frase pronta transforma o direito em ação na fila do caixa. A fonte com data de verificação dá confiança. O "não sei" honesto evita causar dano.

Os testes mostram alta precisão nas situações cobertas e uma queda esperada em perguntas inéditas, quase sempre para o lado seguro. Próximos passos:
1. ampliar a base e o vocabulário com perguntas reais coletadas no teste de usabilidade;
2. reduzir o erro perigoso com a checagem de "entidade" (ex.: academia ≠ operadora de telecom);
3. levar o assistente ao **WhatsApp**, onde estão pessoas de todas as idades, reaproveitando o mesmo núcleo;
4. revisão periódica automática das fontes com mais de 180 dias.

---

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/fiap-tutoria/FIAP-PORTFOLIO-AI">TEMPLATE - FIAP PORTFÓLIO AI</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">FIAP</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>
