import unittest

from dominio.tarefa_tecnica import TarefaTecnica


class TestTarefa(unittest.TestCase):

    def test_criar_tarefa_tecnica(self):

        tarefa = TarefaTecnica(
            1,
            "Script ETL",
            "Ana",
            "Python",
            8
        )

        self.assertEqual(tarefa.id, 1)
        self.assertEqual(tarefa.titulo, "Script ETL")
        self.assertEqual(tarefa.responsavel, "Ana")
        self.assertEqual(tarefa.estado, "pendente")
        
    def test_mudar_estado_valido(self):

        tarefa = TarefaTecnica(
            1,
            "Script ETL",
            "Ana",
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
            "Ana",
            "Python",
            8
        )

        with self.assertRaises(ValueError):
            tarefa.estado = "concluída"
            
    def test_custo_tarefa_tecnica(self):

        tarefa = TarefaTecnica(
            1,
            "Script ETL",
            "Ana",
            "Python",
            8
        )

        self.assertEqual(
            tarefa.custo(),
            200
        )