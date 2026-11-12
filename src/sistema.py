"""Citizen Assist AI — assistente de direitos do consumidor no dia a dia.

Execução:   python src/sistema.py
Opções:     python src/sistema.py --help

Interface textual. Só usa a biblioteca padrão do Python (3.10+).
"""
import argparse
import os
import sys
import textwrap

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)

from base_conhecimento import Base, ErroBase          # noqa: E402
from busca import Buscador, ESTRATEGIAS, LIMIAR        # noqa: E402
from condicoes import avaliar, interpretar_resposta    # noqa: E402
from privacidade import mascarar                       # noqa: E402

RAIZ = os.path.dirname(AQUI)
BASE_PADRAO = os.path.join(RAIZ, "data", "base.json")
SINONIMOS_PADRAO = os.path.join(RAIZ, "data", "sinonimos.json")
LARGURA = 78


# ---------------------------------------------------------------- saída
class Tela:
    """Cuida da impressão: quebra de linha e marcadores textuais."""

    TEXTOS = {
        "titulo": "==", "direito": "»", "fala": "»", "passos": "»", "prazo": "»",
        "reclamar": "»", "fonte": "»", "limite": "(!)", "aviso": "(!)", "rel": "»", "erro": "(!)",
        "info": "(i)", "privado": "(!)",
    }

    def __init__(self, simples: bool):
        self.simples = simples

    def i(self, chave):
        return self.TEXTOS[chave]

    def p(self, texto="", recuo=0):
        if not texto:
            print()
            return
        prefixo = " " * recuo
        for par in str(texto).split("\n"):
            print(textwrap.fill(par, LARGURA, initial_indent=prefixo, subsequent_indent=prefixo))

    def linha(self):
        print(("-" if self.simples else "─") * LARGURA)


def preparar_console(simples: bool) -> bool:
    """Força UTF-8 no terminal. Se não der, liga o modo simples automaticamente."""
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stdin.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass
    enc = (getattr(sys.stdout, "encoding", "") or "").lower()
    return simples or "utf" not in enc


# ---------------------------------------------------------------- respostas
def mostrar_registro(t: Tela, base: Base, rid: str, explicacao: str = ""):
    reg = base.registros[rid]
    ref = reg["referencia"]
    t.linha()
    t.p(f"{t.i('titulo')} {reg['titulo'].upper()}   ({reg['tema']})")
    t.linha()
    t.p(f"{t.i('direito')} O QUE VOCÊ PRECISA SABER")
    t.p(reg["orientacao_resumida"], 3)
    if reg.get("frase_pronta"):
        t.p()
        t.p(f"{t.i('fala')} MOSTRE NA TELA OU FALE:")
        t.p(f"“{reg['frase_pronta']}”", 3)
    if reg.get("passos"):
        t.p()
        t.p(f"{t.i('passos')} O QUE FAZER")
        for n, passo in enumerate(reg["passos"], 1):
            t.p(f"{n}. {passo}", 3)
    if reg.get("prazo"):
        t.p()
        t.p(f"{t.i('prazo')} PRAZO: {reg['prazo']}")
    if reg.get("onde_reclamar"):
        t.p(f"{t.i('reclamar')} SE NÃO RESOLVEREM: {reg['onde_reclamar']}")
    if reg.get("limitacoes"):
        t.p(f"{t.i('limite')} ATENÇÃO: {reg['limitacoes']}")
    t.p()
    data = reg["data_de_verificacao"].split("-")
    t.p(f"{t.i('fonte')} FONTE: {ref['norma']}")
    if ref.get("url"):
        t.p(ref["url"], 3)
    t.p(f"Verificado em {data[2]}/{data[1]}/{data[0]}.", 3)
    t.p(f"{t.i('aviso')} {base.meta.get('aviso_padrao', '')}")
    if explicacao:
        t.p(f"{t.i('info')} {explicacao}")
    t.linha()


