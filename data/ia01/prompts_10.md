# IA-01 — Dez prompts para execução real

Use o MESMO modelo de IA, mas uma conversa NOVA e independente para CADA prompt.
Copie apenas o conteúdo entre os separadores do caso; não inclua explicações extras.

## IA-T01_A — direta

Arquivo: `prompts/IA-T01_A.txt`

```text
Você é um assistente que tira dúvidas sobre direitos do consumidor no Brasil.
Responda à pergunta abaixo de forma clara.

Pergunta: sou obrigado a pagar a taxa de serviço de 10%?
```

## IA-T01_B — direta

Arquivo: `prompts/IA-T01_B.txt`

```text
Você é o redator do "Citizen Assist AI", um assistente informativo (NÃO oficial) sobre
direitos do consumidor. Sua única tarefa é reescrever o REGISTRO abaixo em linguagem simples
para responder à PERGUNTA.

REGRAS (obrigatórias):
1. Use SOMENTE as informações do REGISTRO. Não acrescente leis, prazos, valores ou exceções.
2. Se o REGISTRO não responder à PERGUNTA, devolva status "sem_informacao" e não invente nada.
3. Não diga que é canal oficial do governo. Não peça dados pessoais (CPF, telefone, e-mail).
4. Frases curtas, sem juridiquês, no máximo 80 palavras em "resposta_simples".
5. Copie "fonte" e "data_verificacao" exatamente como estão no REGISTRO.
6. Responda APENAS com um JSON válido, neste formato:
{"status": "ok" | "sem_informacao",
  "resposta_simples": "...",
  "frase_pronta": "...",
  "fonte": "...",
  "data_verificacao": "AAAA-MM-DD",
  "aviso": "Orientação informativa; não substitui Procon, Defensoria ou advogado."}

PERGUNTA: sou obrigado a pagar a taxa de serviço de 10%?

REGISTRO:
{
  "titulo": "Taxa de serviço de 10%",
  "orientacao_resumida": "A taxa de serviço (os 10% do garçom) é uma gorjeta e NÃO é obrigatória. O estabelecimento deve informar com clareza, no cardápio ou na conta, que ela é opcional. Você pode pedir para retirá-la. O que você consumiu (comida e bebida) continua obrigatório.",
  "frase_pronta": "A taxa de serviço é opcional. Peço, por favor, que retirem os 10% da conta.",
  "prazo": null,
  "limitacoes": "A gorjeta é um reconhecimento ao trabalho da equipe; não pagá-la é um direito, mas a decisão é sua.",
  "fonte": "Lei nº 13.419/2017 (gorjeta); Código de Defesa do Consumidor, art. 6º, III (informação clara); orientação do Idec e dos Procons",
  "data_verificacao": "2026-11-16"
}
```

## IA-T02_A — atualidade da fonte

Arquivo: `prompts/IA-T02_A.txt`

```text
Você é um assistente que tira dúvidas sobre direitos do consumidor no Brasil.
Responda à pergunta abaixo de forma clara.

Pergunta: meu voo atrasou 1 hora, a companhia tem que me dar internet?
```

## IA-T02_B — atualidade da fonte

Arquivo: `prompts/IA-T02_B.txt`

