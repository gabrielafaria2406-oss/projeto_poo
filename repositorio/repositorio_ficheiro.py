import csv
import os

from dominio.tarefa import Tarefa
from dominio.tarefa_tecnica import TarefaTecnica
from dominio.tarefa_reuniao import TarefaReuniao
from repositorio.i_repositorio import IRepositorio

SEPARADOR = ";"


class RepositorioFicheiro(IRepositorio):

    def __init__(self, caminho: str = "tarefas.csv"):
        self._caminho = caminho

    def guardar(self, tarefas: list[Tarefa]) -> None:
        with open(self._caminho, "w", newline="", encoding="utf-8") as f:
            escritor = csv.writer(f, delimiter=SEPARADOR)

            for t in tarefas:
                escritor.writerow(self._para_linha(t))

    def _para_linha(self, t: Tarefa) -> list:

        base = [
            t.tipo(),
            t.id,
            t.titulo,
            t.responsavel,
            t.estado
        ]

        if isinstance(t, TarefaTecnica):
            return base + [t.linguagem, t.estimativa_horas]

        if isinstance(t, TarefaReuniao):
            return base + [t.local, t.duracao]

        return base

    def carregar(self) -> list:

        if not os.path.exists(self._caminho):
            return []

        tarefas = []

        with open(
            self._caminho,
            "r",
            newline="",
            encoding="utf-8"
        ) as f:

            leitor = csv.reader(
                f,
                delimiter=SEPARADOR
            )

            for campos in leitor:

                try:
                    if len(campos) < 7:
                        print(f"Linha ignorada (inválida): {campos}")
                        continue

                    tipo = campos[0]

                    id_tarefa = int(campos[1])
                    titulo = campos[2]
                    responsavel = campos[3]
                    estado = campos[4]

                    if tipo == "tecnica":

                        linguagem = campos[5]
                        horas = float(campos[6])

                        tarefas.append(
                            TarefaTecnica(
                                id_tarefa,
                                titulo,
                                responsavel,
                                linguagem,
                                horas,
                                estado
                            )
                        )
                    
            

                    elif tipo == "reuniao":

                        local = campos[5]
                        duracao = float(campos[6])

                        tarefas.append(
                            TarefaReuniao(
                                id_tarefa,
                                titulo,
                                responsavel,
                                local,
                                duracao,
                                estado
                            )
                        )
                
            

                    else:
                        print(f"Tipo desconhecido: {tipo}")

                except (ValueError, IndexError) as e:
                    print(f"Erro ao carregar linha {campos}: {e}")

        return tarefas