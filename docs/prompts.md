# Estratégias de prompt — Pode Isso?

## Por que o sistema funciona sem IA generativa

O núcleo do Pode Isso? é **determinístico**: a resposta sai sempre de um registro da base (`data/base.json`), com a fonte e a data de verificação. Isso garante o requisito mais importante do case: **não inventar**. A IA generativa entra apenas como uma camada **opcional** para reescrever o registro em linguagem ainda mais simples. Nenhuma API paga é necessária.

A comparação abaixo responde à pergunta: *se usarmos um modelo de linguagem, qual forma de pedir dá respostas mais seguras?*

## Cadeia de prompts proposta

```
Pergunta da pessoa
   │
   ▼
[Etapa 1 — Classificação]  busca determinística (src/busca.py)
   │   RESPOSTA / AMBIGUA / SEM_RESPOSTA / FORA_DO_TEMA / VAZIA / INVALIDA
   ▼
[Etapa 2 — Redação]        Prompt B recebe a pergunta + o registro encontrado
   │   saída estruturada em JSON
   ▼
[Etapa 3 — Validação]      o programa confere o JSON:
       mostra a versão da IA  SE  (JSON válido  E  status = "ok"  E  fonte idêntica à do registro)
       caso contrário (De Morgan: JSON inválido OU status ≠ "ok" OU fonte divergente)
       → descarta a IA e mostra o texto original da base
```

## Modelo A — Prompt direto (sem base)

```text
Você é um assistente que tira dúvidas sobre direitos do consumidor no Brasil.
Responda à pergunta abaixo de forma clara.

Pergunta: {pergunta}
```

## Modelo B — Prompt ancorado na base, com saída estruturada

```text
Você é o redator do "Pode Isso?", um assistente informativo (NÃO oficial) sobre
direitos do consumidor. Sua única tarefa é reescrever o REGISTRO abaixo em linguagem simples
para responder à PERGUNTA.

REGRAS (obrigatórias):
1. Use SOMENTE as informações do REGISTRO. Não acrescente leis, prazos, valores ou exceções.
2. Se o REGISTRO não responder à PERGUNTA, devolva status "sem_informacao" e não invente nada.
3. Não diga que é canal oficial do governo. Não peça dados pessoais (CPF, telefone, e-mail).
4. Frases curtas, sem juridiquês, no máximo 80 palavras em "resposta_simples".
5. Copie "fonte" e "data_verificacao" exatamente como estão no REGISTRO.
6. Responda APENAS com um JSON válido, neste formato:
{"status": "ok" | "sem_informacao", "resposta_simples": "...", "frase_pronta": "...",
 "fonte": "...", "data_verificacao": "AAAA-MM-DD",
 "aviso": "Orientação informativa; não substitui Procon, Defensoria ou advogado."}

PERGUNTA: {pergunta}

REGISTRO:
{registro em JSON}
```

Para gerar os dois prompts já preenchidos para qualquer pergunta:

```bash
python src/prompts.py "sou obrigado a pagar 10% do garçom?"
```

## Comparação esperada (análise de projeto)

| Critério | Modelo A (direto) | Modelo B (ancorado + JSON) |
|---|---|---|
| Fonte citada | Às vezes, sem garantia de que existe | Sempre a do registro (verificável) |
| Risco de inventar lei, prazo ou valor | Alto | Baixo (proibido pela regra 1 e conferido na etapa 3) |
| Informação desatualizada | Depende do corte de treino do modelo | Depende da base, que tem data de verificação |
| Fora do tema | Tende a responder mesmo assim | Devolve `sem_informacao` |
| Formato | Texto livre, difícil de validar | JSON validável pelo programa |
| Linguagem simples | Variável | Exigida (regra 4) |
| Custo | Igual | Igual (prompt maior, mas sem API paga) |

**Exemplo concreto de risco do Modelo A:** a Resolução ANAC 813/2026 retirou, a partir de 26/10/2026, a obrigação de "facilidades de comunicação" após 1 hora de atraso de voo. Um modelo treinado antes dessa data tende a afirmar a regra antiga com confiança. No Modelo B, a resposta vem do registro DB22, verificado em 11/11/2026.

## Experimento de comparação (protocolo)

Para transformar a análise acima em dados, rode as mesmas 5 perguntas nos dois prompts, no mesmo chat de IA gratuito, em conversas novas:

| # | Pergunta | Por que foi escolhida |
|---|---|---|
| 1 | sou obrigado a pagar a taxa de serviço de 10%? | direta |
| 2 | meu voo atrasou 1 hora, a companhia tem que me dar internet? | regra que mudou em 2026 |
| 3 | caí num golpe no pix, tenho quantos dias para pedir o dinheiro de volta? | prazo numérico |
| 4 | fui demitido, quanto recebo de FGTS? | fora do tema |
| 5 | a academia não quer cancelar meu plano sem multa | situação que a base não cobre |

Para cada resposta, marque: (a) citou fonte verificável? (b) inventou algo que não está no registro/na lei? (c) recusou quando devia? (d) saída no formato pedido? (e) número de palavras.

| # | Modelo | Fonte verificável | Inventou algo | Recusou quando devia | Formato OK | Palavras |
|---|---|---|---|---|---|---|
| 1 | A | | | n/a | n/a | |
| 1 | B | | | n/a | | |
| 2 | A | | | n/a | n/a | |
| 2 | B | | | n/a | | |
| 3 | A | | | n/a | n/a | |
| 3 | B | | | n/a | | |
| 4 | A | | | | n/a | |
| 4 | B | | | | | |
| 5 | A | | | | n/a | |
| 5 | B | | | | | |

> **Pendente:** preencher esta tabela com a execução real (modelo usado, data). Registrar também em `docs/uso_ia.md`.
