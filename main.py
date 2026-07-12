from dominio.colaborador import Colaborador
from dominio.tarefa_reuniao import TarefaReuniao
from dominio.tarefa_tecnica import TarefaTecnica
from interface.consola import Consola
from repositorio.repositorio_ficheiro import RepositorioFicheiro
from servico.servico_tarefas import ServicoTarefas


def criar_servico_com_exemplos() -> ServicoTarefas:
    """Cria o serviço com algumas tarefas de exemplo."""

    repositorio = RepositorioFicheiro(
        "tarefas.csv"
    )

    servico = ServicoTarefas(
        repositorio
    )

    ana = Colaborador(
        "Ana",
        "ana@email.com"
    )

    bruno = Colaborador(
        "Bruno",
        "bruno@email.com"
    )

    carla = Colaborador(
        "Carla",
        "carla@email.com"
    )

    servico.adicionar(
        TarefaTecnica(
            servico.proximo_id(),
            "Script de ETL",
            ana,
            "Python",
            8
        )
    )

    servico.adicionar(
        TarefaTecnica(
            servico.proximo_id(),
            "Dashboard de KPIs",
            bruno,
            "C#",
            12
        )
    )

    servico.adicionar(
        TarefaReuniao(
            servico.proximo_id(),
            "Kickoff Cliente",
            carla,
            "Sala 3",
            1.5
        )
    )

    return servico


def main() -> None:
    servico = criar_servico_com_exemplos()
    Consola(servico).executar()


if __name__ == "__main__":
    main()