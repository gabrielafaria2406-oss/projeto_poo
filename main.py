from repositorio.repositorio_ficheiro import RepositorioFicheiro
from servico.servico_tarefas import ServicoTarefas
from dominio.tarefa_tecnica import TarefaTecnica
from dominio.tarefa_reuniao import TarefaReuniao
from interface.consola import Consola


def criar_servico_com_exemplos() -> ServicoTarefas:
    """Monta o serviço com 2-3 tarefas de exemplo, para a opção 'Listar'
    ter logo algo para mostrar no arranque."""

    repositorio = RepositorioFicheiro("tarefas.csv")
    servico = ServicoTarefas(repositorio)

    servico.adicionar(
        TarefaTecnica(
            servico.proximo_id(),
            "Script de ETL",
            "Ana",
            "Python",
            8
        )
    )
    servico.adicionar(
        TarefaTecnica(
            servico.proximo_id(),
            "Dashboard de KPIs",
            "Bruno",
            "C#",
            12
        )
    )
    servico.adicionar(
        TarefaReuniao(
            servico.proximo_id(),
            "Kickoff Cliente",
            "Carla",
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