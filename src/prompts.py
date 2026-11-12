"""Os dois modelos de prompt comparados no projeto (ver docs/prompts.md).

O sistema funciona 100% sem IA generativa: a resposta sai sempre da base.
Este módulo existe para (1) documentar os prompts e (2) gerá-los prontos para
o experimento de comparação, que pode ser feito em qualquer chat de IA gratuito.

Uso:
    python src/prompts.py "sou obrigado a pagar 10% do garçom?"
"""
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)

from base_conhecimento import Base   # noqa: E402
from busca import Buscador           # noqa: E402

RAIZ = os.path.dirname(AQUI)

PROMPT_A = """Você é um assistente que tira dúvidas sobre direitos do consumidor no Brasil.
Responda à pergunta abaixo de forma clara.

Pergunta: {pergunta}"""

PROMPT_B = """Você é o redator do "Citizen Assist AI", um assistente informativo (NÃO oficial) sobre
direitos do consumidor. Sua única tarefa é reescrever o REGISTRO abaixo em linguagem simples
para responder à PERGUNTA.

REGRAS (obrigatórias):
1. Use SOMENTE as informações do REGISTRO. Não acrescente leis, prazos, valores ou exceções.
2. Se o REGISTRO não responder à PERGUNTA, devolva status "sem_informacao" e não invente nada.
3. Não diga que é canal oficial do governo. Não peça dados pessoais (CPF, telefone, e-mail).
4. Frases curtas, sem juridiquês, no máximo 80 palavras em "resposta_simples".
5. Copie "fonte" e "data_verificacao" exatamente como estão no REGISTRO.
6. Responda APENAS com um JSON válido, neste formato:
{{"status": "ok" | "sem_informacao",
  "resposta_simples": "...",
  "frase_pronta": "...",
  "fonte": "...",
  "data_verificacao": "AAAA-MM-DD",
  "aviso": "Orientação informativa; não substitui Procon, Defensoria ou advogado."}}

PERGUNTA: {pergunta}

REGISTRO:
{registro}"""


def registro_para_prompt(reg: dict) -> str:
    campos = {
        "titulo": reg.get("titulo"),
        "orientacao_resumida": reg["orientacao_resumida"],
        "frase_pronta": reg.get("frase_pronta"),
        "prazo": reg.get("prazo"),
        "limitacoes": reg.get("limitacoes"),
        "fonte": reg["referencia"]["norma"],
        "data_verificacao": reg["data_de_verificacao"],
    }
    return json.dumps(campos, ensure_ascii=False, indent=2)


def validar_saida_ia(texto: str, reg: dict):
    """Etapa 3 da cadeia: decide se a resposta da IA pode ser mostrada.

    Mostra SE (JSON válido E status == "ok" E fonte idêntica à do registro).
    Pela Lei de De Morgan, descarta SE (JSON inválido OU status != "ok" OU fonte divergente).
    Retorna (pode_mostrar: bool, motivo: str).
    """
    try:
        dados = json.loads(texto)
    except (json.JSONDecodeError, TypeError):
        return False, "JSON inválido"
    if not isinstance(dados, dict):
        return False, "JSON inválido"
    if dados.get("status") != "ok":
        return False, "IA informou que o registro não responde à pergunta"
    if dados.get("fonte") != reg["referencia"]["norma"]:
        return False, "fonte diferente da do registro"
    if dados.get("data_verificacao") != reg["data_de_verificacao"]:
        return False, "data de verificação diferente da do registro"
    return True, "ok"


def gerar(pergunta: str):
    base = Base(os.path.join(RAIZ, "data", "base.json"), os.path.join(RAIZ, "data", "sinonimos.json"))
    res = Buscador(base).buscar(pergunta)
    a = PROMPT_A.format(pergunta=pergunta)
    if res.tipo == "RESPOSTA":
        registro = registro_para_prompt(base.registros[res.ids[0]])
    else:
        registro = '{"aviso": "nenhum registro confiável encontrado para esta pergunta"}'
    b = PROMPT_B.format(pergunta=pergunta, registro=registro)
    return res, a, b


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass
    if len(sys.argv) < 2:
        print('Uso: python src/prompts.py "sua pergunta"')
        return 1
    pergunta = " ".join(sys.argv[1:])
    res, a, b = gerar(pergunta)
    print(f"[busca] resultado: {res.tipo} {res.ids[:1]}\n")
    print("=" * 30, "PROMPT A (direto, sem base)", "=" * 30)
    print(a)
    print()
    print("=" * 30, "PROMPT B (ancorado na base, saída JSON)", "=" * 30)
    print(b)
    return 0


if __name__ == "__main__":
    sys.exit(main())
