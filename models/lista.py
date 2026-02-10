from sqlite3 import Cursor
from typing import Optional, Self, Any
from models.database import Database

class Tarefa:
    def __init__(
        self, 
        titulo: str, 
        tipo: str, 
        indicado_por: str, 
        id_tarefa: Optional[int] = None
    ) -> None:
        self.id_tarefa: Optional[int] = id_tarefa
        self.titulo: str = titulo
        self.tipo: str = tipo
        self.indicado_por: str = indicado_por

    @classmethod
    def id(cls, id: int) -> Optional[Self]:
        with Database() as db:
            # Busca os campos exatos da nova estrutura
            query: str = 'SELECT titulo, tipo, indicado_por FROM tarefas WHERE id = ?;'
            params: tuple = (id,)
            resultado: list[tuple] = db.buscar_tudo(query, params)
            
            if not resultado:
                return None

            # Desempacotamento seguro da lista de resultados
            [[titulo, tipo, indicado_por]] = resultado

        return cls(titulo=titulo, tipo=tipo, indicado_por=indicado_por, id_tarefa=id)
        
    def salvar_tarefa(self: Self) -> None:
        with Database() as db:
            # Inserção seguindo a nova ordem de colunas
            query: str = "INSERT INTO tarefas (titulo, tipo, indicado_por) VALUES (?, ?, ?);"
            params: tuple = (self.titulo, self.tipo, self.indicado_por)
            db.executar(query, params)

    @classmethod
    def obter_tarefas(cls) -> list[Self]:
        with Database() as db:
            # Seleciona todos os itens para renderizar na lista
            query: str = 'SELECT titulo, tipo, indicado_por, id FROM tarefas;'
            resultados: list[Any] = db.buscar_tudo(query)
            
            # List comprehension para converter as linhas do banco em objetos Tarefa
            tarefas: list[Self] = [
                cls(titulo, tipo, indicado, id_reg) 
                for titulo, tipo, indicado, id_reg in resultados
            ]
            return tarefas
    
    def excluir_tarefa(self: Self) -> Cursor:
        with Database() as db:
            query: str = 'DELETE FROM tarefas WHERE id = ?;'
            params: tuple = (self.id_tarefa,)
            resultado: Cursor = db.executar(query, params)
            return resultado
    
    def atualizar_tarefas(self: Self) -> Cursor:
        with Database() as db:
            # Atualiza todos os campos baseados no ID oculto
            query: str = 'UPDATE tarefas SET titulo = ?, tipo = ?, indicado_por = ? WHERE id = ?;'
            params: tuple = (self.titulo, self.tipo, self.indicado_por, self.id_tarefa)
            resultado: Cursor = db.executar(query, params)
            return resultado