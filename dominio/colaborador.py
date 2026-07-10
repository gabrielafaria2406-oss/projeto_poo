class Colaborador:

    def __init__(self, nome: str, email: str):
        self._nome = nome
        self._email = email

    @property
    def nome(self):
        return self._nome

    @property
    def email(self):
        return self._email

    def __str__(self):
        return self._nome
