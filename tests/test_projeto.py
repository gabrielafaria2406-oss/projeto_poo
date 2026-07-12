import unittest

from dominio.colaborador import Colaborador
from dominio.projeto import Projeto
from dominio.tarefa_tecnica import TarefaTecnica


class TestProjeto(unittest.TestCase):

    def setUp(self):
        self.ana = Colaborador(
            "Ana",
            "ana@email.com"
        )

        self.bruno = Colaborador(
            "Bruno",
            "bruno@email.com"
        )

    def test_adicionar_e_procurar_tarefa(self):
        projeto = Projeto("Projeto POO")

        tarefa = TarefaTecnica(
            1,
            "Script ETL",
            self.ana,
            "Python",
            8
        )

        projeto.adicionar_tarefa(tarefa)

        encontrada = projeto.procurar_tarefa(1)

        self.assertEqual(
            projeto.total_tarefas(),
            1
        )

        self.assertIs(
            encontrada,
            tarefa
        )

        self.assertIs(
            encontrada.responsavel,
            self.ana
        )

    def test_nao_permite_ids_repetidos(self):
        projeto = Projeto("Projeto POO")

        primeira = TarefaTecnica(
            1,
            "Script ETL",
            self.ana,
            "Python",
            8
        )

        segunda = TarefaTecnica(
            1,
            "Dashboard",
            self.bruno,
            "C#",
            12
        )

        projeto.adicionar_tarefa(primeira)

        with self.assertRaises(ValueError):
            projeto.adicionar_tarefa(segunda)