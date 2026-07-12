import unittest

from dominio.colaborador import Colaborador
from dominio.tarefa_tecnica import TarefaTecnica


class TestTarefa(unittest.TestCase):

    def setUp(self):
        self.colaborador = Colaborador(
            "Ana",
            "ana@email.com"
        )

    def test_criar_tarefa_tecnica(self):
        tarefa = TarefaTecnica(
            1,
            "Script ETL",
            self.colaborador,
            "Python",
            8
        )

        self.assertEqual(tarefa.id, 1)
        self.assertEqual(tarefa.titulo, "Script ETL")
        self.assertIs(
            tarefa.responsavel,
            self.colaborador
        )
        self.assertEqual(
            tarefa.responsavel.nome,
            "Ana"
        )
        self.assertEqual(
            tarefa.responsavel.email,
            "ana@email.com"
        )
        self.assertEqual(
            tarefa.estado,
            "pendente"
        )

    def test_mudar_estado_valido(self):
        tarefa = TarefaTecnica(
            1,
            "Script ETL",
            self.colaborador,
            "Python",
            8
        )

        tarefa.estado = "em curso"

        self.assertEqual(
            tarefa.estado,
            "em curso"
        )

    def test_mudar_estado_invalido(self):
        tarefa = TarefaTecnica(
            1,
            "Script ETL",
            self.colaborador,
            "Python",
            8
        )

        with self.assertRaises(ValueError):
            tarefa.estado = "concluída"

    def test_custo_tarefa_tecnica(self):
        tarefa = TarefaTecnica(
            1,
            "Script ETL",
            self.colaborador,
            "Python",
            8
        )

        self.assertEqual(
            tarefa.custo(),
            200
        )

    def test_responsavel_tem_de_ser_colaborador(self):
        with self.assertRaises(TypeError):
            TarefaTecnica(
                1,
                "Script ETL",
                "Ana",
                "Python",
                8
            )