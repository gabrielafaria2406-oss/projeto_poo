class ErroDominio(Exception):
    """Classe base para erros das regras do domínio."""


class TransicaoEstadoInvalida(ErroDominio):
    """Usada quando uma tarefa tenta mudar para um estado proibido."""


class DependenciasPendentes(ErroDominio):
    """Usada quando uma tarefa tenta iniciar com dependências pendentes."""


class DependenciaInvalida(ErroDominio):
    """Usada quando uma dependência não pode ser adicionada."""


class TarefaNaoEncontrada(ErroDominio):
    """Usada quando não existe uma tarefa com o ID informado."""