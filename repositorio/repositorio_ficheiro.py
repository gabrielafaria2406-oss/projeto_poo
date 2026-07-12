import csv
import os

from dominio.colaborador import Colaborador
from dominio.tarefa import Tarefa
from dominio.tarefa_reuniao import TarefaReuniao
from dominio.tarefa_tecnica import TarefaTecnica
from repositorio.i_repositorio import IRepositorio


SEPARADOR = ";"


class RepositorioFicheiro(IRepositorio):

    def __init__(
        self,
        caminho: str = "tarefas.csv"
    ):
        self._caminho = caminho

    def guardar(
        self,
        tarefas: list[Tarefa]
    ) -> None:

        with open(
            self._caminho,
            "w",
            newline="",
            encoding="utf-8"
        ) as ficheiro:

            escritor = csv.writer(
                ficheiro,
                delimiter=SEPARADOR
            )

            for tarefa in tarefas:
                escritor.writerow(
                    self._para_linha(tarefa)
                )

    def _para_linha(
        self,
        tarefa: Tarefa
    ) -> list:

        dados_base = [
            tarefa.tipo(),
            tarefa.id,
            tarefa.titulo,
            tarefa.responsavel.nome,
            tarefa.responsavel.email,
            tarefa.estado
        ]

        if isinstance(
            tarefa,
            TarefaTecnica
        ):
            return dados_base + [
                tarefa.linguagem,
                tarefa.estimativa_horas
            ]

        if isinstance(
            tarefa,
            TarefaReuniao
        ):
            return dados_base + [
                tarefa.local,
                tarefa.duracao
            ]

        return dados_base

    def carregar(self) -> list[Tarefa]:

        if not os.path.exists(
            self._caminho
        ):
            return []

        tarefas = []

        with open(
            self._caminho,
            "r",
            newline="",
            encoding="utf-8"
        ) as ficheiro:

            leitor = csv.reader(
                ficheiro,
                delimiter=SEPARADOR
            )

            for numero_linha, campos in enumerate(
                leitor,
                start=1
            ):

                try:
                    tarefa = self._criar_tarefa(
                        campos
                    )

                    tarefas.append(tarefa)

                except (
                    ValueError,
                    TypeError,
                    IndexError
                ) as erro:

                    print(
                        f"Linha {numero_linha} "
                        f"ignorada: {erro}"
                    )

        return tarefas

    def _criar_tarefa(
        self,
        campos: list[str]
    ) -> Tarefa:

        if len(campos) < 8:
            raise ValueError(
                "A linha não possui todos os campos."
            )

        tipo = campos[0]
        id_tarefa = int(campos[1])
        titulo = campos[2]

        responsavel = Colaborador(
            campos[3],
            campos[4]
        )

        estado = campos[5]

        if tipo == "tecnica":

            linguagem = campos[6]
            horas = float(campos[7])

            return TarefaTecnica(
                id_tarefa,
                titulo,
                responsavel,
                linguagem,
                horas,
                estado
            )

        if tipo == "reuniao":

            local = campos[6]
            duracao = float(campos[7])

            return TarefaReuniao(
                id_tarefa,
                titulo,
                responsavel,
                local,
                duracao,
                estado
            )

        raise ValueError(
            f"Tipo de tarefa desconhecido: {tipo}"
        )