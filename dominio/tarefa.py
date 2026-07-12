from abc import ABC, abstractmethod

from dominio.colaborador import Colaborador
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
            raise ValueError(
                f"Estado inválido. Usa um de {ESTADOS_VALIDOS}"
            )

        if hasattr(self, "_estado"):

            estado_atual = self._estado

            if novo_estado != estado_atual:

                if novo_estado not in TRANSICOES_VALIDAS[estado_atual]:
                    raise ValueError(
                        f"Transição inválida: "
                        f"{estado_atual} -> {novo_estado}"
                    )

        self._estado = novo_estado

    @abstractmethod
    def resumo(self) -> str:
        pass

    @abstractmethod
    def tipo(self) -> str:
        pass

    def detalhe(self) -> str:
        return (
            f"[{self._id}] {self._titulo}\n"
            f"    Responsável: {self._responsavel.nome}\n"
            f"    Email: {self._responsavel.email}\n"
            f"    Estado: {self._estado}\n"
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