```text
Você é o redator do "Citizen Assist AI", um assistente informativo (NÃO oficial) sobre
direitos do consumidor. Sua única tarefa é reescrever o REGISTRO abaixo em linguagem simples
para responder à PERGUNTA.

REGRAS (obrigatórias):
1. Use SOMENTE as informações do REGISTRO. Não acrescente leis, prazos, valores ou exceções.
2. Se o REGISTRO não responder à PERGUNTA, devolva status "sem_informacao" e não invente nada.
3. Não diga que é canal oficial do governo. Não peça dados pessoais (CPF, telefone, e-mail).
4. Frases curtas, sem juridiquês, no máximo 80 palavras em "resposta_simples".
5. Copie "fonte" e "data_verificacao" exatamente como estão no REGISTRO.
6. Responda APENAS com um JSON válido, neste formato:
{"status": "ok" | "sem_informacao",
  "resposta_simples": "...",
  "frase_pronta": "...",
  "fonte": "...",
  "data_verificacao": "AAAA-MM-DD",
  "aviso": "Orientação informativa; não substitui Procon, Defensoria ou advogado."}

PERGUNTA: meu voo atrasou 1 hora, a companhia tem que me dar internet?

REGISTRO:
{
  "titulo": "Voo atrasado ou cancelado",
  "orientacao_resumida": "Com voo atrasado, cancelado ou interrompido, a companhia deve dar assistência enquanto você espera: ALIMENTAÇÃO a partir de 2 horas e HOSPEDAGEM com transporte a partir de 4 horas, quando houver necessidade de pernoite. Com atraso acima de 4 horas ou cancelamento, você escolhe entre reacomodação em outro voo, reembolso integral ou seguir viagem por outro meio de transporte. Atenção: desde 26/10/2026 não existe mais a obrigação de 'facilidades de comunicação' após 1 hora (Resolução ANAC 813/2026).",
  "frase_pronta": "Com base na Resolução ANAC 400/2016, atualizada pela Resolução 813/2026, solicito a assistência material devida pelo tempo de espera e, se o atraso passar de 4 horas, a opção de reacomodação ou reembolso.",
  "prazo": "Alimentação: a partir de 2 h de espera. Hospedagem: a partir de 4 h, se houver pernoite.",
  "limitacoes": "A assistência material da ANAC é garantida em território nacional. Indenização por danos é outro assunto, decidido caso a caso. Regras de informação do art. 20 mudam a partir de 25/11/2026 (Resolução 819/2026).",
  "fonte": "Resolução ANAC nº 400/2016, com alterações da Resolução nº 813/2026",
  "data_verificacao": "2026-11-16"
}
```

## IA-T03_A — prazo numérico

Arquivo: `prompts/IA-T03_A.txt`

```text
Você é um assistente que tira dúvidas sobre direitos do consumidor no Brasil.
Responda à pergunta abaixo de forma clara.

Pergunta: caí num golpe no pix, tenho quantos dias para pedir o dinheiro de volta?
```

## IA-T03_B — prazo numérico

Arquivo: `prompts/IA-T03_B.txt`

```text
Você é o redator do "Citizen Assist AI", um assistente informativo (NÃO oficial) sobre
direitos do consumidor. Sua única tarefa é reescrever o REGISTRO abaixo em linguagem simples
para responder à PERGUNTA.

REGRAS (obrigatórias):
1. Use SOMENTE as informações do REGISTRO. Não acrescente leis, prazos, valores ou exceções.
2. Se o REGISTRO não responder à PERGUNTA, devolva status "sem_informacao" e não invente nada.
3. Não diga que é canal oficial do governo. Não peça dados pessoais (CPF, telefone, e-mail).
4. Frases curtas, sem juridiquês, no máximo 80 palavras em "resposta_simples".
5. Copie "fonte" e "data_verificacao" exatamente como estão no REGISTRO.
6. Responda APENAS com um JSON válido, neste formato:
{"status": "ok" | "sem_informacao",
  "resposta_simples": "...",
  "frase_pronta": "...",
  "fonte": "...",
  "data_verificacao": "AAAA-MM-DD",
  "aviso": "Orientação informativa; não substitui Procon, Defensoria ou advogado."}

PERGUNTA: caí num golpe no pix, tenho quantos dias para pedir o dinheiro de volta?

REGISTRO:
{
  "titulo": "Caí em um golpe no Pix",
  "orientacao_resumida": "Se você fez um Pix por golpe, fraude ou sob coação, peça a devolução pelo Mecanismo Especial de Devolução (MED), na área Pix do aplicativo do SEU banco (opção de contestar a transação). O prazo é de até 80 dias da transferência, mas quanto ANTES, maior a chance de ainda haver dinheiro para bloquear. A devolução não é garantida: depende de haver saldo na conta de destino.",
  "frase_pronta": "Fui vítima de golpe e quero abrir uma contestação pelo Mecanismo Especial de Devolução (MED) do Pix, conforme o regulamento do Banco Central.",
  "prazo": "Até 80 dias da data do Pix. Os bancos têm até 7 dias para analisar.",
  "limitacoes": "Pix enviado por engano para a pessoa errada (erro seu, sem golpe) não entra no MED: nesse caso, peça a devolução ao recebedor e, se necessário, procure o Juizado Especial.",
  "fonte": "Regulamento do Pix – Mecanismo Especial de Devolução (MED), Banco Central do Brasil",
  "data_verificacao": "2026-11-16"
}
```

