from sqlite3 import Connection, connect, Cursor
from typing import Any, Optional, Self, Type
from types import TracebackType
from dotenv import load_dotenv
import traceback
import os

load_dotenv() # Procura um arquivo .env com variáveis 
DB_PATH = os.getenv('DATABASE', './data/lista.sqlite3')

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

class Database:
    """
        Classe que regencia conexões e operações com o banco de dados SQLitre. Utiliza o protocolo de gerenciamento de contxtos para garantir qua a conexão seja encerrada corretamente
    """
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

    def executar(self, query: str, params: tuple = ()) -> Cursor:
        self.cursor.execute(query, params)
        self.connection.commit()
        return self.cursor

    def buscar_tudo(self, query: str, params: tuple = ()) -> list[Any]:
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def close(self) -> None:
        self.connection.close()

    # Métodos para o gerenciamento de contexto

    # Método de entrada do contexto
    def __enter__(self) -> Self:
        return self

    # Método de saída do contexto
    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        tb: Optional[TracebackType],
    ) -> None:
        if exc_type is not None:
            print("Exceção capiturar no contexto: ")
            print(f"Tipo: {exc_type.__name__}")
            print(f"Mensagem: {exc_value}")
            print("Traceback completo:")
            traceback.print_tb(tb)

        self.close()