class Projeto:

    def __init__(self, nome):
        self._nome = nome
        self._tarefas = []

    @property
    def nome(self):
        return self._nome

    @property
    def tarefas(self):
        return list(self._tarefas)

    def adicionar_tarefa(self, tarefa):
        self._tarefas.append(tarefa)

    def remover_tarefa(self, tarefa):

        if tarefa in self._tarefas:
            self._tarefas.remove(tarefa)

    def total_tarefas(self):
        return len(self._tarefas)

    def listar_tarefas(self):
        return list(self._tarefas)

    def __str__(self):
        return f"{self._nome} ({len(self._tarefas)} tarefas)"