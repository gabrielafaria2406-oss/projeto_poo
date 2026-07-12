from dominio.colaborador import Colaborador
from dominio.tarefa_reuniao import TarefaReuniao
from dominio.tarefa_tecnica import TarefaTecnica
from servico.servico_tarefas import ServicoTarefas


class Consola:

    def __init__(self, servico: ServicoTarefas):
        self._servico = servico

    def executar(self) -> None:

        opcoes = {
            "1": ("Listar tarefas", self._listar),
            "2": ("Adicionar tarefa", self._adicionar),
            "3": (
                "Mudar estado de uma tarefa",
                self._mudar_estado
            ),
            "4": ("Filtrar por estado", self._filtrar),
            "5": ("Ver estatísticas", self._estatisticas),
            "6": ("Guardar em ficheiro", self._guardar),
            "7": ("Carregar de ficheiro", self._carregar),
            "8": ("Exportar", self._exportar),
            "9": (
                "Relatório de custos",
                self._relatorio_custos
            )
        }

        while True:

            print("\n=== Gestão de Tarefas ===")

            for tecla, (rotulo, _) in opcoes.items():
                print(f"  {tecla}. {rotulo}")

            print("  0. Sair")

            escolha = input(
                "Escolhe uma opção: "
            ).strip()

            if escolha == "0":
                print("Até à próxima!")
                break

            opcao = opcoes.get(escolha)

            if opcao is None:
                print("Opção inválida.")
                continue

            try:
                opcao[1]()

            except (ValueError, TypeError) as erro:
                print(f"Erro: {erro}")

    def _listar(self) -> None:

        tarefas = self._servico.listar()

        if not tarefas:
            print("(sem tarefas)")
            return

        for tarefa in tarefas:
            print()
            print(tarefa.detalhe())

    def _adicionar(self) -> None:

        tipo = input(
            "Tipo (tecnica/reuniao): "
        ).strip().lower()

        titulo = input(
            "Título: "
        ).strip()

        nome_responsavel = input(
            "Nome do responsável: "
        ).strip()

        email_responsavel = input(
            "Email do responsável: "
        ).strip()

        responsavel = Colaborador(
            nome_responsavel,
            email_responsavel
        )

        if tipo == "tecnica":

            linguagem = input(
                "Linguagem: "
            ).strip()

            horas = self._ler_float_positivo(
                "Horas estimadas: "
            )

            tarefa = TarefaTecnica(
                self._servico.proximo_id(),
                titulo,
                responsavel,
                linguagem,
                horas
            )

        elif tipo == "reuniao":

            local = input(
                "Local: "
            ).strip()

            duracao = self._ler_float_positivo(
                "Duração: "
            )

            tarefa = TarefaReuniao(
                self._servico.proximo_id(),
                titulo,
                responsavel,
                local,
                duracao
            )

        else:
            print("Tipo inválido.")
            return

        self._servico.adicionar(tarefa)

        print("Tarefa adicionada com sucesso.")

    def _mudar_estado(self) -> None:

        id_tarefa = self._ler_inteiro(
            "ID da tarefa: "
        )

        novo_estado = input(
            "Novo estado "
            "(pendente/em curso/concluída): "
        ).strip().lower()

        self._servico.mudar_estado(
            id_tarefa,
            novo_estado
        )

        print("Estado alterado.")

    def _filtrar(self) -> None:

        estado = input(
            "Estado "
            "(pendente/em curso/concluída): "
        ).strip().lower()

        tarefas = self._servico.filtrar_por_estado(
            estado
        )

        if not tarefas:
            print("Nenhuma tarefa encontrada.")
            return

        for tarefa in tarefas:
            print()
            print(tarefa.detalhe())

    def _estatisticas(self) -> None:

        estatisticas = self._servico.estatisticas()

        print("\n=== Estatísticas ===")
        print(
            f"Total: "
            f"{estatisticas['total']}"
        )
        print(
            f"Horas estimadas: "
            f"{estatisticas['horas_estimadas']}"
        )
        print(
            f"Concluídas: "
            f"{estatisticas['percentagem_concluidas']:.2f}%"
        )

    def _guardar(self) -> None:

        self._servico.guardar()

        print(
            "Tarefas guardadas com sucesso."
        )

    def _carregar(self) -> None:

        self._servico.carregar()

        print(
            "Tarefas carregadas com sucesso."
        )

    def _exportar(self) -> None:

        tarefas = self._servico.listar()

        if not tarefas:
            print("(sem tarefas para exportar)")
            return

        print("\n=== Exportação ===")

        for tarefa in tarefas:
            print(tarefa.exportar())

    def _relatorio_custos(self) -> None:

        relatorio = (
            self._servico.relatorio_custos()
        )

        print("\n=== Relatório de Custos ===")

        if not relatorio["tarefas"]:
            print("(sem tarefas faturáveis)")
            return

        for item in relatorio["tarefas"]:
            print(
                f"[{item['id']}] "
                f"{item['titulo']} "
                f"({item['tipo']}): "
                f"{item['custo']:.2f} €"
            )

        print(
            f"Total: "
            f"{relatorio['total']:.2f} €"
        )

    def _ler_inteiro(
        self,
        mensagem: str
    ) -> int:

        while True:

            try:
                return int(
                    input(mensagem)
                )

            except ValueError:
                print(
                    "Introduz um número inteiro válido."
                )

    def _ler_float_positivo(
        self,
        mensagem: str
    ) -> float:

        while True:

            try:
                valor = float(
                    input(mensagem)
                )

                if valor <= 0:
                    raise ValueError

                return valor

            except ValueError:
                print(
                    "Introduz um número positivo válido."
                )