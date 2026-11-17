"""Busca na base: três estratégias comparáveis e a regra de decisão.

Estratégias
-----------
1. "palavras"  – casamento de palavras-chave e frases-chave (com sinônimos e radicais).
                Rápida e fácil de explicar; frases inteiras valem mais que palavras soltas.
2. "tfidf"     – TF-IDF + similaridade do cosseno, implementado em Python puro.
                Dá mais peso a palavras raras (ex.: "comanda") do que a comuns (ex.: "conta").
3. "hibrida"   – média das duas notas. É a estratégia padrão do sistema
                (escolhida pelos resultados de docs/resultados_testes.md).

Regra de decisão (o que fazer com as notas)
-------------------------------------------
- entrada vazia                         -> VAZIA
- só símbolos/palavras vazias           -> INVALIDA
- nenhuma palavra conhecida pela base   -> FORA_DO_TEMA
- melhor nota abaixo do limiar          -> SEM_RESPOSTA  (não inventa: avisa)
- 2º colocado muito perto do 1º         -> AMBIGUA       (mostra as opções e pergunta)
- setor/fornecedor incompatível         -> SEM_RESPOSTA  (evita erro perigoso entre setores)
- caso contrário                        -> RESPOSTA
"""
import math
import time
from collections import Counter
from dataclasses import dataclass, field

from texto import termos, normalizar, tokens, radical

ESTRATEGIAS = ("palavras", "tfidf", "hibrida")

# Limiar mínimo de confiança por estratégia e razão de empate (2º/1º) para ambiguidade.
# Calibrados com data/perguntas_teste.json (ver docs/resultados_testes.md).
LIMIAR = {"palavras": 0.40, "tfidf": 0.20, "hibrida": 0.31}
RAZAO_AMBIGUIDADE = 0.85
# Penalidade por palavra da pergunta que não casou com nada do registro.
PESO_SOBRA = 0.35

# Contexto setorial para DB20 (Telecomunicações / Anatel):
# distingue objeto/prestadora do contrato de saudação ("oi, ...") e canal digital ("pela internet").
MARCAS_TELECOM = {"vivo", "claro", "tim", "sky", "anatel"}
PREPOSICOES_MARCA_OI = {
    "da", "de", "na", "no", "pela", "pelo", "operadora", "linha", "plano", "chip",
    "internet", "tv", "fibra",
}
SERVICOS_TELECOM_DIRETOS = {
    "celular", "telefonia", "telefone", "chip", "fibra", "banda", "wifi", "operadora", "tv",
}
PREPOSICOES_CANAL = {"pela", "na", "via", "por"}
INCOMPATIVEIS_TELECOM = {
    "academ", "escola", "curso", "faculd", "clube", "saude", "conven",
    "ginasi", "pilate", "crossf",
}


@dataclass
class Resultado:
    tipo: str                         # RESPOSTA | AMBIGUA | SEM_RESPOSTA | FORA_DO_TEMA | VAZIA | INVALIDA
    ids: list = field(default_factory=list)      # candidatos em ordem de nota
    notas: list = field(default_factory=list)
    estrategia: str = "hibrida"
    tempo_ms: float = 0.0
    termos_consulta: list = field(default_factory=list)


