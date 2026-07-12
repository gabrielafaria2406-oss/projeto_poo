import os
import tempfile
import unittest

from dominio.colaborador import Colaborador
from dominio.tarefa_reuniao import TarefaReuniao
from dominio.tarefa_tecnica import TarefaTecnica
from repositorio.repositorio_ficheiro import RepositorioFicheiro


class TestRepositorioFicheiro(unittest.TestCase):

    def setUp(self):
        ficheiro_temporario = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".csv"
        )

        ficheiro_temporario.close()

        self.caminho = ficheiro_temporario.name
        self.repositorio = RepositorioFicheiro(
            self.caminho
        )

        self.ana = Colaborador(
            "Ana",
            "ana@email.com"
        )

        self.bruno = Colaborador(
            "Bruno",
            "bruno@email.com"
        )

    def tearDown(self):
        if os.path.exists(self.caminho):
            os.remove(self.caminho)

    def test_guardar_e_carregar_tarefas(self):
        tarefas = [
            TarefaTecnica(
                1,
                "Script ETL",
                self.ana,
                "Python",
                8
            ),
            TarefaReuniao(
                2,
                "Reunião",
                self.bruno,
                "Sala 3",
                1.5
            )
        ]

        self.repositorio.guardar(tarefas)

        carregadas = self.repositorio.carregar()

        self.assertEqual(len(carregadas), 2)
        self.assertEqual(
            carregadas[0].responsavel.nome,
            "Ana"
        )
        self.assertEqual(
            carregadas[0].responsavel.email,
            "ana@email.com"
        )
        self.assertEqual(
            carregadas[1].responsavel.nome,
            "Bruno"
        )

    def test_ficheiro_corrompido_nao_interrompe(self):
        with open(
            self.caminho,
            "w",
            encoding="utf-8"
        ) as ficheiro:
            ficheiro.write(
                "tecnica;abc;dados-invalidos\n"
            )

        tarefas = self.repositorio.carregar()

        self.assertEqual(tarefas, [])