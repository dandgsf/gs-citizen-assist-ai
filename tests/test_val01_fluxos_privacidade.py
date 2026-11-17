# VAL-01 - Fluxos, condições e privacidade do Citizen Assist AI

# Uso a partir da raiz do repo:
# python -m unittest discover -s tests -p 'test_val01_*.py' -v

from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
import subprocess
import sys
import unittest

RAIZ = Path(__file__).resolve().parents[1]
SRC = RAIZ / "src"
sys.path.insert(0, str(SRC))

from base_conhecimento import Base # noqa: E402
from busca import Buscador # noqa: E402
from condicoes import avaliar, interpretar_resposta # noqa: E402
from privacidade import mascarar # noqa: E402
from sistema import Tela, responder, verificar_condicoes # noqa: E402

# Preparando a base de conhecimento e buscador, compartilhando-os entre
# os testes da classe
class BaseDeTeste(unittest.TestCase): #unittest para criar tests automatizados
    @classmethod # define o método que trabalha com a prórpia classe (cls)
    def setUpClass(cls): # é executado uma única vez antes dos testes de classe
        cls.base = Base(str(RAIZ / "data" / "base.json"), str(RAIZ/ "data" / "sinonimos.json")) # carrega os arquivos JSON da base de conhecimento e dos sinônimos
        cls.buscador = Buscador(cls.base) # Cria uma instância de "Buscador", utilizando a base carregada

    # Devolve a saída textual da consulta e os atalhos disponíveis
    def consulta(self, pergunta):
        saida = StringIO()
        with redirect_stdout(saida):
            atalhos = responder(Tela(simples=True), 
                                self.base, 
                                self.buscador, 
                                pergunta,
                                "hibrida", 
                                explicar=False)
        return saida.getvalue(), atalhos
    
    # Roda a interface real sem usar rede ou coletar dados pessoais
    def sessao(self, entradas):
        return subprocess.run(
            [sys.executable, str(SRC / "sistema.py"), "--simples"],
            input="\n".join(entradas) + "\n",
            capture_output=True, text=True, cwd=str(RAIZ), timeout=10,
        )
    
# Valida a inicialização, o aviso não oficial e o encerramento
# correto do sistema
class TesteFluxosVAL01A(BaseDeTeste): # cria uma classe de test que herda os recursos de BaseDeTeste
    def test_01_menu_inicial_e_aviso_nao_oficial(self): # define um test que o unittest reconhece de forma automatica
        r = self.sessao(["0"]) # executa uma sessão simulada que envia a opção 0 do sistema
        self.assertEqual(r.returncode, 0, r.stderr) # verifica o codigo de encerramento
        self.assertIn("CITIZEN ASSIST AI", r.stdout)
        self.assertIn("Não sou canal oficial", r.stdout)
        self.assertIn("Até logo", r.stdout)

    def test_02_menu_temas(self):
        r = self.sessao(["1", "0"])
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("[t1]", r.stdout)
        self.assertIn("Mercado e lojas", r.stdout)

    def test_03_navegacao_tema_situacao_fonte(self):
        r = self.sessao(["1", "t1", "s1", "0"])
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("[s1]", r.stdout)
        self.assertIn("FONTE:", r.stdout)
        self.assertIn("ASSUNTOS RELACIONADOS", r.stdout)

    def test_04_navegacao_relacioados(self):
        r = self.sessao(["1", "t1", "s1", "r1", "r2", "0"])
        self.assertEqual(r.returncode, 0, r.stderr)
        # DB01 -> DB02 -> DB05: três orientações distintas por assuntos relacionados
        self.assertGreaterEqual(r.stdout.count("FONTE:"), 3)

    def test_05_opcao_inexistente(self):
        r = self.sessao(["99", "t99", "s99", "r99", "v99", "0"])
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertGreaterEqual(r.stdout.count("não existe aqui"), 5)

    def test_06_entrada_vazia(self):
        saida, atalhos = self.consulta("")
        self.assertIn("Você não escreveu nada", saida)
        self.assertEqual(atalhos, {})

    def test_07_entrada_apenas_simbolos(self):
        saida, atalhos = self.consulta("!!!")
        self.assertIn("Não consegui entender", saida)
        self.assertEqual(atalhos, {})

    def test_08_pergunta_ambigua(self):
        saida, atalhos = self.consulta("cancelar")
        self.assertIn("mais de uma situação", saida)
        self.assertIn("a", atalhos)
        self.assertIn("n", atalhos)

    def test_09_usuario_recusa_opcoes_ambiguas(self):
        r = self.sessao(["cancelar", "n", "0"])
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("Tente descrever de outro jeito", r.stdout)

    def test_10_pergunta_fora_do_tema(self):
        saida, atalhos = self.consulta("astronautas em plutão")
        self.assertNotIn("FONTE:", saida)
        self.assertEqual(atalhos, {})

    def test_11_sem_resposta_confiavel(self):
        saida, atalhos = self.consulta("sem dados não tem consulta")
        self.assertIn("Não encontrei uma informação confiável", saida)
        self.assertIn("ver as situações", saida)
        self.assertEqual(atalhos, {})

    def test_12_menu_explicacao_e_aviso(self):
        r = self.sessao(["2", "3", "0"])
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("COMO FUNCIONA", r.stdout)
        self.assertIn("Modo explicação LIGADO", r.stdout)