def opcoes_pos_resposta(t: Tela, base: Base, rid: str, interativo: bool = True) -> dict:
    """Mostra os atalhos de navegação e devolve o mapa atalho -> ação."""
    mapa = {}
    rel = base.relacionados(rid)
    if rel:
        t.p(f"{t.i('rel')} ASSUNTOS RELACIONADOS:")
        for n, r in enumerate(rel, 1):
            mapa[f"r{n}"] = ("abrir", r)
            t.p(f"[r{n}] {base.registros[r]['titulo']}", 3)
    if not interativo:
        return mapa
    if base.registros[rid].get("condicoes"):
        mapa["v"] = ("verificar", rid)
        t.p("[v]  Verificar se isso vale para o seu caso (perguntas de sim/não)")
    t.p("Ou digite outra dúvida.  [m] menu   [0] sair")
    return mapa


def verificar_condicoes(t: Tela, base: Base, rid: str, entrada):
    cond = base.registros[rid]["condicoes"]
    t.p()
    t.p("Responda com  s (sim),  n (não)  ou  ? (não sei).  Não guardo nenhuma resposta.")
    respostas = {}
    for item in cond["itens"]:
        while True:
            r = interpretar_resposta(entrada(f"  {item['pergunta']} "))
            if r != "invalida":
                respostas[item["id"]] = r
                break
            t.p("Resposta não reconhecida. Use s, n ou ?.", 3)
    resultado, quais = avaliar(cond["regra"], respostas)
    perguntas = {i["id"]: i["pergunta"] for i in cond["itens"]}
    t.p()
    if resultado is True:
        t.p(f"{t.i('direito')} {cond['se_sim']}")
    elif resultado is False:
        t.p(f"{t.i('limite')} {cond['se_nao']}")
        if cond["regra"] == "todas":
            t.p("Motivo — esta condição não foi atendida:" if len(quais) == 1
                else "Motivo — estas condições não foram atendidas:")
        else:
            t.p("Motivo — nenhuma das condições foi atendida.")
        for q in quais:
            t.p(f"• {perguntas[q]}", 3)
    else:
        t.p(f"{t.i('info')} Não dá para afirmar com as respostas dadas. Confira estes pontos:")
        for q in quais:
            t.p(f"• {perguntas[q]}", 3)
    t.p(f"{t.i('aviso')} Esta checagem é uma orientação, não uma decisão oficial.")


def explicar_decisao(res, base) -> str:
    if not res.notas:
        return ""
    partes = [f"{rid}={nota:.2f}" for rid, nota in zip(res.ids, res.notas)]
    return (f"Busca '{res.estrategia}' em {res.tempo_ms:.2f} ms | notas: {', '.join(partes)} "
            f"| limiar {LIMIAR[res.estrategia]:.2f}")


# ---------------------------------------------------------------- menus
def menu(t: Tela):
    t.p()
    t.p("O que você quer fazer?")
    t.p("[1] Ver os temas e todas as situações", 2)
    t.p("[2] Como funciona e avisos importantes", 2)
    t.p("[3] Ligar/desligar o modo explicação (mostra como a busca decidiu)", 2)
    t.p("[0] Sair", 2)
    t.p("…ou simplesmente escreva sua dúvida. Ex.: “cobraram 10% na conta, sou obrigado?”")


def sobre(t: Tela, base: Base, estrategia: str):
    t.linha()
    t.p("COMO FUNCIONA")
    t.p(f"Você escreve a dúvida do seu jeito. Eu procuro a situação mais parecida entre "
        f"{len(base.registros)} situações verificadas, em {len(base.por_tema)} temas, e respondo "
        f"com: o seu direito, uma frase pronta para mostrar, os passos, onde reclamar e a FONTE "
        f"oficial com a data em que foi conferida.")
    t.p(f"Se eu não tiver uma resposta confiável, eu aviso em vez de inventar. "
        f"Estratégia de busca atual: {estrategia}.")
    t.p()
    t.p(f"{t.i('privado')} Não peça nem digite CPF, telefone, e-mail ou número de cartão. "
        "Eu não preciso de nenhum dado pessoal e não gravo nada do que você digita.")
    t.p(f"{t.i('aviso')} {base.meta.get('aviso_padrao', '')}")
    t.linha()


