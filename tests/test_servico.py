import unittest

from dominio.colaborador import Colaborador
from dominio.tarefa_reuniao import TarefaReuniao
from dominio.tarefa_tecnica import TarefaTecnica
from servico.servico_tarefas import ServicoTarefas


class RepositorioMemoria:
    """Repositório simples usado apenas nos testes."""

    def __init__(self):
        self._tarefas = []

    def guardar(self, tarefas):
        self._tarefas = list(tarefas)

    def carregar(self):
        return list(self._tarefas)


class TestServicoTarefas(unittest.TestCase):

    def setUp(self):
        repositorio = RepositorioMemoria()
        self.servico = ServicoTarefas(repositorio)

        self.ana = Colaborador(
            "Ana",
            "ana@email.com"
        )

        self.bruno = Colaborador(
            "Bruno",
            "bruno@email.com"
        )

    def test_adicionar_e_listar_tarefa(self):
        tarefa = TarefaTecnica(
            1,
            "Script ETL",
            self.ana,
            "Python",
            8
        )

        self.servico.adicionar(tarefa)

        tarefas = self.servico.listar()

        self.assertEqual(len(tarefas), 1)
        self.assertEqual(
            tarefas[0].titulo,
            "Script ETL"
        )
        self.assertIs(
            tarefas[0].responsavel,
            self.ana
        )

    def test_filtrar_por_estado(self):
        tarefa_pendente = TarefaTecnica(
            1,
            "Script ETL",
            self.ana,
            "Python",
            8
        )

        tarefa_em_curso = TarefaReuniao(
            2,
            "Reunião com cliente",
            self.bruno,
            "Sala 3",
            1.5
        )

        tarefa_em_curso.estado = "em curso"

        self.servico.adicionar(tarefa_pendente)
        self.servico.adicionar(tarefa_em_curso)

        resultado = self.servico.filtrar_por_estado(
            "em curso"
        )

        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0].id, 2)

    def test_estatisticas(self):
        tarefa_tecnica = TarefaTecnica(
            1,
            "Script ETL",
            self.ana,
            "Python",
            8
        )

        tarefa_reuniao = TarefaReuniao(
            2,
            "Reunião com cliente",
            self.bruno,
            "Sala 3",
            1.5
        )

        tarefa_tecnica.estado = "em curso"
        tarefa_tecnica.estado = "concluída"

        self.servico.adicionar(tarefa_tecnica)
        self.servico.adicionar(tarefa_reuniao)

        estatisticas = self.servico.estatisticas()

        self.assertEqual(
            estatisticas["total"],
            2
        )
        self.assertEqual(
            estatisticas["horas_estimadas"],
            8
        )
        self.assertEqual(
            estatisticas["percentagem_concluidas"],
            50
        )

    def test_relatorio_custos(self):
        tarefa_tecnica = TarefaTecnica(
            1,
            "Script ETL",
            self.ana,
            "Python",
            8
        )

        tarefa_reuniao = TarefaReuniao(
            2,
            "Reunião com cliente",
            self.bruno,
            "Sala 3",
            2
        )

        self.servico.adicionar(tarefa_tecnica)
        self.servico.adicionar(tarefa_reuniao)

        relatorio = self.servico.relatorio_custos()

        self.assertEqual(
            len(relatorio["tarefas"]),
            2
        )
        self.assertEqual(
            relatorio["total"],
            230
        )