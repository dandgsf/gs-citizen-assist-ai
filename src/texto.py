"""Tratamento de texto: normalização, tokens, sinônimos e radicais.

Tudo em Python puro (sem bibliotecas externas) para rodar em qualquer máquina.
"""
import re
import unicodedata

# Palavras muito comuns que não ajudam a achar o assunto.
# Inclui palavras "de domínio" que aparecem em quase toda pergunta
# (direito, lei, consumidor...), por isso não distinguem um registro do outro.
# "não" e "sem" NÃO são descartadas: mudam o sentido ("não pedi", "sem pedir").
STOPWORDS = {
    "a", "o", "as", "os", "um", "uma", "uns", "umas", "de", "do", "da", "dos", "das",
    "em", "no", "na", "nos", "nas", "por", "pelo", "pela", "pelos", "pelas", "para",
    "pra", "pro", "com", "e", "ou", "mas", "se", "que", "quem", "qual", "quais",
    "como", "quando", "onde", "porque", "pq", "eu", "me", "mim", "meu", "minha", "meus",
    "minhas", "voce", "voces", "vc", "ele", "ela", "eles", "elas", "lhe", "isso", "isto",
    "esse", "essa", "este", "esta", "aquele", "aquela", "ao", "aos", "ja", "sim",
    "mais", "muito", "muita", "so", "tambem", "ainda", "agora", "aqui", "la", "foi",
    "ser", "sou", "estou", "esta", "estao", "era", "tem", "tenho", "tinha", "ter", "ha",
    "fazer", "faco", "fiz", "posso", "pode", "podem", "devo", "deve", "preciso", "quero",
    "queria", "gostaria", "sobre", "algo", "coisa", "alguma", "algum", "todo", "toda",
    "direito", "direitos", "lei", "leis", "consumidor", "obrigado", "obrigada", "oi",
    "ola", "bom", "boa", "dia", "tarde", "noite", "favor", "ajuda", "ajudar", "duvida",
    "saber", "certo", "errado", "entao", "ai", "tipo", "ne", "dele", "dela", "faz", "ate",
    "nada", "hoje", "ontem", "tudo", "bem", "beleza", "ta", "to", "tava", "aquilo", "la",
}

TOKEN_RE = re.compile(r"[a-z0-9]+")
TAMANHO_RADICAL = 6


def sem_acentos(texto: str) -> str:
    """Remove acentos: 'cobrança' -> 'cobranca'."""
    decomposto = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in decomposto if not unicodedata.combining(c))


def normalizar(texto: str) -> str:
    """Minúsculas e sem acentos."""
    return sem_acentos(texto or "").lower()


def tokens(texto: str) -> list:
    """Quebra o texto em palavras normalizadas (com stopwords)."""
    return TOKEN_RE.findall(normalizar(texto))


def radical(palavra: str) -> str:
    """Radical simples por prefixo: 'cancelamento' e 'cancelar' -> 'cancel'.

    É uma aproximação barata de stemming. Funciona bem para o português do dia a dia
    e é fácil de explicar. Números ficam como estão.
    """
    if palavra.isdigit():
        return palavra
    return palavra[:TAMANHO_RADICAL]


def termos(texto: str, sinonimos: dict) -> list:
    """Pipeline completo: normaliza -> tira stopwords -> aplica sinônimos -> radical.

    Retorna uma LISTA (mantém repetições, útil para TF-IDF).
    """
    saida = []
    for t in tokens(texto):
        t = sinonimos.get(t, t)
        if t in STOPWORDS or (len(t) < 2 and not t.isdigit()):
            continue
        saida.append(radical(t))
    return saida
