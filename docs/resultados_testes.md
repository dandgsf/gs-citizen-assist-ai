# Resultados dos testes — Pode Isso?

Gerado automaticamente por `python src/avaliar.py` em 12/11/2026 12:51. 23 registros na base, 5 execuções por consulta (tempo = média).

- **Conjunto de teste** (`data/perguntas_teste.json`, 40 perguntas): usado para calibrar sinônimos, palavras-chave e limiares.
- **Conjunto de validação** (`data/perguntas_validacao.json`, 15 perguntas novas): escrito depois da calibração e **não** usado para ajustes. É a medida mais honesta do desempenho em perguntas inéditas.

## Comparação das estratégias de busca

| Estratégia | Acerto (teste) | Acerto (validação) | Erros perigosos (teste + validação) | Tempo médio (ms) | Tempo máximo (ms) |
|---|---|---|---|---|---|
| palavras | 39/40 (97.5%) | 11/15 (73.3%) | 1 | 0.034 | 0.047 |
| tfidf | 38/40 (95.0%) | 9/15 (60.0%) | 1 | 0.073 | 0.104 |
| hibrida **(padrão)** | 39/40 (97.5%) | 11/15 (73.3%) | 1 | 0.086 | 0.124 |

*Erro seguro*: o sistema não respondeu ou pediu esclarecimento (não induz ninguém a erro). *Erro perigoso*: deu uma orientação errada com confiança — é o tipo de erro que mais importa reduzir.

Empate em acerto e erros perigosos entre: **palavras, hibrida**. A diferença de tempo (frações de milissegundo) é imperceptível para quem usa.

## Taxa de acerto por categoria (conjunto de teste)

| Categoria | palavras | tfidf | hibrida |
|---|---|---|---|
| direta | 12/12 | 12/12 | 12/12 |
| reformulacao | 15/16 | 14/16 | 15/16 |
| fora | 5/5 | 5/5 | 5/5 |
| limite | 7/7 | 7/7 | 7/7 |

## Detalhe por pergunta — conjunto de teste (estratégia híbrida)

