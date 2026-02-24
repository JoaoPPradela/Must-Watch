from sqlite3 import Connection, connect, Cursor
from typing import Any, Optional, Self, Type
from types import TracebackType
from dotenv import load_dotenv
import traceback
import os

# --- Configurações de Ambiente e Caminho do Banco ---
load_dotenv() # Carrega as configurações do arquivo .env
DB_PATH = os.getenv('DATABASE', './data/lista.sqlite3')

# --- Função para criar a tabela se ela não existir ---
def init_db(db_name: str = DB_PATH):
    with connect(db_name) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS atividades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo_atividade TEXT NOT NULL,
            tipo_de_atividade TEXT,
            indicado_por TEXT      
        );
        """)

# --- Classe que gerencia a conexão com o Banco ---
class Database:
    """
    Classe que controla as conexões e garante que o banco 
    seja fechado corretamente após o uso.
    """
    
    # Inicia a conexão e garante que a tabela exista
    def __init__(self, db_name: str = DB_PATH) -> None:
        self.connection: Connection = connect(db_name)
        self.cursor: Cursor = self.connection.cursor()
        self.executar("""
        CREATE TABLE IF NOT EXISTS atividades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo_atividade TEXT NOT NULL,
            tipo_de_atividade TEXT,
            indicado_por TEXT      
        );
        """)

    # Executa comandos como INSERT, UPDATE e DELETE
    def executar(self, query: str, params: tuple = ()) -> Cursor:
        self.cursor.execute(query, params)
        self.connection.commit() # Salva as alterações
        return self.cursor

    # Executa comandos de busca (SELECT)
    def buscar_tudo(self, query: str, params: tuple = ()) -> list[Any]:
        self.cursor.execute(query, params)
        return self.cursor.fetchall() # Retorna a lista de dados

    # Fecha a conexão manualmente
    def close(self) -> None:
        self.connection.close()

    # Gerenciamento automático (usando o 'with') 

    # O que acontece quando você abre o 'with Database()
    def __enter__(self) -> Self:
        return self

    # O que acontece quando você sai do bloco 'with'
    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        tb: Optional[TracebackType],
    ) -> None:
        # Se houver erro durante o uso, ele imprime os detalhes aqui
        if exc_type is not None:
            print("Exceção capiturar no contexto: ")
            print(f"Tipo: {exc_type.__name__}")
            print(f"Mensagem: {exc_value}")
            print("Traceback completo:")
            traceback.print_tb(tb)

        # Fecha a conexão automaticamente ao sair
        self.close()