# Resultados dos testes — Citizen Assist AI

Gerado automaticamente por `python src/avaliar.py` em 18/11/2026 14:28. 23 registros na base, 5 execuções por consulta (tempo = média).

- **Conjunto de teste e regressão** (`data/perguntas_teste.json`, 56 perguntas): usado para calibrar sinônimos, palavras-chave, limiares e regressões de BUS-01.
- **Conjunto de validação** (`data/perguntas_validacao.json`, 18 perguntas inéditas reservadas + 1 regressão conhecida `V15`): casos inéditos não usados para ajustes são separados da regressão conhecida `V15`.

## Comparação das estratégias de busca

| Estratégia | Acerto (teste + regressão) | Acerto (validação inédita) | Erros perigosos (corpus avaliado) | Tempo médio (ms) | Tempo máximo (ms) |
|---|---|---|---|---|---|
| palavras | 55/56 (98.2%) | 14/18 (77.8%) | 0 | 0.039 | 0.060 |
| tfidf | 54/56 (96.4%) | 12/18 (66.7%) | 1 | 0.078 | 0.131 |
| hibrida **(padrão)** | 55/56 (98.2%) | 14/18 (77.8%) | 0 | 0.112 | 0.379 |

*Erro seguro*: o sistema não respondeu ou pediu esclarecimento sem oferecer opção incompatível. *Erro perigoso*: deu orientação errada ou ofereceu candidato explicitamente proibido no corpus avaliado (não garante ausência de falhas fora dele).

Empate em acerto e erros perigosos entre: **palavras, hibrida**. A diferença de tempo (frações de milissegundo) é imperceptível para quem usa.

## Taxa de acerto por categoria (conjunto de teste)

| Categoria | palavras | tfidf | hibrida |
|---|---|---|---|
| direta | 12/12 | 12/12 | 12/12 |
| reformulacao | 15/16 | 14/16 | 15/16 |
| fora | 5/5 | 5/5 | 5/5 |
| limite | 7/7 | 7/7 | 7/7 |
| regressao | 16/16 | 16/16 | 16/16 |

## Detalhe por pergunta — conjunto de teste e regressão (estratégia híbrida)

