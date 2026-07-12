import os
import sys

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

sys.path.insert(
    0,
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from dominio.colaborador import Colaborador
from dominio.tarefa_tecnica import TarefaTecnica
from repositorio.repositorio_ficheiro import RepositorioFicheiro
from servico.servico_tarefas import ServicoTarefas


app = FastAPI(
    title="Gestão de Tarefas"
)

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
    RepositorioFicheiro(
        "tarefas.csv"
    )
)


class NovoColaborador(BaseModel):
    nome: str
    email: str


class NovaTarefaTecnica(BaseModel):
    titulo: str
    responsavel: NovoColaborador
    linguagem: str
    estimativa_horas: float


class NovoEstado(BaseModel):
    estado: str


def para_dict(tarefa) -> dict:

    return {
        "id": tarefa.id,
        "titulo": tarefa.titulo,
        "responsavel": {
            "nome": tarefa.responsavel.nome,
            "email": tarefa.responsavel.email
        },
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
        para_dict(tarefa)
        for tarefa in _servico.listar()
    ]


@app.post("/tarefas")
def criar_tarefa(
    dados: NovaTarefaTecnica
):

    try:
        responsavel = Colaborador(
            dados.responsavel.nome,
            dados.responsavel.email
        )

        tarefa = TarefaTecnica(
            _servico.proximo_id(),
            dados.titulo,
            responsavel,
            dados.linguagem,
            dados.estimativa_horas
        )

        _servico.adicionar(tarefa)

        return para_dict(tarefa)

    except (ValueError, TypeError) as erro:
        raise HTTPException(
            status_code=400,
            detail=str(erro)
        )


@app.put("/tarefas/{id_tarefa}/estado")
def mudar_estado(
    id_tarefa: int,
    dados: NovoEstado
):

    try:
        _servico.mudar_estado(
            id_tarefa,
            dados.estado
        )

        return {
            "mensagem": "Estado atualizado"
        }

    except ValueError as erro:
        raise HTTPException(
            status_code=400,
            detail=str(erro)
        )


@app.get("/tarefas/estado/{estado}")
def filtrar_estado(
    estado: str
):

    return [
        para_dict(tarefa)
        for tarefa in _servico.filtrar_por_estado(
            estado
        )
    ]


@app.get("/estatisticas")
def estatisticas():

    return _servico.estatisticas()


@app.get("/custos")
def relatorio_custos():

    return _servico.relatorio_custos()