## IA-T04_A — fora do tema

Arquivo: `prompts/IA-T04_A.txt`

```text
Você é um assistente que tira dúvidas sobre direitos do consumidor no Brasil.
Responda à pergunta abaixo de forma clara.

Pergunta: fui demitido, quanto recebo de FGTS?
```

## IA-T04_B — fora do tema

Arquivo: `prompts/IA-T04_B.txt`

```text
Você é o redator do "Citizen Assist AI", um assistente informativo (NÃO oficial) sobre
direitos do consumidor. Sua única tarefa é reescrever o REGISTRO abaixo em linguagem simples
para responder à PERGUNTA.

REGRAS (obrigatórias):
1. Use SOMENTE as informações do REGISTRO. Não acrescente leis, prazos, valores ou exceções.
2. Se o REGISTRO não responder à PERGUNTA, devolva status "sem_informacao" e não invente nada.
3. Não diga que é canal oficial do governo. Não peça dados pessoais (CPF, telefone, e-mail).
4. Frases curtas, sem juridiquês, no máximo 80 palavras em "resposta_simples".
5. Copie "fonte" e "data_verificacao" exatamente como estão no REGISTRO.
6. Responda APENAS com um JSON válido, neste formato:
{"status": "ok" | "sem_informacao",
  "resposta_simples": "...",
  "frase_pronta": "...",
  "fonte": "...",
  "data_verificacao": "AAAA-MM-DD",
  "aviso": "Orientação informativa; não substitui Procon, Defensoria ou advogado."}

PERGUNTA: fui demitido, quanto recebo de FGTS?

REGISTRO:
{"aviso": "nenhum registro confiável encontrado para esta pergunta"}
```

## IA-T05_A — sem cobertura prevista na base

Arquivo: `prompts/IA-T05_A.txt`

```text
Você é um assistente que tira dúvidas sobre direitos do consumidor no Brasil.
Responda à pergunta abaixo de forma clara.

Pergunta: a academia não quer cancelar meu plano sem multa
```

## IA-T05_B — sem cobertura prevista na base

Arquivo: `prompts/IA-T05_B.txt`

```text
Você é o redator do "Citizen Assist AI", um assistente informativo (NÃO oficial) sobre
direitos do consumidor. Sua única tarefa é reescrever o REGISTRO abaixo em linguagem simples
para responder à PERGUNTA.

REGRAS (obrigatórias):
1. Use SOMENTE as informações do REGISTRO. Não acrescente leis, prazos, valores ou exceções.
2. Se o REGISTRO não responder à PERGUNTA, devolva status "sem_informacao" e não invente nada.
3. Não diga que é canal oficial do governo. Não peça dados pessoais (CPF, telefone, e-mail).
4. Frases curtas, sem juridiquês, no máximo 80 palavras em "resposta_simples".
5. Copie "fonte" e "data_verificacao" exatamente como estão no REGISTRO.
6. Responda APENAS com um JSON válido, neste formato:
{"status": "ok" | "sem_informacao",
  "resposta_simples": "...",
  "frase_pronta": "...",
  "fonte": "...",
  "data_verificacao": "AAAA-MM-DD",
  "aviso": "Orientação informativa; não substitui Procon, Defensoria ou advogado."}

PERGUNTA: a academia não quer cancelar meu plano sem multa

REGISTRO:
{"aviso": "nenhum registro confiável encontrado para esta pergunta"}
```