| ID | Categoria | Pergunta | Esperado | Obtido | Candidatos exibidos | Resultado | Tempo (ms) |
|---|---|---|---|---|---|---|---|
| T01 | direta | O preço da prateleira é diferente do preço no caixa | DB01 | DB01 | DB01 | Acerto | 0.100 |
| T02 | direta | A loja pode cobrar mais caro no cartão de crédito? | DB02 | DB02 | DB02 | Acerto | 0.098 |
| T03 | direta | Comprei uma geladeira e ela veio com defeito | DB03 | DB03 | DB03 | Acerto | 0.091 |
| T04 | direta | Me arrependi de uma compra pela internet, posso devolver? | DB07 | DB07 | DB07 | Acerto | 0.093 |
| T05 | direta | Sou obrigado a pagar a taxa de serviço de 10%? | DB10 | DB10 | DB10 | Acerto | 0.139 |
| T06 | direta | O bar cobra consumação mínima, pode? | DB11 | DB11 | DB11 | Acerto | 0.165 |
| T07 | direta | Caí em um golpe no Pix, como recupero o dinheiro? | DB15 | DB15 | DB15 | Acerto | 0.178 |
| T08 | direta | Meu nome foi negativado no Serasa sem aviso | DB18 | DB18 | DB18 | Acerto | 0.152 |
| T09 | direta | Como cancelar a internet da operadora? | DB20 | DB20 | DB20 | Acerto | 0.088 |
| T10 | direta | Meu voo foi cancelado, tenho direito a hotel? | DB22 | DB22 | DB22 | Acerto | 0.123 |
| T11 | direta | Quem tem direito a meia-entrada no cinema? | DB14 | DB14 | DB14 | Acerto | 0.159 |
| T12 | direta | Idoso tem passagem de ônibus interestadual gratuita? | DB23 | DB23 | DB23 | Acerto | 0.143 |
| T13 | reformulacao | passaram as compras e o arroz deu mais caro do que tava na gondola | DB01 | DB01 | DB01 | Acerto | 0.127 |
| T14 | reformulacao | o tênis que eu comprei rasgou e a loja falou pra eu me virar com a fábrica | DB03 | DB03 | DB03 | Acerto | 0.130 |
| T15 | reformulacao | ganhei uma blusa de presente mas ficou apertada, a loja tem que trocar? | DB04 | DB04 | DB04 | Acerto | 0.134 |
| T16 | reformulacao | o vendedor disse que o celular só sai se eu levar a garantia estendida junto | DB05 | DB05 | DB05 | Acerto | 0.135 |
| T17 | reformulacao | to gravida e o banco nao quis me atender na fila preferencial | DB06 | DB06 | DB06 | Acerto | 0.179 |
| T18 | reformulacao | fiz um pedido no app faz 20 dias e até agora nada de chegar | DB08 | AMBIGUA | DB08, DB07 | Erro | 0.108 |
| T19 | reformulacao | chegou um cartão de crédito em casa que eu nunca pedi | DB09 | DB09 | DB09 | Acerto | 0.102 |
| T20 | reformulacao | o garçom botou os dez por cento sem me perguntar | DB10 | DB10 | DB10 | Acerto | 0.106 |
| T21 | reformulacao | sumiu meu cartão de consumo na balada e querem me cobrar 300 reais | DB12 | DB12 | DB12 | Acerto | 0.119 |
| T22 | reformulacao | trouxeram pãozinho e manteiga na mesa sem eu pedir e cobraram | DB13 | DB13 | DB13 | Acerto | 0.109 |
| T23 | reformulacao | mandei dinheiro pro golpista que se passou pelo meu filho no zap | DB15 | DB15 | DB15 | Acerto | 0.108 |
| T24 | reformulacao | a empresa me cobrou duas vezes a mesma fatura e eu paguei as duas | DB16 | DB16 | DB16 | Acerto | 0.112 |
| T25 | reformulacao | a assessoria de cobrança liga pros meus colegas de trabalho falando da minha dívida | DB17 | DB17 | DB17 | Acerto | 0.122 |
| T26 | reformulacao | a enel cortou a energia lá de casa num sábado | DB19 | DB19 | DB19 | Acerto | 0.103 |
| T27 | reformulacao | não aguento mais o banco me ligando pra oferecer consignado | DB21 | DB21 | DB21 | Acerto | 0.107 |
| T28 | reformulacao | meu pai tem 63 anos e quer visitar a irmã em outro estado de ônibus, ele paga? | DB23 | DB23 | DB23 | Acerto | 0.379 |
| T29 | fora_do_tema | Fui demitido, quanto recebo de FGTS? | SEM_RESPOSTA | SEM_RESPOSTA | — | Acerto | 0.194 |
| T30 | fora_do_tema | Como faço para pedir pensão alimentícia? | SEM_RESPOSTA | SEM_RESPOSTA | — | Acerto | 0.118 |
| T31 | fora_do_tema | Qual a receita de bolo de cenoura? | SEM_RESPOSTA | SEM_RESPOSTA | — | Acerto | 0.009 |
| T32 | fora_do_tema | Quem ganhou o jogo do Corinthians ontem? | SEM_RESPOSTA | SEM_RESPOSTA | — | Acerto | 0.120 |
| T33 | fora_do_tema | O dono do apartamento não devolveu o caução do aluguel | SEM_RESPOSTA | SEM_RESPOSTA | — | Acerto | 0.111 |
| T34 | limite_vazia | (vazia) | VAZIA | VAZIA | — | Acerto | 0.001 |
| T35 | limite_vazia | (vazia) | VAZIA | VAZIA | — | Acerto | 0.000 |
| T36 | limite_invalida | ?!?! ... | INVALIDA | INVALIDA | — | Acerto | 0.002 |
| T37 | limite_ambigua | cobrança | AMBIGUA | AMBIGUA | DB16, DB17, DB02 | Acerto | 0.069 |
| T38 | limite_ambigua | quero cancelar | AMBIGUA | AMBIGUA | DB20, DB22, DB07 | Acerto | 0.070 |
| T39 | limite_sem_resposta | a loja não quis me dar nota fiscal | SEM_RESPOSTA | SEM_RESPOSTA | — | Acerto | 0.105 |
| T40 | limite_sem_resposta | o mercado não aceita cheque | SEM_RESPOSTA | SEM_RESPOSTA | — | Acerto | 0.088 |
| T41 | regressao_setor | a academia quer cobrar multa para cancelar minha matrícula | SEM_RESPOSTA | SEM_RESPOSTA | — | Acerto | 0.113 |
| T42 | regressao_setor | a academia quer cobrar multa indevida para cancelar o plano | DB16 | DB16 | DB16 | Acerto | 0.118 |
| T43 | regressao_setor | quero cancelar minha linha da Oi | DB20 | DB20 | DB20 | Acerto | 0.078 |
| T44 | regressao_setor | quero cancelar minha internet da Vivo que uso para estudar na faculdade | DB20 | DB20 | DB20 | Acerto | 0.110 |
| T45 | regressao_setor | quero cancelar minha tv por assinatura da claro | DB20 | DB20 | DB20 | Acerto | 0.089 |
| T46 | regressao_setor | como cancelar plano de fibra óptica da tim sem falar com atendente | DB20 | DB20 | DB20 | Acerto | 0.161 |
| T47 | regressao_setor | a escola de idiomas quer cobrar multa abusiva para cancelar o curso | SEM_RESPOSTA | SEM_RESPOSTA | — | Acerto | 0.156 |
| T48 | regressao_setor | oi, a academia nao quer cancelar meu plano sem multa | SEM_RESPOSTA | SEM_RESPOSTA | — | Acerto | 0.143 |
| T49 | regressao_setor | quero cancelar meu plano da academia pela internet | SEM_RESPOSTA | SEM_RESPOSTA | — | Acerto | 0.096 |
| T50 | regressao_setor | quero cancelar minha assinatura de curso online | SEM_RESPOSTA | SEM_RESPOSTA | — | Acerto | 0.091 |
| T51 | regressao_setor | oi, quero cancelar minha linha da Oi | DB20 | DB20 | DB20 | Acerto | 0.078 |
| T52 | regressao_setor | a academia quer cobrar multa para cancelar meu plano pelo celular | SEM_RESPOSTA | SEM_RESPOSTA | — | Acerto | 0.116 |
| T53 | regressao_setor | quero cancelar minha net | DB20 | DB20 | DB20 | Acerto | 0.075 |
| T54 | regressao_setor | fiz a compra de um curso pela internet ontem e me arrependi, posso devolver? | DB07 | DB07 | DB07 | Acerto | 0.103 |
| T55 | regressao_setor | quero cancelar minha academia pelo meu celular da Vivo | SEM_RESPOSTA | SEM_RESPOSTA | — | Acerto | 0.093 |
| T56 | regressao_setor | quero cancelar o curso | SEM_RESPOSTA | SEM_RESPOSTA | — | Acerto | 0.075 |