| ID | Categoria | Pergunta | Esperado | Obtido | Resultado | Tempo (ms) |
|---|---|---|---|---|---|---|
| T01 | direta | O preço da prateleira é diferente do preço no caixa | DB01 | DB01 | ✅ acerto | 0.091 |
| T02 | direta | A loja pode cobrar mais caro no cartão de crédito? | DB02 | DB02 | ✅ acerto | 0.091 |
| T03 | direta | Comprei uma geladeira e ela veio com defeito | DB03 | DB03 | ✅ acerto | 0.085 |
| T04 | direta | Me arrependi de uma compra pela internet, posso devolver? | DB07 | DB07 | ✅ acerto | 0.088 |
| T05 | direta | Sou obrigado a pagar a taxa de serviço de 10%? | DB10 | DB10 | ✅ acerto | 0.087 |
| T06 | direta | O bar cobra consumação mínima, pode? | DB11 | DB11 | ✅ acerto | 0.085 |
| T07 | direta | Caí em um golpe no Pix, como recupero o dinheiro? | DB15 | DB15 | ✅ acerto | 0.094 |
| T08 | direta | Meu nome foi negativado no Serasa sem aviso | DB18 | DB18 | ✅ acerto | 0.086 |
| T09 | direta | Como cancelar a internet da operadora? | DB20 | DB20 | ✅ acerto | 0.080 |
| T10 | direta | Meu voo foi cancelado, tenho direito a hotel? | DB22 | DB22 | ✅ acerto | 0.110 |
| T11 | direta | Quem tem direito a meia-entrada no cinema? | DB14 | DB14 | ✅ acerto | 0.083 |
| T12 | direta | Idoso tem passagem de ônibus interestadual gratuita? | DB23 | DB23 | ✅ acerto | 0.094 |
| T13 | reformulacao | passaram as compras e o arroz deu mais caro do que tava na gondola | DB01 | DB01 | ✅ acerto | 0.103 |
| T14 | reformulacao | o tênis que eu comprei rasgou e a loja falou pra eu me virar com a fábrica | DB03 | DB03 | ✅ acerto | 0.112 |
| T15 | reformulacao | ganhei uma blusa de presente mas ficou apertada, a loja tem que trocar? | DB04 | DB04 | ✅ acerto | 0.108 |
| T16 | reformulacao | o vendedor disse que o celular só sai se eu levar a garantia estendida junto | DB05 | DB05 | ✅ acerto | 0.115 |
| T17 | reformulacao | to gravida e o banco nao quis me atender na fila preferencial | DB06 | DB06 | ✅ acerto | 0.108 |
| T18 | reformulacao | fiz um pedido no app faz 20 dias e até agora nada de chegar | DB08 | AMBIGUA | ❌ erro | 0.097 |
| T19 | reformulacao | chegou um cartão de crédito em casa que eu nunca pedi | DB09 | DB09 | ✅ acerto | 0.097 |
| T20 | reformulacao | o garçom botou os dez por cento sem me perguntar | DB10 | DB10 | ✅ acerto | 0.100 |
| T21 | reformulacao | sumiu meu cartão de consumo na balada e querem me cobrar 300 reais | DB12 | DB12 | ✅ acerto | 0.113 |
| T22 | reformulacao | trouxeram pãozinho e manteiga na mesa sem eu pedir e cobraram | DB13 | DB13 | ✅ acerto | 0.103 |
| T23 | reformulacao | mandei dinheiro pro golpista que se passou pelo meu filho no zap | DB15 | DB15 | ✅ acerto | 0.101 |
| T24 | reformulacao | a empresa me cobrou duas vezes a mesma fatura e eu paguei as duas | DB16 | DB16 | ✅ acerto | 0.109 |
| T25 | reformulacao | a assessoria de cobrança liga pros meus colegas de trabalho falando da minha dívida | DB17 | DB17 | ✅ acerto | 0.116 |
| T26 | reformulacao | a enel cortou a energia lá de casa num sábado | DB19 | DB19 | ✅ acerto | 0.099 |
| T27 | reformulacao | não aguento mais o banco me ligando pra oferecer consignado | DB21 | DB21 | ✅ acerto | 0.101 |
| T28 | reformulacao | meu pai tem 63 anos e quer visitar a irmã em outro estado de ônibus, ele paga? | DB23 | DB23 | ✅ acerto | 0.124 |
| T29 | fora_do_tema | Fui demitido, quanto recebo de FGTS? | SEM_RESPOSTA | SEM_RESPOSTA | ✅ acerto | 0.090 |
| T30 | fora_do_tema | Como faço para pedir pensão alimentícia? | SEM_RESPOSTA | SEM_RESPOSTA | ✅ acerto | 0.080 |
| T31 | fora_do_tema | Qual a receita de bolo de cenoura? | SEM_RESPOSTA | SEM_RESPOSTA | ✅ acerto | 0.007 |
| T32 | fora_do_tema | Quem ganhou o jogo do Corinthians ontem? | SEM_RESPOSTA | SEM_RESPOSTA | ✅ acerto | 0.079 |
| T33 | fora_do_tema | O dono do apartamento não devolveu o caução do aluguel | SEM_RESPOSTA | SEM_RESPOSTA | ✅ acerto | 0.102 |
| T34 | limite_vazia | (vazia) | VAZIA | VAZIA | ✅ acerto | 0.000 |
| T35 | limite_vazia | (vazia) | VAZIA | VAZIA | ✅ acerto | 0.000 |
| T36 | limite_invalida | ?!?! ... | INVALIDA | INVALIDA | ✅ acerto | 0.001 |
| T37 | limite_ambigua | cobrança | AMBIGUA | AMBIGUA | ✅ acerto | 0.066 |
| T38 | limite_ambigua | quero cancelar | AMBIGUA | AMBIGUA | ✅ acerto | 0.066 |
| T39 | limite_sem_resposta | a loja não quis me dar nota fiscal | SEM_RESPOSTA | SEM_RESPOSTA | ✅ acerto | 0.096 |
| T40 | limite_sem_resposta | o mercado não aceita cheque | SEM_RESPOSTA | SEM_RESPOSTA | ✅ acerto | 0.084 |

## Detalhe por pergunta — conjunto de validação (estratégia híbrida)

