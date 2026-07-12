from abc import ABC, abstractmethod

from dominio.colaborador import Colaborador
from dominio.excecoes import (
    DependenciaInvalida,
    DependenciasPendentes,
    TransicaoEstadoInvalida
)
from dominio.exportavel import Exportavel


ESTADOS_VALIDOS = (
    "pendente",
    "em curso",
    "concluída"
)

TRANSICOES_VALIDAS = {
    "pendente": ["em curso"],
    "em curso": ["concluída"],
    "concluída": []
}


class Tarefa(Exportavel, ABC):

    def __init__(
        self,
        id_tarefa: int,
        titulo: str,
        responsavel: Colaborador,
        estado: str = "pendente"
    ):

        if not isinstance(responsavel, Colaborador):
            raise TypeError(
                "O responsável deve ser um objeto Colaborador."
            )

        self._id = id_tarefa
        self._titulo = titulo
        self._responsavel = responsavel
        self._estado = estado
        self._dependencias: list["Tarefa"] = []

    @property
    def id(self) -> int:
        return self._id

    @property
    def titulo(self) -> str:
        return self._titulo

    @property
    def responsavel(self) -> Colaborador:
        return self._responsavel

    @property
    def estado(self) -> str:
        return self._estado

    @estado.setter
    def estado(self, novo_estado: str) -> None:

        if novo_estado not in ESTADOS_VALIDOS:
            raise TransicaoEstadoInvalida(
                f"Estado inválido. Usa um de {ESTADOS_VALIDOS}"
            )

        estado_atual = self._estado

        if novo_estado == estado_atual:
            return

        if novo_estado not in TRANSICOES_VALIDAS[estado_atual]:
            raise TransicaoEstadoInvalida(
                f"Transição inválida: "
                f"{estado_atual} -> {novo_estado}"
            )

        if (
            novo_estado == "em curso"
            and not self.dependencias_concluidas()
        ):
            raise DependenciasPendentes(
                "A tarefa não pode iniciar enquanto "
                "existirem dependências pendentes."
            )

        self._estado = novo_estado

    @property
    def dependencias(self) -> list["Tarefa"]:
        return list(self._dependencias)

    def adicionar_dependencia(
        self,
        tarefa: "Tarefa"
    ) -> None:

        if not isinstance(tarefa, Tarefa):
            raise TypeError(
                "A dependência deve ser uma Tarefa."
            )

        if tarefa is self:
            raise DependenciaInvalida(
                "Uma tarefa não pode depender de si própria."
            )

        if tarefa in self._dependencias:
            raise DependenciaInvalida(
                "Essa dependência já foi adicionada."
            )

        self._dependencias.append(tarefa)

    def dependencias_concluidas(self) -> bool:
        return all(
            tarefa.estado == "concluída"
            for tarefa in self._dependencias
        )

    @abstractmethod
    def resumo(self) -> str:
        pass

    @abstractmethod
    def tipo(self) -> str:
        pass

    def detalhe(self) -> str:

        quantidade_dependencias = len(
            self._dependencias
        )

        return (
            f"[{self._id}] {self._titulo}\n"
            f"    Responsável: {self._responsavel.nome}\n"
            f"    Email: {self._responsavel.email}\n"
            f"    Estado: {self._estado}\n"
            f"    Dependências: {quantidade_dependencias}\n"
            f"    {self.resumo()}"
        )

    def exportar(self) -> str:
        return (
            f"{self.tipo()};"
            f"{self.id};"
            f"{self.titulo};"
            f"{self.responsavel.nome};"
            f"{self.responsavel.email};"
            f"{self.estado}"
        )