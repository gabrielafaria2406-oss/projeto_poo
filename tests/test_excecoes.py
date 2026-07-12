import unittest

from dominio.excecoes import (
    DependenciaInvalida,
    DependenciasPendentes,
    ErroDominio,
    TarefaNaoEncontrada,
    TransicaoEstadoInvalida
)


class TestExcecoes(unittest.TestCase):

    def test_excecoes_sao_erros_de_dominio(self):

        excecoes = [
            TransicaoEstadoInvalida,
            DependenciasPendentes,
            DependenciaInvalida,
            TarefaNaoEncontrada
        ]

        for excecao in excecoes:
            self.assertTrue(
                issubclass(excecao, ErroDominio)
            )