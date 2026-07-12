from dominio.faturavel import Faturavel
from dominio.projeto import Projeto
from dominio.tarefa_tecnica import TarefaTecnica
from repositorio.i_repositorio import IRepositorio


class ServicoTarefas:

    def __init__(self, repositorio: IRepositorio):
        self._repositorio = repositorio
        self._projeto = Projeto("Projeto POO")
        self._proximo_id = 1

    def proximo_id(self) -> int:
        return self._proximo_id

    def adicionar(self, tarefa):
        self._projeto.adicionar_tarefa(tarefa)

        self._proximo_id = max(
            self._proximo_id,
            tarefa.id + 1
        )

        return tarefa

    def listar(self):
        return self._projeto.tarefas

    def mudar_estado(
        self,
        id_tarefa: int,
        novo_estado: str
    ) -> None:

        tarefa = self._projeto.procurar_tarefa(
            id_tarefa
        )

        tarefa.estado = novo_estado

    def filtrar_por_estado(self, estado: str):

        return [
            tarefa
            for tarefa in self._projeto.tarefas
            if tarefa.estado == estado
        ]

    def estatisticas(self):

        tarefas = self._projeto.tarefas
        total = len(tarefas)

        horas_estimadas = sum(
            tarefa.estimativa_horas
            for tarefa in tarefas
            if isinstance(tarefa, TarefaTecnica)
        )

        concluidas = sum(
            1
            for tarefa in tarefas
            if tarefa.estado == "concluída"
        )

        percentagem = 0

        if total > 0:
            percentagem = (
                concluidas / total
            ) * 100

        return {
            "total": total,
            "horas_estimadas": horas_estimadas,
            "percentagem_concluidas": percentagem
        }

    def guardar(self) -> None:

        self._repositorio.guardar(
            self._projeto.tarefas
        )

    def carregar(self) -> None:

        tarefas = self._repositorio.carregar()

        self._projeto.substituir_tarefas(
            tarefas
        )

        self._proximo_id = (
            max(
                (
                    tarefa.id
                    for tarefa in tarefas
                ),
                default=0
            ) + 1
        )

    def relatorio_custos(self):

        total = 0
        relatorio = []

        for tarefa in self._projeto.tarefas:

            if isinstance(tarefa, Faturavel):

                custo = tarefa.custo()

                relatorio.append({
                    "id": tarefa.id,
                    "titulo": tarefa.titulo,
                    "tipo": tarefa.tipo(),
                    "custo": custo
                })

                total += custo

        return {
            "tarefas": relatorio,
            "total": total
        }