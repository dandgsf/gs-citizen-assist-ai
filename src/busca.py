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
MARCAS_NO_CANAL = MARCAS_TELECOM | {"oi"}
PREPOSICOES_MARCA_OI = {
    "da", "de", "na", "no", "pela", "pelo", "operadora", "linha", "plano", "chip",
    "internet", "tv", "fibra",
}
SERVICOS_TELECOM = {"internet", "celular", "telefone", "tv", "operadora", "telefonia",
                    "chip", "fibra", "banda", "wifi"}
CANAIS_DIGITAIS = {"online", "ecommerce", "marketplace"}
CANAIS_CONTATO = {"whatsapp", "site", "aplicativo", "portal", "chat"}
INTRODUZEM_CANAL = {"pela", "pelo", "na", "no", "via", "por", "usando"}
INTENCAO_CANCELAR = {"cancel", "encerr", "desist", "rescin"}
TERMOS_GENERICOS_CONTRATO = {"plano", "contra", "assina", "servic"}
OUTROS_SERVICOS = {"academ", "escola", "curso", "faculd", "clube", "saude", "conven",
                  "ginasi", "pilate", "crossf"}


@dataclass
class Resultado:
    tipo: str                         # RESPOSTA | AMBIGUA | SEM_RESPOSTA | FORA_DO_TEMA | VAZIA | INVALIDA
    ids: list = field(default_factory=list)      # candidatos em ordem de nota
    notas: list = field(default_factory=list)
    estrategia: str = "hibrida"
    tempo_ms: float = 0.0
    termos_consulta: list = field(default_factory=list)
    confirmar: str | None = None     # registro que exige confirmação antes da orientação
    esclarecer_servico: bool = False


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

    def sem_canal_de_contato(self, toks: list) -> list:
        """Retira expressões como 'pelo meu celular da Vivo', preservando o objeto do contrato."""
        restantes = []
        fim_canal = 0
        for i, t in enumerate(toks):
            if i < fim_canal:
                continue
            nome = self.sin.get(t, t)
            if nome not in CANAIS_CONTATO and nome not in SERVICOS_TELECOM:
                continue
            inicio = i
            while inicio > fim_canal and toks[inicio - 1] in {"meu", "minha", "seu", "sua", "a", "o"}:
                inicio -= 1
            if inicio > fim_canal and toks[inicio - 1] in INTRODUZEM_CANAL:
                inicio -= 1
            elif nome not in CANAIS_CONTATO:
                continue
            restantes.extend(toks[fim_canal:inicio])
            fim_canal = i + 1
            if fim_canal < len(toks) and toks[fim_canal] == "oficial":
                fim_canal += 1
            marca = fim_canal
            if marca < len(toks) and toks[marca] in {"da", "do", "de"}:
                marca += 1
            if marca < len(toks) and toks[marca] == "operadora":
                marca += 1
                fim_canal = marca
            if marca < len(toks) and toks[marca] in MARCAS_NO_CANAL:
                fim_canal = marca + 1
        return restantes + toks[fim_canal:]

    def tem_servico_telecom(self, toks: list) -> bool:
        """Procura o serviço ou a prestadora nos termos que descrevem o contrato."""
        return self._telecom_no_contrato(self.sem_canal_de_contato(toks))

    def _telecom_no_contrato(self, toks: list) -> bool:
        for i, t in enumerate(toks):
            anterior = toks[i - 1] if i else ""
            if t in MARCAS_TELECOM or (t == "oi" and anterior in PREPOSICOES_MARCA_OI):
                return True
            if t in CANAIS_DIGITAIS:
                continue
            if t in SERVICOS_TELECOM or self.sin.get(t) in SERVICOS_TELECOM:
                # Em "curso de internet", o objeto do contrato é o curso.
                if i >= 2 and anterior == "de" and radical(toks[i - 2]) in OUTROS_SERVICOS:
                    continue
                return True
        return False

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
        palavras = tokens(consulta)
        if not conhecidos:
            return Resultado("FORA_DO_TEMA", termos_consulta=q_lista)

        objeto = self.sem_canal_de_contato(palavras)
        telecom = self._telecom_no_contrato(objeto)
        unicos = set(q_lista)
        cancelar = bool(INTENCAO_CANCELAR & unicos)
        if cancelar and objeto != palavras:
            consulta = " ".join(objeto)
            especificos = set(termos(consulta, self.sin)) - INTENCAO_CANCELAR - TERMOS_GENERICOS_CONTRATO
            if not telecom and not especificos.intersection(self.vocabulario | OUTROS_SERVICOS):
                return Resultado("SEM_RESPOSTA", termos_consulta=q_lista, esclarecer_servico=True)
        ranking = self.notas(consulta, estrategia)
        outro_servico = bool(OUTROS_SERVICOS & unicos) and not telecom
        if len(unicos) > 1 and not telecom:
            ranking = [(n, r) for n, r in ranking if r != "DB20"]
        if cancelar and outro_servico:
            # "Cancelar o curso" compartilha apenas o verbo com "voo cancelado".
            contexto = unicos - INTENCAO_CANCELAR
            ranking = [(n, r) for n, r in ranking if contexto & self.docs[r]]
        if not ranking:
            return Resultado("SEM_RESPOSTA", termos_consulta=q_lista)
        (n1, id1) = ranking[0]
        limiar = LIMIAR[estrategia]

        if self.fora_escopo.intersection(palavras) and n1 < limiar * 2:
            return Resultado("FORA_DO_TEMA", [id1], [n1], termos_consulta=q_lista)
        canal_digital = bool({"intern", "site", "aplica", "whatsa", "portal", "chat"} & unicos)
        if cancelar and outro_servico and canal_digital and "DB07" in self.base.registros:
            return Resultado("SEM_RESPOSTA", termos_consulta=q_lista, confirmar="DB07")
        if n1 < limiar:
            return Resultado("SEM_RESPOSTA", [id1], [n1], termos_consulta=q_lista)

        # Pergunta de UMA palavra que aparece em vários registros ("cancelar", "cobrança"):
        # preserva as opções de esclarecimento quando só se conhece a intenção.
        if len(unicos) == 1:
            termo = next(iter(unicos))
            if self.df.get(termo, 0) >= 2:
                cand = [
                    (n, r) for n, r in ranking
                    if termo in self.docs[r]
                ][:3]
                if len(cand) >= 2:
                    return Resultado("AMBIGUA", [r for _, r in cand], [n for n, _ in cand],
                                     termos_consulta=q_lista)
                if len(cand) == 1:
                    return Resultado("RESPOSTA", [cand[0][1]], [cand[0][0]],
                                     termos_consulta=q_lista)
                return Resultado("SEM_RESPOSTA", [id1], [n1], termos_consulta=q_lista)

        n2, id2 = ranking[1] if len(ranking) > 1 else (0.0, None)
        # O canal do cancelamento não comprova o local nem a data da contratação.
        if id1 == "DB07" and cancelar:
            return Resultado("SEM_RESPOSTA", termos_consulta=q_lista, confirmar="DB07")
        if n2 >= limiar and n2 >= RAZAO_AMBIGUIDADE * n1:
            candidatos = [
                (n, r) for n, r in ranking[:3]
                if n >= limiar and n >= RAZAO_AMBIGUIDADE * n1
            ]
            return Resultado("AMBIGUA", [r for _, r in candidatos], [n for n, _ in candidatos],
                             termos_consulta=q_lista)
        ids_resp = [id1, id2] if id2 is not None else [id1]
        notas_resp = [n1, n2] if id2 is not None else [n1]
        return Resultado("RESPOSTA", ids_resp, notas_resp, termos_consulta=q_lista)
