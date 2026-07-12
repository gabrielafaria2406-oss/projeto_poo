from dominio.tarefa import Tarefa
from dominio.faturavel import Faturavel


class TarefaTecnica(Tarefa, Faturavel):
    """Tarefa de execução técnica (ex.: desenvolver um script Python)."""

    def __init__(self, id_tarefa: int, titulo: str, responsavel: str,
                 linguagem: str, estimativa_horas: float,
                 estado: str = "pendente"):
        # A mãe constrói a parte comum (id, título, responsável, estado).
        super().__init__(id_tarefa, titulo, responsavel, estado)
        # A filha acrescenta o que é só seu.
        self._linguagem = linguagem
        self._estimativa_horas = estimativa_horas

    @property
    def linguagem(self) -> str:
        return self._linguagem

    @property
    def estimativa_horas(self) -> float:
        return self._estimativa_horas

    # Override dos métodos abstratos da mãe.
    def resumo(self) -> str:
        return (f"Técnica · {self._linguagem} · "
                f"{self._estimativa_horas}h estimadas")

    def tipo(self) -> str:
        return "tecnica"


    def custo(self) -> float:
        return self._estimativa_horas * 25