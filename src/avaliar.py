"""Roda o plano de testes e compara as três estratégias de busca.

Uso:  python src/avaliar.py
Gera: docs/resultados_testes.md  e  data/resultados_testes.csv

Para cada pergunta registra: resposta esperada, resposta obtida, acerto/erro e tempo.
Indicadores: taxa de acerto (geral e por categoria) e tempo médio de consulta.
Também testa a robustez da leitura da base (arquivo ausente, vazio, JSON quebrado,
registro inválido).
"""
import csv
import json
import os
import statistics
import sys
import tempfile
from datetime import datetime

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)

from base_conhecimento import Base, ErroBase   # noqa: E402
from busca import Buscador, ESTRATEGIAS         # noqa: E402
from prompts import validar_saida_ia            # noqa: E402

RAIZ = os.path.dirname(AQUI)
REPETICOES = 5   # cada consulta roda 5 vezes; o tempo registrado é a média


def obtido(res):
    """Converte o Resultado no mesmo vocabulário do campo 'esperado'."""
    if res.tipo == "RESPOSTA":
        return res.ids[0]
    if res.tipo in ("FORA_DO_TEMA", "SEM_RESPOSTA"):
        return "SEM_RESPOSTA"
    return res.tipo


def rodar(buscador, casos, estrategia):
    linhas = []
    for c in casos:
        tempos = []
        for _ in range(REPETICOES):
            res = buscador.buscar(c["pergunta"], estrategia)
            tempos.append(res.tempo_ms)
        o = obtido(res)
        linhas.append({
            "id": c["id"], "categoria": c["categoria"], "pergunta": c["pergunta"],
            "esperado": c["esperado"], "obtido": o, "detalhe": res.tipo,
            "acerto": o == c["esperado"], "tempo_ms": statistics.mean(tempos),
        })
    return linhas


def gravidade(l):
    """Erro SEGURO: o sistema se absteve ou pediu esclarecimento (não induz a pessoa a erro).
    Erro PERIGOSO: o sistema deu uma orientação errada com confiança."""
    if l["acerto"]:
        return ""
    if l["obtido"] in ("SEM_RESPOSTA", "AMBIGUA", "VAZIA", "INVALIDA"):
        return "seguro"
    return "perigoso"


def resumo(linhas):
    total = len(linhas)
    acertos = sum(l["acerto"] for l in linhas)
    return {
        "acertos": acertos, "total": total, "taxa": acertos / total if total else 0,
        "perigosos": sum(gravidade(l) == "perigoso" for l in linhas),
        "tempo_medio": statistics.mean(l["tempo_ms"] for l in linhas),
        "tempo_max": max(l["tempo_ms"] for l in linhas),
    }


def por_categoria(linhas):
    cats = {}
    for l in linhas:
        cat = l["categoria"].split("_")[0]
        cats.setdefault(cat, []).append(l["acerto"])
    return {k: (sum(v), len(v)) for k, v in cats.items()}


def testes_robustez():
    """Cada teste: (descrição, função que deve levantar ErroBase ou gerar aviso)."""
    resultados = []
    tmp = tempfile.mkdtemp()

    def caso(desc, conteudo, espera_erro=True, espera_aviso=None):
        caminho = os.path.join(tmp, f"base_{len(resultados)}.json")
        if conteudo is not None:
            with open(caminho, "w", encoding="utf-8") as f:
                f.write(conteudo)
        try:
            b = Base(caminho)
            ok = (not espera_erro) and (espera_aviso is None or any(espera_aviso in a for a in b.avisos))
            msg = "; ".join(b.avisos) or "carregou sem avisos"
        except ErroBase as e:
            ok, msg = espera_erro, str(e)
        resultados.append((desc, ok, msg.replace(tmp, "<tmp>")))

    caso("Arquivo ausente", None)
    caso("Arquivo vazio", "")
    caso("JSON quebrado", '{"registros": [ {"identificador": "X1", ')
    caso("Sem registros", '{"registros": []}')
    reg_ok = {
        "identificador": "X1", "tema": "T", "pergunta_ou_palavras_chave": {"palavras_chave": ["teste"]},
        "orientacao_resumida": "ok", "referencia": {"norma": "Lei X"}, "data_de_verificacao": "2026-11-11",
        "relacionados": ["X9"],
    }
    reg_ruim = {"identificador": "X2", "tema": "T", "orientacao_resumida": "sem fonte"}
    caso("Registro sem campos obrigatórios é ignorado (com aviso)",
         json.dumps({"temas": ["T"], "registros": [reg_ok, reg_ruim]}), espera_erro=False,
         espera_aviso="X2 ignorado")
    caso("Relacionado inexistente gera aviso",
         json.dumps({"temas": ["T"], "registros": [reg_ok]}), espera_erro=False,
         espera_aviso="X9")
    reg_data = dict(reg_ok, identificador="X3", data_de_verificacao="11/11/2026")
    caso("Data fora do formato é recusada",
         json.dumps({"temas": ["T"], "registros": [reg_ok, reg_data]}), espera_erro=False,
         espera_aviso="X3 ignorado")
    return resultados