class Buscador:
    def __init__(self, base):
        self.base = base
        self.sin = base.sinonimos
        self.fora_escopo = {normalizar(t) for t in base.meta.get("termos_fora_do_escopo", [])}
        self.frases = {}      # id -> lista de frases-chave (cada uma = conjunto de radicais)
        self.fracos = {}      # id -> radicais de título e perguntas de exemplo
        docs = {}             # id -> lista de radicais (para TF-IDF)

        for rid, reg in base.registros.items():
            ppc = reg["pergunta_ou_palavras_chave"]
            frases = [set(termos(f, self.sin)) for f in ppc.get("palavras_chave", [])]
            self.frases[rid] = [f for f in frases if f]
            titulo = termos(reg.get("titulo", ""), self.sin)
            exemplos = [t for p in ppc.get("perguntas_exemplo", []) for t in termos(p, self.sin)]
            self.fracos[rid] = set(titulo) | set(exemplos)
            chave = [t for f in ppc.get("palavras_chave", []) for t in termos(f, self.sin)]
            # Título e palavras-chave pesam o dobro dos exemplos.
            docs[rid] = titulo * 2 + chave * 2 + exemplos

        # ----- índice TF-IDF -----
        n = len(docs)
        df = Counter()
        for lista in docs.values():
            df.update(set(lista))
        self.idf = {t: math.log((1 + n) / (1 + d)) + 1 for t, d in df.items()}
        # Palavra que não existe na base recebe o maior peso possível (é "rara"):
        # assim, perguntas cheias de palavras desconhecidas ficam com nota baixa.
        self.idf_desconhecida = math.log(1 + n) + 1
        self.vetores = {}
        for rid, lista in docs.items():
            tf = Counter(lista)
            vet = {t: (c / len(lista)) * self.idf[t] for t, c in tf.items()}
            norma = math.sqrt(sum(v * v for v in vet.values())) or 1.0
            self.vetores[rid] = {t: v / norma for t, v in vet.items()}
        self.vocabulario = set(self.idf)
        self.df = df
        self.docs = {rid: set(lista) for rid, lista in docs.items()}

    # ---------------- estratégias ----------------
    def _nota_palavras(self, q: set, rid: str) -> float:
        bruto, cobertos = 0.0, set()
        for frase in self.frases[rid]:
            if frase <= q:                      # todas as palavras da frase estão na pergunta
                bruto += len(frase)             # frase de 2 palavras vale 2, de 1 vale 1
                cobertos |= frase
        fracos = (q - cobertos) & self.fracos[rid]
        bruto += 0.5 * len(fracos)
        sobra = len(q - cobertos - fracos)
        return bruto / (bruto + PESO_SOBRA * sobra + 1.0)

    def _nota_tfidf(self, q_lista: list, rid: str) -> float:
        if not any(t in self.idf for t in q_lista):
            return 0.0
        tf = Counter(q_lista)
        vet = {t: (c / len(q_lista)) * self.idf.get(t, self.idf_desconhecida) for t, c in tf.items()}
        norma = math.sqrt(sum(v * v for v in vet.values())) or 1.0
        doc = self.vetores[rid]
        return sum((v / norma) * doc.get(t, 0.0) for t, v in vet.items())

    def _tem_entidade_incompativel_telecom(self, consulta: str) -> bool:
        radicais = {radical(t) for t in tokens(consulta) if len(t) >= 2 or t.isdigit()}
        return bool(radicais & INCOMPATIVEIS_TELECOM)

    def _setor_compativel(self, rid: str, consulta: str) -> bool:
        if rid != "DB20":
            return True
        toks = tokens(consulta)
        tem_incompativel = self._tem_entidade_incompativel_telecom(consulta)

        # 1. Prestadora explícita (ignorando "oi" quando usado como saudação inicial)
        tem_marca = bool(set(toks) & MARCAS_TELECOM)
        for i, t in enumerate(toks):
            if t == "oi" and i > 0 and toks[i - 1] in PREPOSICOES_MARCA_OI:
                tem_marca = True

        # 2. Objeto/serviço explícito de telecomunicações (ignorando "pela/na/via internet" como canal)
        tem_servico = bool(set(toks) & SERVICOS_TELECOM_DIRETOS)
        for i, t in enumerate(toks):
            if t == "internet" and (i == 0 or toks[i - 1] not in PREPOSICOES_CANAL):
                tem_servico = True

        tem_telecom = tem_marca or tem_servico
        if tem_incompativel and not tem_telecom:
            return False
        if not tem_telecom:
            return False
        return True

    def notas(self, consulta: str, estrategia: str = "hibrida") -> list:
        """Lista [(nota, id)] em ordem decrescente."""
        q_lista = termos(consulta, self.sin)
        q = set(q_lista)
        saida = []
        for rid in self.base.registros:
            if estrategia == "palavras":
                s = self._nota_palavras(q, rid)
            elif estrategia == "tfidf":
                s = self._nota_tfidf(q_lista, rid)
            else:
                s = 0.5 * self._nota_palavras(q, rid) + 0.5 * self._nota_tfidf(q_lista, rid)
            saida.append((round(s, 4), rid))
        saida.sort(key=lambda x: (-x[0], x[1]))
        return saida

    # ---------------- decisão ----------------
    def buscar(self, consulta: str, estrategia: str = "hibrida") -> Resultado:
        inicio = time.perf_counter()
        res = self._decidir(consulta, estrategia)
        res.tempo_ms = (time.perf_counter() - inicio) * 1000
        res.estrategia = estrategia
        return res

    def _decidir(self, consulta, estrategia) -> Resultado:
        if consulta is None or not consulta.strip():
            return Resultado("VAZIA")
        q_lista = termos(consulta, self.sin)
        if not q_lista:
            return Resultado("INVALIDA")
        conhecidos = [t for t in q_lista if t in self.vocabulario]
        palavras = set(tokens(consulta))
        if not conhecidos:
            return Resultado("FORA_DO_TEMA", termos_consulta=q_lista)

        ranking = self.notas(consulta, estrategia)
        (n1, id1) = ranking[0]
        limiar = LIMIAR[estrategia]

        if palavras & self.fora_escopo and n1 < limiar * 2:
            return Resultado("FORA_DO_TEMA", [id1], [n1], termos_consulta=q_lista)
        if n1 < limiar:
            return Resultado("SEM_RESPOSTA", [id1], [n1], termos_consulta=q_lista)

        # Pergunta de UMA palavra que aparece em vários registros ("cancelar", "cobrança"):
        # preserva esclarecimento genérico, mas exclui registros explicitamente incompatíveis.
        unicos = set(q_lista)
        if len(unicos) == 1:
            termo = next(iter(unicos))
            if self.df.get(termo, 0) >= 2:
                incomp_telecom = self._tem_entidade_incompativel_telecom(consulta)
                cand = [
                    (n, r) for n, r in ranking
                    if termo in self.docs[r] and not (incomp_telecom and r == "DB20")
                ][:3]
                if len(cand) >= 2:
                    return Resultado("AMBIGUA", [r for _, r in cand], [n for n, _ in cand],
                                     termos_consulta=q_lista)
                if len(cand) == 1:
                    return Resultado("RESPOSTA", [cand[0][1]], [cand[0][0]],
                                     termos_consulta=q_lista)
                return Resultado("SEM_RESPOSTA", [id1], [n1], termos_consulta=q_lista)

        # Filtra candidatos setorialmente incompatíveis ANTES de avaliar ambiguidade ou resposta,
        # impedindo que DB20 apareça nas opções [a]/[b]/[c] para consultas de academia ou cursos.
        compativeis = [(n, r) for n, r in ranking if self._setor_compativel(r, consulta)]
        if not compativeis or compativeis[0][0] < limiar:
            return Resultado("SEM_RESPOSTA", [id1], [n1], termos_consulta=q_lista)

        n1_c, id1_c = compativeis[0]
        n2_c, id2_c = (compativeis[1] if len(compativeis) > 1 else (0.0, None))
        if n2_c >= limiar and n2_c >= RAZAO_AMBIGUIDADE * n1_c:
            candidatos = [
                (n, r) for n, r in compativeis[:3]
                if n >= limiar and n >= RAZAO_AMBIGUIDADE * n1_c
            ]
            return Resultado("AMBIGUA", [r for _, r in candidatos], [n for n, _ in candidatos],
                             termos_consulta=q_lista)
        ids_resp = [id1_c, id2_c] if id2_c is not None else [id1_c]
        notas_resp = [n1_c, n2_c] if id2_c is not None else [n1_c]
        return Resultado("RESPOSTA", ids_resp, notas_resp, termos_consulta=q_lista)
    