# Valida a interpretação de respostas afirmativas, negativas, indefinida e invalida
class TesteCondicoesVAL01B(BaseDeTeste):
    def test_13_interpretar_sim_nao_nao_sei_e_invalida(self):
        exemplos = {
            "s": True,
            "sim": True,
            "n": False,
            "não": False,
            "?" : None,
            "nao sei": None,
            "talvez": None,
            "qualquer": "invalida"
        }

        for texto, esperado in exemplos.items():
            with self.subTest(texto=texto):
                self.assertEqual(interpretar_resposta(texto), esperado)

    def test_14_regra_todas_tres_estados(self):
        cenarios = [
            ({
                "a": True,
                "b": True
            },
            True),
            ({
                "a": False,
                "b": None
            },
            False),
            ({
                "a": True,
                "b": None
            },
            None)
        ]

        for respostas, esperado in cenarios:
            with self.subTest(respostas=respostas):
                resultado, _ = avaliar("todas", respostas)
                self.assertIs(resultado, esperado)

    def test_15_regra_alguma_tres_estados(self):
        cenarios = [
            ({
                "a": False,
                "b": True
            },
            True),
            ({
                "a": False,
                "b": False
            },
            False),
            ({
                "a": False,
                "b": None
            },
            None)
        ]

        for respostas, esperado in cenarios:
            with self.subTest(respostas=respostas):
                resultado, _ = avaliar("alguma", respostas)
                self.assertIs(resultado, esperado)

    def _executar_verificacao(self, rid, respostas):
        saida = StringIO()
        respostas = iter(respostas)
        with redirect_stdout(saida):
            verificar_condicoes(
                Tela(simples=True),
                self.base,
                rid,
                lambda _: next(respostas)
            )
        return saida.getvalue()
    
    def test_16_condicoes_db07_sim_nao_nao_sei(self):
        sim = self._executar_verificacao("DB07", ["s", "s"])
        nao = self._executar_verificacao("DB07", ["n", "s"])
        duvida = self._executar_verificacao("DB07", ["?", "s"])
        self.assertIn("direito de arrependimento se aplica", sim)
        self.assertRegex(nao, r"NÃO\s+se\s+aplica")
        self.assertIn("Não dá para afirmar", duvida)

    def test_17_condicoes_db14_sim_nao_nao_sei(self):
        sim = self._executar_verificacao("DB14", ["n", "s", "n", "n"])
        nao = self._executar_verificacao("DB14", ["n", "n", "n", "n"])
        duvida = self._executar_verificacao("DB14", ["?", "n", "n", "n"])
        self.assertIn("se enquadra em pelo menos um grupo", sim)
        self.assertIn("não se enquadra nos grupos", nao)
        self.assertIn("Não dá para afirmar", duvida)

    def test_18_condicoes_db23_sim_nao_nao_sei(self):
        sim = self._executar_verificacao("DB23", ["s", "s", "s"])
        nao = self._executar_verificacao("DB23", ["s", "n", "s"])
        duvida = self._executar_verificacao("DB23", ["s", "?", "s"])
        self.assertIn("direito à vaga gratuita", sim)
        self.assertRegex(nao, r"NÃO\s+se\s+aplica")
        self.assertIn("Não dá para afirmar", duvida)

    def test_19_respostas_invalida_pergunta_novamente(self):
        saida = self._executar_verificacao("DB07", ["qualquer", "s", "s"])
        self.assertIn("Resposta não reconhecida", saida)
        self.assertIn("direito de arrependimento se aplica", saida)

class TestePrivacidadeVAL01C(BaseDeTeste):
    EXEMPLOS_FICTICIOS = {
        "CPF": "123.456.789-00",
        "telefone": "(11) 91234-5678",
        "e-mail": "pessoa.teste@exemplo.invalid",
        "cartão": "4111 1111 1111 1111",
    }

    def test_20_mascarar_cpf_ficticio(self):
        texto, tipos = mascarar("cpf " + self.EXEMPLOS_FICTICIOS["CPF"])
        self.assertIn("CPF", tipos)
        self.assertNotIn(self.EXEMPLOS_FICTICIOS["CPF"], texto)

    def test_21_mascarar_telefone_ficticio(self):
        texto, tipos = mascarar("telefone " + self.EXEMPLOS_FICTICIOS["telefone"])
        self.assertIn("telefone", tipos)
        self.assertNotIn(self.EXEMPLOS_FICTICIOS["telefone"], texto)

    def test_22_mascarar_email_ficticio(self):
        texto, tipos = mascarar("email " + self.EXEMPLOS_FICTICIOS["e-mail"])
        self.assertIn("e-mail", tipos)
        self.assertNotIn(self.EXEMPLOS_FICTICIOS["e-mail"], texto)

    def test_23_mascarar_cartao_ficticio(self):
        texto, tipos = mascarar("cartão " + self.EXEMPLOS_FICTICIOS["cartão"])
        self.assertIn("cartão", tipos)
        self.assertNotIn(self.EXEMPLOS_FICTICIOS["cartão"], texto)

    def test_24_mascarar_multiplos_dados(self):
        dados = " ".join(self.EXEMPLOS_FICTICIOS.values())
        texto, tipos = mascarar(dados)
        self.assertEqual(set(tipos), set(self.EXEMPLOS_FICTICIOS))
        
        for valor in self.EXEMPLOS_FICTICIOS.values():
            self.assertNotIn(valor, texto)

    def test_25_interface_nao_reexibe_email(self):
        email = self.EXEMPLOS_FICTICIOS["e-mail"]
        r = subprocess.run(
            [
                sys.executable,
                str(SRC / "sistema.py"),
                "--simples",
                "--pergunta",
                "quero reclamar " + email
            ],
            capture_output=True,
            text=True,
            cwd=str(RAIZ),
            timeout=10
        )

        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertNotIn(email, r.stdout)
        self.assertIn("Você digitou", r.stdout)

if __name__ == "__main__":
    unittest.main()