def testes_validador_ia(base):
    """Etapa 3 da cadeia de prompts: a saída da IA só é mostrada se passar na checagem."""
    reg = base.registros["DB10"]
    boa = {"status": "ok", "resposta_simples": "Não é obrigatória.", "frase_pronta": "...",
           "fonte": reg["referencia"]["norma"], "data_verificacao": reg["data_de_verificacao"], "aviso": "..."}
    casos = [
        ("Saída correta é aceita", json.dumps(boa, ensure_ascii=False), True),
        ("Texto que não é JSON é descartado", "A taxa não é obrigatória, segundo a lei 123.", False),
        ("status sem_informacao é descartado", json.dumps(dict(boa, status="sem_informacao")), False),
        ("Fonte inventada é descartada", json.dumps(dict(boa, fonte="Lei 99.999/2030")), False),
        ("Data alterada é descartada", json.dumps(dict(boa, data_verificacao="2020-01-01")), False),
    ]
    saida = []
    for desc, texto, esperado in casos:
        ok, motivo = validar_saida_ia(texto, reg)
        saida.append((desc, ok == esperado, motivo))
    return saida


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass
    base = Base(os.path.join(RAIZ, "data", "base.json"), os.path.join(RAIZ, "data", "sinonimos.json"))
    buscador = Buscador(base)
    conjuntos = {}
    for nome, arquivo in (("teste", "perguntas_teste.json"), ("validacao", "perguntas_validacao.json")):
        caminho = os.path.join(RAIZ, "data", arquivo)
        if os.path.exists(caminho):
            with open(caminho, encoding="utf-8") as f:
                conjuntos[nome] = json.load(f)["casos"]
    casos = conjuntos["teste"]

    todos = {e: rodar(buscador, casos, e) for e in ESTRATEGIAS}
    resumos = {e: resumo(l) for e, l in todos.items()}
    val = {e: rodar(buscador, conjuntos["validacao"], e) for e in ESTRATEGIAS} if "validacao" in conjuntos else {}
    resumos_val = {e: resumo(l) for e, l in val.items()}
    robustez = testes_robustez() + testes_validador_ia(base)

    # ---- CSV completo ----
    with open(os.path.join(RAIZ, "data", "resultados_testes.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["conjunto", "estrategia", "id", "categoria", "pergunta", "esperado", "obtido", "acerto", "tempo_ms"])
        for nome, dados in (("teste", todos), ("validacao", val)):
            for e, linhas in dados.items():
                for l in linhas:
                    w.writerow([nome, e, l["id"], l["categoria"], l["pergunta"], l["esperado"], l["obtido"],
                                "acerto" if l["acerto"] else "erro", f"{l['tempo_ms']:.3f}"])

    # ---- relatório Markdown ----
    def chave(e):
        rv = resumos_val.get(e, {"taxa": 0, "perigosos": 0})
        return (resumos[e]["taxa"] + rv["taxa"], -(resumos[e]["perigosos"] + rv["perigosos"]))
    topo = max(chave(e) for e in ESTRATEGIAS)
    melhores = [e for e in ESTRATEGIAS if chave(e) == topo]
    md = []
    md.append("# Resultados dos testes — Citizen Assist AI\n")
    md.append(f"Gerado automaticamente por `python src/avaliar.py` em {datetime.now():%d/%m/%Y %H:%M}. "
              f"{len(base.registros)} registros na base, {REPETICOES} execuções por consulta (tempo = média).\n")
    md.append("- **Conjunto de teste** (`data/perguntas_teste.json`, "
              f"{len(casos)} perguntas): usado para calibrar sinônimos, palavras-chave e limiares.")
    if val:
        md.append("- **Conjunto de validação** (`data/perguntas_validacao.json`, "
                  f"{len(conjuntos['validacao'])} perguntas novas): escrito depois da calibração e "
                  "**não** usado para ajustes. É a medida mais honesta do desempenho em perguntas inéditas.\n")
    md.append("## Comparação das estratégias de busca\n")
    md.append("| Estratégia | Acerto (teste) | Acerto (validação) | Erros perigosos (teste + validação) | Tempo médio (ms) | Tempo máximo (ms) |")
    md.append("|---|---|---|---|---|---|")
    for e in ESTRATEGIAS:
        r = resumos[e]
        rv = resumos_val.get(e)
        txt_val = f"{rv['acertos']}/{rv['total']} ({rv['taxa']:.1%})" if rv else "—"
        perig = r["perigosos"] + (rv["perigosos"] if rv else 0)
        md.append(f"| {e}{' **(padrão)**' if e == 'hibrida' else ''} | {r['acertos']}/{r['total']} "
                  f"({r['taxa']:.1%}) | {txt_val} | {perig} | {r['tempo_medio']:.3f} | {r['tempo_max']:.3f} |")
    md.append("\n*Erro seguro*: o sistema não respondeu ou pediu esclarecimento (não induz ninguém a erro). "
              "*Erro perigoso*: deu uma orientação errada com confiança — é o tipo de erro que mais importa reduzir.")
    if len(melhores) == 1:
        md.append(f"\nMelhor desempenho (teste + validação, desempate por erros perigosos): **{melhores[0]}**.\n")
    else:
        md.append(f"\nEmpate em acerto e erros perigosos entre: **{', '.join(melhores)}**. "
                  "A diferença de tempo (frações de milissegundo) é imperceptível para quem usa.\n")

    md.append("## Taxa de acerto por categoria (conjunto de teste)\n")
    cats = list(por_categoria(todos["hibrida"]).keys())
    md.append("| Categoria | " + " | ".join(ESTRATEGIAS) + " |")
    md.append("|---|" + "---|" * len(ESTRATEGIAS))
    for cat in cats:
        cel = []
        for e in ESTRATEGIAS:
            a, t_ = por_categoria(todos[e])[cat]
            cel.append(f"{a}/{t_}")
        md.append(f"| {cat} | " + " | ".join(cel) + " |")

    for titulo, linhas_h in (("conjunto de teste", todos["hibrida"]), ("conjunto de validação", val.get("hibrida", []))):
        if not linhas_h:
            continue
        md.append(f"\n## Detalhe por pergunta — {titulo} (estratégia híbrida)\n")
        md.append("| ID | Categoria | Pergunta | Esperado | Obtido | Resultado | Tempo (ms) |")
        md.append("|---|---|---|---|---|---|---|")
        for l in linhas_h:
            perg = l["pergunta"].strip() or "(vazia)"
            md.append(f"| {l['id']} | {l['categoria']} | {perg} | {l['esperado']} | {l['obtido']} | "
                      f"{'✅ acerto' if l['acerto'] else '❌ erro'} | {l['tempo_ms']:.3f} |")

    erros = {e: [l for l in todos[e] if not l["acerto"]] + [l for l in val.get(e, []) if not l["acerto"]]
             for e in ESTRATEGIAS}
    md.append("\n## Erros por estratégia (teste + validação)\n")
    for e in ESTRATEGIAS:
        if not erros[e]:
            md.append(f"- **{e}**: nenhum erro.")
        else:
            itens = ", ".join(f"{l['id']} (esperado {l['esperado']}, obtido {l['obtido']}, erro {gravidade(l)})"
                              for l in erros[e])
            md.append(f"- **{e}**: {itens}")

    md.append("\n## Testes de robustez (leitura da base e validação da saída da IA)\n")
    md.append("| Situação | Resultado | Mensagem do sistema |")
    md.append("|---|---|---|")
    for desc, ok, msg in robustez:
        md.append(f"| {desc} | {'✅ tratado' if ok else '❌ falhou'} | {msg} |")

    with open(os.path.join(RAIZ, "docs", "resultados_testes.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")

    # ---- resumo no terminal ----
    print("Estratégia   Teste            Validação        Tempo médio")
    for e in ESTRATEGIAS:
        r, rv = resumos[e], resumos_val.get(e)
        v = f"{rv['acertos']:>2}/{rv['total']:<3} {rv['taxa']:6.1%}" if rv else "—"
        print(f"{e:11}  {r['acertos']:>2}/{r['total']:<3} {r['taxa']:6.1%}   {v}   {r['tempo_medio']:.3f} ms")
    for e in ESTRATEGIAS:
        for l in erros[e]:
            print(f"  [{e}] ERRO {gravidade(l).upper()} {l['id']}: esperado {l['esperado']}, obtido {l['obtido']} ({l['detalhe']}) — {l['pergunta']}")
    falhas_rob = [d for d, ok, _ in robustez if not ok]
    print(f"Robustez: {len(robustez) - len(falhas_rob)}/{len(robustez)} tratados" +
          (f" — falhas: {falhas_rob}" if falhas_rob else ""))
    print("Relatório: docs/resultados_testes.md | CSV: data/resultados_testes.csv")


if __name__ == "__main__":
    main()