## Detalhe por pergunta — conjunto de validação (estratégia híbrida)

| ID | Categoria | Pergunta | Esperado | Obtido | Candidatos exibidos | Resultado | Tempo (ms) |
|---|---|---|---|---|---|---|---|
| V01 | reformulacao | no supermercado a etiqueta dizia 8,99 e no caixa passou 12 reais | DB01 | SEM_RESPOSTA | — | Erro | 0.167 |
| V02 | reformulacao | a farmácia dá desconto só no dinheiro, isso é permitido? | DB02 | DB02 | DB02 | Acerto | 0.120 |
| V03 | reformulacao | a televisão nova queimou na primeira semana | DB03 | SEM_RESPOSTA | — | Erro | 0.011 |
| V04 | reformulacao | comprei um tênis no site e quero devolver porque não gostei | DB07 | DB07 | DB07 | Acerto | 0.134 |
| V05 | reformulacao | o restaurante disse que a gorjeta é obrigatória | DB10 | DB10 | DB10 | Acerto | 0.093 |
| V06 | reformulacao | na entrada da boate falaram que tem que consumir no mínimo 80 reais | DB11 | DB11 | DB11 | Acerto | 0.248 |
| V07 | reformulacao | minha avó recebeu mensagem de um falso neto pedindo pix e mandou 500 reais | DB15 | SEM_RESPOSTA | — | Erro | 0.235 |
| V08 | reformulacao | quitei a dívida faz duas semanas e o meu nome ainda está no spc | DB18 | DB18 | DB18 | Acerto | 0.195 |
| V09 | reformulacao | a companhia de luz desligou a energia sem mandar nenhum aviso | DB19 | DB19 | DB19 | Acerto | 0.188 |
| V10 | reformulacao | a vivo não deixa eu cancelar meu plano de celular | DB20 | DB20 | DB20 | Acerto | 0.187 |
| V11 | reformulacao | fiquei 5 horas no aeroporto esperando e a companhia não deu nem lanche | DB22 | DB22 | DB22 | Acerto | 0.229 |
| V12 | reformulacao | minha filha estuda na faculdade, ela paga meia no show? | DB14 | DB14 | DB14 | Acerto | 0.189 |
| V13 | fora_do_tema | como tirar a segunda via do RG? | SEM_RESPOSTA | SEM_RESPOSTA | — | Acerto | 0.158 |
| V14 | fora_do_tema | meu patrão não pagou minhas férias | SEM_RESPOSTA | SEM_RESPOSTA | — | Acerto | 0.142 |
| V15 | regressao_conhecida | a academia não quer cancelar meu plano sem multa | SEM_RESPOSTA | SEM_RESPOSTA | — | Acerto | 0.148 |
| V16 | limite_sem_resposta | o clube social não deixa eu encerrar minha assinatura anual sem multa | SEM_RESPOSTA | SEM_RESPOSTA | — | Acerto | 0.152 |
| V17 | reformulacao | quero encerrar meu contrato de banda larga residencial | DB20 | SEM_RESPOSTA | — | Erro | 0.099 |
| V18 | limite_sem_resposta | o estúdio de pilates quer cobrar 50% de multa rescisória no cancelamento | SEM_RESPOSTA | SEM_RESPOSTA | — | Acerto | 0.125 |
| V19 | reformulacao | a operadora claro cobrou multa de fidelidade no cancelamento do meu chip | DB20 | DB20 | DB20 | Acerto | 0.115 |

