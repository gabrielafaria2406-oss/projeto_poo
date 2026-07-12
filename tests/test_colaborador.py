import unittest

from dominio.colaborador import Colaborador


class TestColaborador(unittest.TestCase):

    def test_criar_colaborador(self):
        colaborador = Colaborador(
            "Ana Silva",
            "ANA@EMAIL.COM"
        )

        self.assertEqual(
            colaborador.nome,
            "Ana Silva"
        )

        self.assertEqual(
            colaborador.email,
            "ana@email.com"
        )

    def test_nome_obrigatorio(self):
        with self.assertRaises(ValueError):
            Colaborador(
                "",
                "ana@email.com"
            )

    def test_email_invalido(self):
        with self.assertRaises(ValueError):
            Colaborador(
                "Ana Silva",
                "email-invalido"
            )

    def test_representacao_em_texto(self):
        colaborador = Colaborador(
            "Ana Silva",
            "ana@email.com"
        )

        self.assertEqual(
            str(colaborador),
            "Ana Silva <ana@email.com>"
        )