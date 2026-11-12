"""Proteção de dados pessoais na entrada.

O Citizen Assist AI não precisa de nenhum dado pessoal. Se a pessoa digitar
CPF, telefone, e-mail ou número de cartão, o sistema avisa e mascara o dado
antes de qualquer processamento. Nada é gravado em disco.
"""
import re

PADROES = {
    "CPF": re.compile(r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b"),
    "cartão": re.compile(r"\b(?:\d[ -]?){13,19}\b"),
    "e-mail": re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b"),
    "telefone": re.compile(r"(?:\+?55\s?)?\(?\b\d{2}\)?\s?9?\d{4}[-\s]?\d{4}\b"),
}


def mascarar(texto: str):
    """Retorna (texto_mascarado, lista_de_tipos_encontrados)."""
    encontrados = []
    for nome, padrao in PADROES.items():
        if padrao.search(texto):
            encontrados.append(nome)
            texto = padrao.sub("[removido]", texto)
    return texto, encontrados
