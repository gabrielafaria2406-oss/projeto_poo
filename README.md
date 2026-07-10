# Backend de Gestão de Tarefas — Python

## Como correr

```bash
cd python
python main.py
```

Abre um menu de consola. A opção **Listar** já funciona (com 2 tarefas de
exemplo). As opções marcadas com `[TODO]` ainda não estão feitas — mostram
uma mensagem em vez de rebentar o programa. São essas que vais implementar.

## Ordem de leitura (de baixo para cima)

As camadas dependem sempre da de baixo. Lê por esta ordem:

1. **`dominio/`** — o quê (os objetos)
   - `tarefa.py` — classe base **abstrata** (abstração, encapsulamento, polimorfismo) ✅
   - `tarefa_tecnica.py` — subclasse **completa**, o teu exemplo trabalhado (herança) ✅
   - `tarefa_reuniao.py` — subclasse a **completar** 🔲
   - `exportavel.py` — interface a **criar** e implementar (tarefa 4) 🔲
2. **`repositorio/`** — onde se guarda
   - `i_repositorio.py` — **interface** (contrato de persistência) ✅
   - `repositorio_ficheiro.py` — implementação em CSV: `guardar()` ✅ / `carregar()` 🔲
3. **`servico/`** — as regras de negócio
   - `servico_tarefas.py` — `adicionar()`/`listar()`/`proximo_id()` ✅ / resto 🔲
4. **`interface/`** — a frente de consola
   - `consola.py` — ciclo do menu + "Listar" + "Sair" ✅ / restantes opções 🔲
5. **`main.py`** — liga tudo (repositório → serviço → consola) ✅

> Regra de dependência: o **serviço** só conhece o **domínio** e a **interface**
> do repositório. Nunca a consola nem o ficheiro. A frente é descartável — ver
> a frente **bónus** em `bonus_api_web/`.

## Lista de TODOs (o teu exercício)

- [ ] `dominio/tarefa_reuniao.py` — espelhar a `TarefaTecnica`
- [ ] `repositorio/repositorio_ficheiro.py` → `carregar()`
- [ ] `servico/servico_tarefas.py` → `mudar_estado()`, `filtrar_por_estado()`, `estatisticas()`
- [ ] `dominio/exportavel.py` — criar a interface `Exportavel` (tarefa 4) e implementá-la em ≥1 classe
- [ ] `interface/consola.py` → opções "Adicionar", "Mudar estado", "Filtrar", "Estatísticas", "Exportar", "Guardar", "Carregar"
- [ ] (bónus) `bonus_api_web/` — ver o README de lá

## Mapa pilar → camada

| Pilar de POO    | Onde vive                                          |
|-----------------|----------------------------------------------------|
| Abstração       | `Tarefa` (abstrata) + interface `IRepositorio`     |
| Encapsulamento  | atributos privados (`_`) + `@property` no domínio  |
| Herança         | `TarefaTecnica` / `TarefaReuniao` (sub de `Tarefa`)|
| Polimorfismo    | `resumo()` / `tipo()` redefinidos por subclasse    |
| Interface       | `IRepositorio` e `Exportavel` (tarefa 4); no bónus, a API web |
