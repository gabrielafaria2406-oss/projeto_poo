from dominio.tarefa import Tarefa


class TarefaReuniao(Tarefa):
    """Tarefa de reunião (ex.: kickoff com o cliente)."""

    def __init__(self, id_tarefa: int, titulo: str, responsavel: str,
                  local: str, duracao: float, estado: str = "pendente"):

        super().__init__(id_tarefa, titulo, responsavel, estado)

        self._local = local
        self._duracao = duracao

    @property
    def local(self) -> str:
        return self._local

    @property
    def duracao(self) -> float:
        return self._duracao

    def resumo(self) -> str:
        return f"Reunião · {self._local} · {self._duracao}h"

    def tipo(self) -> str:
        return "reuniao"