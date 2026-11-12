"""Leitura e validação da base de conhecimento (data/base.json).

A base pode ser editada sem mexer no código: este módulo confere cada registro,
descarta os inválidos com um aviso claro e monta as estruturas usadas pela busca:
  - dicionário id -> registro
  - hierarquia tema -> lista de ids
  - grafo de assuntos relacionados (lista de adjacência, não direcionado)
"""
import json
import os
from collections import deque
from datetime import date, datetime

CAMPOS_OBRIGATORIOS = (
    "identificador",
    "tema",
    "pergunta_ou_palavras_chave",
    "orientacao_resumida",
    "referencia",
    "data_de_verificacao",
)


class ErroBase(Exception):
    """Problema que impede o uso da base (arquivo ausente, vazio ou ilegível)."""


def carregar_json(caminho: str) -> dict:
    if not os.path.exists(caminho):
        raise ErroBase(f"Arquivo não encontrado: {caminho}")
    if os.path.getsize(caminho) == 0:
        raise ErroBase(f"O arquivo está vazio: {caminho}")
    try:
        with open(caminho, encoding="utf-8") as f:
            dados = json.load(f)
    except json.JSONDecodeError as e:
        raise ErroBase(f"JSON inválido em {caminho} (linha {e.lineno}, coluna {e.colno}): {e.msg}")
    if not isinstance(dados, dict):
        raise ErroBase(f"Formato inesperado em {caminho}: o arquivo deve conter um objeto JSON.")
    return dados


def _validar_registro(reg, temas_validos: set) -> list:
    """Devolve a lista de problemas encontrados (vazia = registro válido)."""
    if not isinstance(reg, dict):
        return ["registro não é um objeto JSON"]
    problemas = []
    for campo in CAMPOS_OBRIGATORIOS:
        valor = reg.get(campo)
        if valor in (None, "", [], {}):
            problemas.append(f"campo obrigatório ausente ou vazio: '{campo}'")
    if problemas:
        return problemas

    if temas_validos and reg["tema"] not in temas_validos:
        problemas.append(f"tema '{reg['tema']}' não está na lista de temas")

    ppc = reg["pergunta_ou_palavras_chave"]
    if not isinstance(ppc, dict) or not (ppc.get("palavras_chave") or ppc.get("perguntas_exemplo")):
        problemas.append("'pergunta_ou_palavras_chave' precisa ter 'palavras_chave' ou 'perguntas_exemplo'")

    ref = reg["referencia"]
    if not isinstance(ref, dict) or not ref.get("norma"):
        problemas.append("'referencia' precisa ter o campo 'norma'")
    elif ref.get("url") and not str(ref["url"]).startswith(("http://", "https://")):
        problemas.append("'referencia.url' deve começar com http:// ou https://")

    try:
        datetime.strptime(reg["data_de_verificacao"], "%Y-%m-%d")
    except (TypeError, ValueError):
        problemas.append("'data_de_verificacao' deve estar no formato AAAA-MM-DD")

    cond = reg.get("condicoes")
    if cond is not None:
        if cond.get("regra") not in ("todas", "alguma"):
            problemas.append("'condicoes.regra' deve ser 'todas' ou 'alguma'")
        if not cond.get("itens"):
            problemas.append("'condicoes.itens' não pode ser vazio")
    return problemas


class Base:
    def __init__(self, caminho_base: str, caminho_sinonimos: str | None = None):
        self.avisos = []           # problemas não fatais, mostrados ao iniciar
        dados = carregar_json(caminho_base)
        self.meta = dados.get("meta", {})
        self.temas = list(dados.get("temas", []))
        brutos = dados.get("registros")
        if not brutos:
            raise ErroBase("A base não tem nenhum registro em 'registros'.")

        self.registros = {}        # id -> registro
        temas_validos = set(self.temas)
        for i, reg in enumerate(brutos, start=1):
            problemas = _validar_registro(reg, temas_validos)
            rid = reg.get("identificador", f"#{i}") if isinstance(reg, dict) else f"#{i}"
            if not problemas and rid in self.registros:
                problemas.append("identificador repetido")
            if problemas:
                self.avisos.append(f"Registro {rid} ignorado: " + "; ".join(problemas))
                continue
            self.registros[rid] = reg

        if not self.registros:
            raise ErroBase("Nenhum registro válido na base. Corrija os avisos acima.")

        # Temas sem lista explícita: deduz a partir dos registros
        if not self.temas:
            self.temas = sorted({r["tema"] for r in self.registros.values()})

        # Hierarquia: tema -> [ids]
        self.por_tema = {t: [] for t in self.temas}
        for rid, reg in self.registros.items():
            self.por_tema.setdefault(reg["tema"], []).append(rid)

        # Grafo não direcionado de assuntos relacionados
        self.grafo = {rid: set() for rid in self.registros}
        for rid, reg in self.registros.items():
            for viz in reg.get("relacionados", []):
                if viz in self.grafo and viz != rid:
                    self.grafo[rid].add(viz)
                    self.grafo[viz].add(rid)
                elif viz not in self.grafo:
                    self.avisos.append(f"Registro {rid}: relacionado '{viz}' não existe (ignorado)")

        # Registros com verificação antiga
        validade = int(self.meta.get("validade_dias", 180))
        hoje = date.today()
        for rid, reg in self.registros.items():
            dv = datetime.strptime(reg["data_de_verificacao"], "%Y-%m-%d").date()
            if (hoje - dv).days > validade:
                self.avisos.append(
                    f"Registro {rid} foi verificado há mais de {validade} dias ({dv:%d/%m/%Y}); revise a fonte."
                )

        self.sinonimos = {}
        if caminho_sinonimos and os.path.exists(caminho_sinonimos):
            try:
                sin = carregar_json(caminho_sinonimos)
                self.sinonimos = {k: v for k, v in sin.items() if not k.startswith("_")}
            except ErroBase as e:
                self.avisos.append(f"Sinônimos não carregados: {e}")

    # ---------- navegação ----------
    def relacionados(self, rid: str) -> list:
        """Vizinhos diretos no grafo, na ordem declarada no registro e depois os demais."""
        declarados = [r for r in self.registros[rid].get("relacionados", []) if r in self.grafo]
        extras = sorted(self.grafo[rid] - set(declarados))
        return declarados + extras

    def caminho(self, origem: str, destino: str) -> list:
        """Busca em largura (BFS): menor sequência de assuntos ligando dois registros."""
        if origem not in self.grafo or destino not in self.grafo:
            return []
        anterior = {origem: None}
        fila = deque([origem])
        while fila:
            atual = fila.popleft()
            if atual == destino:
                break
            for viz in sorted(self.grafo[atual]):
                if viz not in anterior:
                    anterior[viz] = atual
                    fila.append(viz)
        if destino not in anterior:
            return []
        rota, no = [], destino
        while no is not None:
            rota.append(no)
            no = anterior[no]
        return rota[::-1]
