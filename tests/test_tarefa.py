import unittest

from dominio.colaborador import Colaborador
from dominio.excecoes import (
    DependenciaInvalida,
    DependenciasPendentes,
    TransicaoEstadoInvalida
)
from dominio.tarefa_tecnica import TarefaTecnica


class TestTarefa(unittest.TestCase):

    def setUp(self):
        self.colaborador = Colaborador(
            "Ana",
            "ana@email.com"
        )

    def criar_tarefa(
        self,
        id_tarefa: int = 1,
        titulo: str = "Script ETL"
    ) -> TarefaTecnica:

        return TarefaTecnica(
            id_tarefa,
            titulo,
            self.colaborador,
            "Python",
            8
        )

    def test_criar_tarefa_tecnica(self):
        tarefa = self.criar_tarefa()

        self.assertEqual(tarefa.id, 1)
        self.assertEqual(
            tarefa.titulo,
            "Script ETL"
        )
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
        tarefa = self.criar_tarefa()

        tarefa.estado = "em curso"

        self.assertEqual(
            tarefa.estado,
            "em curso"
        )

    def test_mudar_estado_invalido(self):
        tarefa = self.criar_tarefa()

        with self.assertRaises(
            TransicaoEstadoInvalida
        ):
            tarefa.estado = "concluída"

    def test_estado_desconhecido(self):
        tarefa = self.criar_tarefa()

        with self.assertRaises(
            TransicaoEstadoInvalida
        ):
            tarefa.estado = "cancelada"

    def test_custo_tarefa_tecnica(self):
        tarefa = self.criar_tarefa()

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

    def test_adicionar_dependencia(self):
        dependencia = self.criar_tarefa(
            1,
            "Script ETL"
        )

        tarefa = self.criar_tarefa(
            2,
            "Dashboard"
        )

        tarefa.adicionar_dependencia(
            dependencia
        )

        self.assertEqual(
            len(tarefa.dependencias),
            1
        )

        self.assertIs(
            tarefa.dependencias[0],
            dependencia
        )

    def test_dependencias_concluidas(self):
        dependencia = self.criar_tarefa(
            1,
            "Script ETL"
        )

        tarefa = self.criar_tarefa(
            2,
            "Dashboard"
        )

        tarefa.adicionar_dependencia(
            dependencia
        )

        self.assertFalse(
            tarefa.dependencias_concluidas()
        )

        dependencia.estado = "em curso"
        dependencia.estado = "concluída"

        self.assertTrue(
            tarefa.dependencias_concluidas()
        )

    def test_nao_inicia_com_dependencia_pendente(self):
        dependencia = self.criar_tarefa(
            1,
            "Preparar dados"
        )

        tarefa = self.criar_tarefa(
            2,
            "Criar dashboard"
        )

        tarefa.adicionar_dependencia(
            dependencia
        )

        with self.assertRaises(
            DependenciasPendentes
        ):
            tarefa.estado = "em curso"

    def test_inicia_com_dependencia_concluida(self):
        dependencia = self.criar_tarefa(
            1,
            "Preparar dados"
        )

        tarefa = self.criar_tarefa(
            2,
            "Criar dashboard"
        )

        tarefa.adicionar_dependencia(
            dependencia
        )

        dependencia.estado = "em curso"
        dependencia.estado = "concluída"

        tarefa.estado = "em curso"

        self.assertEqual(
            tarefa.estado,
            "em curso"
        )

    def test_nao_permite_dependencia_em_si_propria(self):
        tarefa = self.criar_tarefa()

        with self.assertRaises(
            DependenciaInvalida
        ):
            tarefa.adicionar_dependencia(
                tarefa
            )

    def test_nao_permite_dependencia_repetida(self):
        dependencia = self.criar_tarefa(
            1,
            "Preparar dados"
        )

        tarefa = self.criar_tarefa(
            2,
            "Criar dashboard"
        )

        tarefa.adicionar_dependencia(
            dependencia
        )

        with self.assertRaises(
            DependenciaInvalida
        ):
            tarefa.adicionar_dependencia(
                dependencia
            )