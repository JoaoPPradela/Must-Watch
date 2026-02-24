from sqlite3 import Cursor
from typing import Optional, Self, Any
from models.database import Database

class Atividade:
    """
    Classe para representar uma atividade, com métodos para salvar, 
    obter, excluir e atualizar no banco de dados.
    """
    
    # --- Criação do objeto Atividade ---
    def __init__(self, titulo_atividade: Optional[str], tipo_de_atividade: Optional[str] = None, indicado_por: Optional[str] = None, id_atividade: Optional[int] = None) -> None:
        self.titulo_atividade: Optional[str] = titulo_atividade
        self.tipo_de_atividade: Optional[str] = tipo_de_atividade
        self.indicado_por: Optional[str] = indicado_por
        self.id_atividade: Optional[int] = id_atividade
        
    # Busca de uma atividade específica 
    @classmethod
    def id(cls, id: int) -> Self:
        """ Busca no banco uma atividade pelo ID e retorna um objeto da classe """
        with Database() as db:
            query: str = 'SELECT titulo_atividade, tipo_de_atividade, indicado_por FROM atividades WHERE id = ?;'
            params: tuple = (id,)
            resultado = db.buscar_tudo(query, params)
            print(resultado)

            # Transforma a linha do banco em variáveis
            [[titulo, tipo, indicado]] = resultado

        return cls(id_atividade=id, titulo_atividade=titulo, tipo_de_atividade=tipo, indicado_por=indicado)
        
    #Salvar nova atividade no banco de dados
    def salvar_atividade(self: Self)-> None:
        """ Insere os dados da atividade atual no banco de dados """
        with Database() as db:
            query: str = " INSERT INTO atividades (titulo_atividade, tipo_de_atividade, indicado_por) VALUES (?, ?, ?);"
            params: tuple = (self.titulo_atividade, self.tipo_de_atividade, self.indicado_por)
            db.executar(query, params)

    #Listar todas as atividades cadastradas
    @classmethod
    def obter_atividades(cls) -> list[Self]:
        """ Retorna uma lista com todas as atividades cadastradas """
        with Database() as db:
            query: str = 'SELECT titulo_atividade, tipo_de_atividade, indicado_por, id FROM atividades;'
            resultados: list[Any] = db.buscar_tudo(query)
            # Converte cada linha encontrada em um objeto da classe Atividade
            atividades: list[Any] = [cls(titulo, tipo, indicado_por, id) for titulo, tipo, indicado_por, id in resultados]
            return atividades
    
    #Remover atividade 
    def excluir_atividade(self) -> Cursor:
        """ Remove a atividade do banco de dados usando o ID """
        with Database() as db:
            query: str = 'DELETE FROM atividades WHERE id = ?;'
            params: tuple = (self.id_atividade,)
            resultado: Cursor = db.executar(query, params)
            return resultado
    
    # Editar atividade existente
    def atualizar_atividade(self) -> Cursor:
        """ Atualiza todas as informações de uma atividade já existente """
        with Database() as db:
            query: str = 'UPDATE atividades SET titulo_atividade = ?, tipo_de_atividade = ?, indicado_por = ? WHERE id = ?;'
            params: tuple = (self.titulo_atividade, self.tipo_de_atividade, self.indicado_por, self.id_atividade)
            resultado: Cursor = db.executar(query, params)
            return resultado