## Erros por estratégia (teste + validação)

- **palavras**: T18 (esperado DB08, obtido AMBIGUA, erro seguro), V01 (esperado DB01, obtido SEM_RESPOSTA, erro seguro), V03 (esperado DB03, obtido SEM_RESPOSTA, erro seguro), V07 (esperado DB15, obtido SEM_RESPOSTA, erro seguro), V17 (esperado DB20, obtido SEM_RESPOSTA, erro seguro)
- **tfidf**: T19 (esperado DB09, obtido AMBIGUA, erro seguro), T21 (esperado DB12, obtido AMBIGUA, erro seguro), V01 (esperado DB01, obtido SEM_RESPOSTA, erro seguro), V02 (esperado DB02, obtido SEM_RESPOSTA, erro seguro), V03 (esperado DB03, obtido SEM_RESPOSTA, erro seguro), V04 (esperado DB07, obtido SEM_RESPOSTA, erro seguro), V07 (esperado DB15, obtido SEM_RESPOSTA, erro seguro), V17 (esperado DB20, obtido DB04, erro perigoso)
- **hibrida**: T18 (esperado DB08, obtido AMBIGUA, erro seguro), V01 (esperado DB01, obtido SEM_RESPOSTA, erro seguro), V03 (esperado DB03, obtido SEM_RESPOSTA, erro seguro), V07 (esperado DB15, obtido SEM_RESPOSTA, erro seguro), V17 (esperado DB20, obtido SEM_RESPOSTA, erro seguro)

## Testes de robustez (base, saída da IA e gravidade do avaliador)

| Situação | Resultado | Mensagem do sistema |
|---|---|---|
| Arquivo ausente | Tratado | Arquivo não encontrado: <tmp>\base_0.json |
| Arquivo vazio | Tratado | O arquivo está vazio: <tmp>\base_1.json |
| JSON quebrado | Tratado | JSON inválido em <tmp>\base_2.json (linha 1, coluna 41): Expecting property name enclosed in double quotes |
| Sem registros | Tratado | A base não tem nenhum registro em 'registros'. |
| Registro sem campos obrigatórios é ignorado (com aviso) | Tratado | Registro X2 ignorado: campo obrigatório ausente ou vazio: 'pergunta_ou_palavras_chave'; campo obrigatório ausente ou vazio: 'referencia'; campo obrigatório ausente ou vazio: 'data_de_verificacao'; Registro X1: relacionado 'X9' não existe (ignorado) |
| Relacionado inexistente gera aviso | Tratado | Registro X1: relacionado 'X9' não existe (ignorado) |
| Data fora do formato é recusada | Tratado | Registro X3 ignorado: 'data_de_verificacao' deve estar no formato AAAA-MM-DD; Registro X1: relacionado 'X9' não existe (ignorado) |
| Saída correta é aceita | Tratado | ok |
| Texto que não é JSON é descartado | Tratado | JSON inválido |
| status sem_informacao é descartado | Tratado | IA informou que o registro não responde à pergunta |
| Fonte inventada é descartada | Tratado | fonte diferente da do registro |
| Data alterada é descartada | Tratado | data de verificação diferente da do registro |
| AMBIGUA com candidato proibido é erro perigoso | Tratado | gravidade=perigoso (ofereceu/exibiu ID proibido: DB20) |
| RESPOSTA com registro exibido proibido é erro perigoso | Tratado | gravidade=perigoso (ofereceu/exibiu ID proibido: DB20) |
