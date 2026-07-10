import os
import sys
from fastapi.middleware.cors import CORSMiddleware

sys.path.insert(
    0,
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)


from fastapi import FastAPI
from pydantic import BaseModel

from dominio.tarefa_tecnica import TarefaTecnica
from servico.servico_tarefas import ServicoTarefas
from repositorio.repositorio_ficheiro import RepositorioFicheiro

app = FastAPI(title="Gestão de Tarefas")

app = FastAPI(title="Gestão de Tarefas")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "http://127.0.0.1:8080"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_servico = ServicoTarefas(
    RepositorioFicheiro("tarefas.csv")
)

_servico.adicionar(
    TarefaTecnica(
        _servico.proximo_id(),
        "Script de ETL",
        "Ana",
        "Python",
        8
    )
)


class NovaTarefaTecnica(BaseModel):
    titulo: str
    responsavel: str
    linguagem: str
    estimativa_horas: float


class NovoEstado(BaseModel):
    estado: str


def para_dict(tarefa):

    return {
        "id": tarefa.id,
        "titulo": tarefa.titulo,
        "responsavel": tarefa.responsavel,
        "estado": tarefa.estado,
        "tipo": tarefa.tipo(),
        "resumo": tarefa.resumo()
    }


@app.get("/")
def inicio():

    return {
        "mensagem": "API Gestão de Tarefas"
    }


@app.get("/tarefas")
def listar_tarefas():

    return [
        para_dict(t)
        for t in _servico.listar()
    ]


@app.post("/tarefas")
def criar_tarefa(
    dados: NovaTarefaTecnica
):

    tarefa = TarefaTecnica(
        _servico.proximo_id(),
        dados.titulo,
        dados.responsavel,
        dados.linguagem,
        dados.estimativa_horas
    )

    _servico.adicionar(tarefa)

    return para_dict(tarefa)


@app.put("/tarefas/{id_tarefa}/estado")
def mudar_estado(
    id_tarefa: int,
    dados: NovoEstado
):

    _servico.mudar_estado(
        id_tarefa,
        dados.estado
    )

    return {
        "mensagem": "Estado atualizado"
    }


@app.get("/tarefas/estado/{estado}")
def filtrar_estado(
    estado: str
):

    return [
        para_dict(t)
        for t in _servico.filtrar_por_estado(
            estado
        )
    ]


@app.get("/estatisticas")
def estatisticas():

    return _servico.estatisticas()