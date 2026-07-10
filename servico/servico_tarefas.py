from dominio.tarefa import Tarefa
from dominio.tarefa_tecnica import TarefaTecnica
from repositorio.i_repositorio import IRepositorio


class ServicoTarefas:

    def __init__(self, repositorio: IRepositorio):
        self._repositorio = repositorio
        self._tarefas = []
        self._proximo_id = 1

    def proximo_id(self):
        return self._proximo_id

    def adicionar(self, tarefa):
        self._tarefas.append(tarefa)
        self._proximo_id = max(self._proximo_id, tarefa.id) + 1
        return tarefa

    def listar(self):
        return list(self._tarefas)

    def mudar_estado(self, id_tarefa, novo_estado):

        for tarefa in self._tarefas:

            if tarefa.id == id_tarefa:
                tarefa.estado = novo_estado
                return

        raise ValueError("Tarefa não encontrada.")

    def filtrar_por_estado(self, estado):

        return [
            tarefa
            for tarefa in self._tarefas
            if tarefa.estado == estado
        ]

    def estatisticas(self):

        total = len(self._tarefas)

        horas_estimadas = sum(
            tarefa.estimativa_horas
            for tarefa in self._tarefas
            if isinstance(tarefa, TarefaTecnica)
        )

        concluidas = sum(
            1
            for tarefa in self._tarefas
            if tarefa.estado == "concluída"
        )

        percentagem = 0

        if total > 0:
            percentagem = (concluidas / total) * 100

        return {
            "total": total,
            "horas_estimadas": horas_estimadas,
            "percentagem_concluidas": percentagem
        }

    def guardar(self):

        self._repositorio.guardar(
            self._tarefas
        )

    def carregar(self):

        self._tarefas = (
            self._repositorio.carregar()
        )

        if self._tarefas:

            self._proximo_id = (
                max(
                    tarefa.id
                    for tarefa in self._tarefas
                ) + 1
            )