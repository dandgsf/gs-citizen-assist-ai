"""Regressões de BUS-01 na interface que a pessoa realmente vê."""
import json
from pathlib import Path
import subprocess
import sys
import unittest


RAIZ = Path(__file__).resolve().parents[1]
BASE = json.loads((RAIZ / "data/base.json").read_text(encoding="utf-8"))
TITULOS = {r["identificador"]: r["titulo"].casefold() for r in BASE["registros"]}
ESTRATEGIAS = ("palavras", "tfidf", "hibrida")


def executar(estrategia, *argumentos, entradas=()):
    processo = subprocess.run(
        [sys.executable, "-X", "utf8", str(RAIZ / "src/sistema.py"),
         "--simples", "--estrategia", estrategia, *argumentos],
        input="\n".join(entradas) + "\n", capture_output=True,
        encoding="utf-8", check=True, timeout=10,
    )
    return " ".join(processo.stdout.casefold().split())


class CancelamentoCLI(unittest.TestCase):
    def test_banda_larga_e_tamanho_de_roupa(self):
        casos = (
            ("Quero encerrar meu contrato de banda larga residencial", "DB20"),
            ("Quero encerrar a banda larga", "DB20"),
            ("Preciso encerrar meu plano de internet", "DB20"),
            ("A camisa ficou larga e a loja não quer trocar o tamanho", "DB04"),
        )
        for pergunta, esperado in casos:
            for estrategia in ESTRATEGIAS:
                with self.subTest(pergunta=pergunta, estrategia=estrategia):
                    saida = executar(estrategia, "--pergunta", pergunta)
                    self.assertIn("== " + TITULOS[esperado], saida)

    def test_banda_larga_como_canal(self):
        for estrategia in ESTRATEGIAS:
            with self.subTest(estrategia=estrategia):
                saida = executar(estrategia, "--pergunta", "Quero encerrar o plano da academia pela banda larga da Vivo")
                self.assertNotIn(TITULOS["DB20"], saida)
                self.assertNotIn("mostre na tela ou fale", saida)

    def test_contrato_de_banda_musical(self):
        for estrategia in ESTRATEGIAS:
            with self.subTest(estrategia=estrategia):
                saida = executar(estrategia, "--pergunta", "Quero encerrar meu contrato com a banda que vai tocar")
                self.assertNotIn(TITULOS["DB20"], saida)
                self.assertNotIn("mostre na tela ou fale", saida)

    def test_resposta_e_atalhos(self):
        casos = json.loads((RAIZ / "data/perguntas_teste.json").read_text(encoding="utf-8"))
        for caso in casos["casos"]:
            if caso["categoria"] != "regressao_setor":
                continue
            for estrategia in ESTRATEGIAS:
                with self.subTest(caso=caso["id"], estrategia=estrategia):
                    saida = executar(estrategia, "--pergunta", caso["pergunta"])
                    for rid in caso.get("nao_deve_conter", []):
                        self.assertNotIn(TITULOS[rid], saida)
                    if caso["esperado"] == "SEM_RESPOSTA":
                        self.assertNotIn("mostre na tela ou fale", saida)
                    else:
                        self.assertIn("== " + TITULOS[caso["esperado"]], saida)

    def test_contratacao_antes_da_orientacao(self):
        pergunta = "Quero cancelar minha assinatura de curso online"
        for estrategia in ESTRATEGIAS:
            for respostas in [("s", "s"), ("s", "n"), ("n", "s"), ("s", "?")]:
                with self.subTest(estrategia=estrategia, respostas=respostas):
                    saida = executar(estrategia, entradas=(pergunta, "v", *respostas, "0"))
                    antes, depois = saida.split("assinou o contrato)?", 1)
                    self.assertIn("fora da loja física", antes)
                    self.assertNotIn(TITULOS["DB07"], antes)
                    self.assertNotIn("mostre na tela ou fale", antes)
                    self.assertEqual(TITULOS["DB07"] in depois, respostas == ("s", "s"))
                    self.assertEqual("mostre na tela ou fale" in depois, respostas == ("s", "s"))

    def test_cancelar_sem_contexto(self):
        for estrategia in ESTRATEGIAS:
            with self.subTest(estrategia=estrategia):
                saida = executar(estrategia, "--pergunta", "cancelar")
                self.assertIn("qual delas é a sua?", saida)
                self.assertNotIn("mostre na tela ou fale", saida)

    def test_marca_do_canal_sem_servico(self):
        for estrategia in ESTRATEGIAS:
            for canal in ("via WhatsApp da Vivo", "pelo site oficial da Oi", "no app da operadora Claro"):
                with self.subTest(estrategia=estrategia, canal=canal):
                    saida = executar(estrategia, "--pergunta", f"Quero cancelar meu plano {canal}")
                    self.assertIn("qual serviço você quer cancelar?", saida)
                    self.assertNotIn("[v]", saida)
                    self.assertNotIn(TITULOS["DB20"], saida)

    def test_canal_antes_do_servico(self):
        for estrategia in ESTRATEGIAS:
            with self.subTest(estrategia=estrategia):
                saida = executar(estrategia, "--pergunta", "Pelo zap da Vivo quero cancelar minha internet")
                self.assertIn("== " + TITULOS["DB20"], saida)

    def test_academia_por_canal_digital(self):
        for estrategia in ESTRATEGIAS:
            for canal in ("pela internet", "pelo WhatsApp da Vivo", "pelo site da Vivo"):
                with self.subTest(estrategia=estrategia, canal=canal):
                    pergunta = f"Quero cancelar meu plano da academia {canal}"
                    saida = executar(estrategia, entradas=(pergunta, "v", "s", "s", "0"))
                    antes, depois = saida.split("assinou o contrato)?", 1)
                    self.assertNotIn(TITULOS["DB07"], antes)
                    self.assertIn("== " + TITULOS["DB07"], depois)
                    self.assertNotIn(TITULOS["DB20"], saida)
