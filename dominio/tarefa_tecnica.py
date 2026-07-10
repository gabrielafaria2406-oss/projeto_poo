"""
Camada de DOMÍNIO — subclasse COMPLETA, o teu exemplo trabalhado.

Quando fores fazer a TarefaReuniao (que está em TODO), copia o padrão
desta classe. Repara em três coisas:
  1. class TarefaTecnica(Tarefa)  -> HERANÇA
  2. super().__init__(...)         -> deixa a mãe tratar do que é dela
  3. def resumo(self)             -> OVERRIDE: a versão própria do método
"""

from dominio.tarefa import Tarefa


class TarefaTecnica(Tarefa):
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