def listar_temas(t: Tela, base: Base) -> dict:
    t.p()
    mapa = {}
    for n, tema in enumerate(base.por_tema, 1):
        ids = base.por_tema[tema]
        t.p(f"[t{n}] {tema}  ({len(ids)} situações)")
        mapa[f"t{n}"] = ("tema", tema)
    t.p("Digite o código do tema (ex.: t1) para ver as situações.")
    return mapa


def listar_situacoes(t: Tela, base: Base, tema: str) -> dict:
    t.p()
    t.p(f"Situações em “{tema}”:")
    mapa = {}
    for n, rid in enumerate(base.por_tema[tema], 1):
        t.p(f"[s{n}] {base.registros[rid]['titulo']}", 2)
        mapa[f"s{n}"] = ("abrir", rid)
    t.p("Digite o código da situação (ex.: s1).")
    return mapa


# ---------------------------------------------------------------- consulta
def responder(t: Tela, base: Base, buscador: Buscador, consulta: str, estrategia: str,
              explicar: bool, interativo: bool = True) -> dict:
    """Processa uma pergunta em texto livre. Devolve os atalhos válidos depois da resposta."""
    consulta, achados = mascarar(consulta)
    if achados:
        t.p(f"{t.i('privado')} Você digitou o que parece ser {', '.join(achados)}. "
            "Não precisa! Removi esse dado e não guardo nada.")

    res = buscador.buscar(consulta, estrategia)
    exp = explicar_decisao(res, base) if explicar else ""

    if res.tipo == "VAZIA":
        t.p(f"{t.i('erro')} Você não escreveu nada. Conte sua dúvida, por exemplo: "
            "“perdi a comanda e querem me cobrar multa”.")
        return {}
    if res.tipo == "INVALIDA":
        if {"oi", "ola", "bom", "boa", "tudo", "obrigado", "obrigada"} & set(consulta.lower().split()):
            t.p("Olá! Me conte o que aconteceu, do seu jeito. Ex.: “o mercado cobrou mais caro no "
                "caixa” ou “meu voo atrasou”. Ou digite [1] para ver os temas.")
            return {}
        t.p(f"{t.i('erro')} Não consegui entender. Escreva com palavras, por exemplo: "
            "“meu voo atrasou”. Ou digite [1] para ver todos os temas.")
        return {}
    if res.tipo == "FORA_DO_TEMA":
        t.p(f"{t.i('info')} {base.meta.get('fora_do_escopo')}")
        if exp:
            t.p(f"{t.i('info')} {exp}")
        return {}
    if res.tipo == "SEM_RESPOSTA":
        t.p(f"{t.i('limite')} Não encontrei uma informação confiável para isso, então prefiro "
            "não chutar uma resposta.")
        t.p("Tente explicar com outras palavras (o que aconteceu, onde e com quem) ou digite [1] "
            "para ver as situações que eu conheço. Para casos fora da lista, procure o Procon "
            "da sua cidade ou o consumidor.gov.br.")
        if exp:
            t.p(f"{t.i('info')} {exp}")
        return {}
    if res.tipo == "AMBIGUA":
        t.p("Sua pergunta combina com mais de uma situação. Qual delas é a sua?")
        mapa = {}
        for letra, rid in zip("abc", res.ids):
            t.p(f"[{letra}] {base.registros[rid]['titulo']}", 3)
            mapa[letra] = ("abrir", rid)
        t.p("[n] Nenhuma dessas")
        mapa["n"] = ("nenhuma", None)
        if exp:
            t.p(f"{t.i('info')} {exp}")
        return mapa

    rid = res.ids[0]
    mostrar_registro(t, base, rid, exp)
    return opcoes_pos_resposta(t, base, rid, interativo)