| ID | Categoria | Pergunta | Esperado | Obtido | Resultado | Tempo (ms) |
|---|---|---|---|---|---|---|
| V01 | reformulacao | no supermercado a etiqueta dizia 8,99 e no caixa passou 12 reais | DB01 | SEM_RESPOSTA | ❌ erro | 0.117 |
| V02 | reformulacao | a farmácia dá desconto só no dinheiro, isso é permitido? | DB02 | DB02 | ✅ acerto | 0.091 |
| V03 | reformulacao | a televisão nova queimou na primeira semana | DB03 | SEM_RESPOSTA | ❌ erro | 0.008 |
| V04 | reformulacao | comprei um tênis no site e quero devolver porque não gostei | DB07 | DB07 | ✅ acerto | 0.104 |
| V05 | reformulacao | o restaurante disse que a gorjeta é obrigatória | DB10 | DB10 | ✅ acerto | 0.087 |
| V06 | reformulacao | na entrada da boate falaram que tem que consumir no mínimo 80 reais | DB11 | DB11 | ✅ acerto | 0.108 |
| V07 | reformulacao | minha avó recebeu mensagem de um falso neto pedindo pix e mandou 500 reais | DB15 | SEM_RESPOSTA | ❌ erro | 0.123 |
| V08 | reformulacao | quitei a dívida faz duas semanas e o meu nome ainda está no spc | DB18 | DB18 | ✅ acerto | 0.103 |
| V09 | reformulacao | a companhia de luz desligou a energia sem mandar nenhum aviso | DB19 | DB19 | ✅ acerto | 0.107 |
| V10 | reformulacao | a vivo não deixa eu cancelar meu plano de celular | DB20 | DB20 | ✅ acerto | 0.102 |
| V11 | reformulacao | fiquei 5 horas no aeroporto esperando e a companhia não deu nem lanche | DB22 | DB22 | ✅ acerto | 0.120 |
| V12 | reformulacao | minha filha estuda na faculdade, ela paga meia no show? | DB14 | DB14 | ✅ acerto | 0.101 |
| V13 | fora_do_tema | como tirar a segunda via do RG? | SEM_RESPOSTA | SEM_RESPOSTA | ✅ acerto | 0.083 |
| V14 | fora_do_tema | meu patrão não pagou minhas férias | SEM_RESPOSTA | SEM_RESPOSTA | ✅ acerto | 0.084 |
| V15 | limite_sem_resposta | a academia não quer cancelar meu plano sem multa | SEM_RESPOSTA | DB20 | ❌ erro | 0.141 |

## Erros por estratégia (teste + validação)

- **palavras**: T18 (esperado DB08, obtido AMBIGUA, erro seguro), V01 (esperado DB01, obtido SEM_RESPOSTA, erro seguro), V03 (esperado DB03, obtido SEM_RESPOSTA, erro seguro), V07 (esperado DB15, obtido SEM_RESPOSTA, erro seguro), V15 (esperado SEM_RESPOSTA, obtido DB20, erro perigoso)
- **tfidf**: T19 (esperado DB09, obtido AMBIGUA, erro seguro), T21 (esperado DB12, obtido AMBIGUA, erro seguro), V01 (esperado DB01, obtido SEM_RESPOSTA, erro seguro), V02 (esperado DB02, obtido SEM_RESPOSTA, erro seguro), V03 (esperado DB03, obtido SEM_RESPOSTA, erro seguro), V04 (esperado DB07, obtido SEM_RESPOSTA, erro seguro), V07 (esperado DB15, obtido SEM_RESPOSTA, erro seguro), V15 (esperado SEM_RESPOSTA, obtido DB20, erro perigoso)
- **hibrida**: T18 (esperado DB08, obtido AMBIGUA, erro seguro), V01 (esperado DB01, obtido SEM_RESPOSTA, erro seguro), V03 (esperado DB03, obtido SEM_RESPOSTA, erro seguro), V07 (esperado DB15, obtido SEM_RESPOSTA, erro seguro), V15 (esperado SEM_RESPOSTA, obtido DB20, erro perigoso)

## Testes de robustez (leitura da base e validação da saída da IA)

| Situação | Resultado | Mensagem do sistema |
|---|---|---|
| Arquivo ausente | ✅ tratado | Arquivo não encontrado: <tmp>\base_0.json |
| Arquivo vazio | ✅ tratado | O arquivo está vazio: <tmp>\base_1.json |
| JSON quebrado | ✅ tratado | JSON inválido em <tmp>\base_2.json (linha 1, coluna 41): Expecting property name enclosed in double quotes |
| Sem registros | ✅ tratado | A base não tem nenhum registro em 'registros'. |
| Registro sem campos obrigatórios é ignorado (com aviso) | ✅ tratado | Registro X2 ignorado: campo obrigatório ausente ou vazio: 'pergunta_ou_palavras_chave'; campo obrigatório ausente ou vazio: 'referencia'; campo obrigatório ausente ou vazio: 'data_de_verificacao'; Registro X1: relacionado 'X9' não existe (ignorado) |
| Relacionado inexistente gera aviso | ✅ tratado | Registro X1: relacionado 'X9' não existe (ignorado) |
| Data fora do formato é recusada | ✅ tratado | Registro X3 ignorado: 'data_de_verificacao' deve estar no formato AAAA-MM-DD; Registro X1: relacionado 'X9' não existe (ignorado) |
| Saída correta é aceita | ✅ tratado | ok |
| Texto que não é JSON é descartado | ✅ tratado | JSON inválido |
| status sem_informacao é descartado | ✅ tratado | IA informou que o registro não responde à pergunta |
| Fonte inventada é descartada | ✅ tratado | fonte diferente da do registro |
| Data alterada é descartada | ✅ tratado | data de verificação diferente da do registro |
