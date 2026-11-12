"""Checagem de condições ("será que isso vale para mim?") com lógica de três valores.

Cada condição é respondida com SIM, NÃO ou NÃO SEI (None).
  - regra "todas"  (E lógico):  A ∧ B ∧ C
  - regra "alguma" (OU lógico): A ∨ B ∨ C

Quando o resultado é negativo, as Leis de De Morgan dizem POR QUÊ:
  ¬(A ∧ B) = ¬A ∨ ¬B   -> basta UMA condição falhar; mostramos qual(is).
  ¬(A ∨ B) = ¬A ∧ ¬B   -> TODAS falharam; mostramos que nenhuma foi atendida.

"Não sei" segue a lógica de Kleene: com "todas", um NÃO decide (falso) mesmo com
dúvidas; com "alguma", um SIM decide (verdadeiro) mesmo com dúvidas. Se nada decide,
o resultado é INDETERMINADO e o sistema não afirma nada.
"""


def avaliar(regra: str, respostas: dict):
    """respostas: id -> True | False | None. Retorna (True|False|None, ids_que_explicam)."""
    valores = list(respostas.values())
    if regra == "todas":
        falhas = [k for k, v in respostas.items() if v is False]
        if falhas:
            return False, falhas                      # De Morgan: ¬A ∨ ¬B
        if all(v is True for v in valores):
            return True, list(respostas)
        return None, [k for k, v in respostas.items() if v is None]
    # regra "alguma"
    acertos = [k for k, v in respostas.items() if v is True]
    if acertos:
        return True, acertos
    if all(v is False for v in valores):
        return False, list(respostas)                 # De Morgan: ¬A ∧ ¬B
    return None, [k for k, v in respostas.items() if v is None]


def interpretar_resposta(texto: str):
    """'s', 'sim' -> True; 'n', 'nao' -> False; '?', 'nao sei' -> None; outro -> 'invalida'."""
    t = (texto or "").strip().lower()
    t = t.replace("ã", "a")
    if t in ("s", "sim", "1", "y", "yes"):
        return True
    if t in ("n", "nao", "2", "no"):
        return False
    if t in ("?", "nao sei", "ns", "3", "talvez"):
        return None
    return "invalida"