# ---------------------------------------------------------------- programa
def argumentos():
    ap = argparse.ArgumentParser(description="Citizen Assist AI — direitos do consumidor no dia a dia.")
    ap.add_argument("--base", default=BASE_PADRAO, help="caminho do JSON da base (padrão: data/base.json)")
    ap.add_argument("--sinonimos", default=SINONIMOS_PADRAO, help="caminho do JSON de sinônimos")
    ap.add_argument("--estrategia", choices=ESTRATEGIAS, default="hibrida", help="estratégia de busca")
    ap.add_argument("--simples", action="store_true", help="usa separadores simples para compatibilidade com terminais antigos")
    ap.add_argument("--explicar", action="store_true", help="mostra as notas da busca em cada resposta")
    ap.add_argument("--pergunta", help="responde uma única pergunta e encerra (modo não interativo)")
    return ap.parse_args()


def main():
    args = argumentos()
    t = Tela(preparar_console(args.simples))

    try:
        base = Base(args.base, args.sinonimos)
    except ErroBase as e:
        t.p(f"{t.i('erro')} Não consegui carregar a base de conhecimento.")
        t.p(str(e), 3)
        t.p("Confira se o arquivo existe, não está vazio e é um JSON válido "
            "(veja o modelo em data/base.json).", 3)
        return 1

    for aviso in base.avisos:
        t.p(f"{t.i('limite')} {aviso}")
    buscador = Buscador(base)

    if args.pergunta is not None:
        responder(t, base, buscador, args.pergunta, args.estrategia, args.explicar, interativo=False)
        return 0

    def entrada(prompt):
        try:
            return input(prompt)
        except EOFError:
            raise KeyboardInterrupt

    t.linha()
    t.p(f"{t.i('titulo')} CITIZEN ASSIST AI")
    t.linha()
    t.p(f"{t.i('aviso')} Não sou canal oficial do governo. Respondo com base em leis e normas "
        "públicas, sempre com a fonte. Não digite dados pessoais.")
    menu(t)

    explicar = args.explicar
    atalhos = {}
    try:
        while True:
            t.p()
            texto = entrada("Sua dúvida › ").strip()
            chave = texto.lower()

            if chave in ("0", "sair"):
                break
            if chave in atalhos:
                acao, alvo = atalhos[chave]
                if acao == "abrir":
                    mostrar_registro(t, base, alvo)
                    atalhos = opcoes_pos_resposta(t, base, alvo)
                elif acao == "tema":
                    atalhos = listar_situacoes(t, base, alvo)
                elif acao == "verificar":
                    verificar_condicoes(t, base, alvo, entrada)
                    atalhos = opcoes_pos_resposta(t, base, alvo)
                elif acao == "nenhuma":
                    t.p("Tudo bem. Tente descrever de outro jeito ou digite [1] para ver a lista.")
                    atalhos = {}
                continue
            if chave in ("m", "menu"):
                menu(t)
                atalhos = {}
                continue
            if chave == "1":
                atalhos = listar_temas(t, base)
                continue
            if chave == "2":
                sobre(t, base, args.estrategia)
                continue
            if chave == "3":
                explicar = not explicar
                t.p(f"Modo explicação {'LIGADO' if explicar else 'DESLIGADO'}.")
                continue
            if chave.isdigit() or (len(chave) <= 3 and chave[:1] in "rstv" and chave[1:].isdigit()):
                t.p(f"{t.i('erro')} Opção “{texto}” não existe aqui. Digite [m] para ver o menu.")
                continue
            atalhos = responder(t, base, buscador, texto, args.estrategia, explicar)
    except KeyboardInterrupt:
        print()
    t.p("Até logo! Lembre-se: na dúvida, procure o Procon da sua cidade.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
