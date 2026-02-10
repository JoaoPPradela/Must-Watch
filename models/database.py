from sqlite3 import Connection, connect, Cursor
from typing import Any, Optional, Self, Type
from types import TracebackType
from dotenv import load_dotenv
import traceback
import os


# Carrega variáveis de ambiente se necessário
load_dotenv()

class Database:
    def __init__(self, db_name: str = "database.db"):
        self.db_name: str = db_name
        self.connection: Optional[Connection] = None

    def __enter__(self) -> Self:
        self.connection = connect(self.db_name)
        self.connection.row_factory = Any # Permite acessar colunas por nome ou índice
        return self

    def __exit__(
        self, 
        exc_type: Optional[Type[BaseException]], 
        exc_val: Optional[BaseException], 
        exc_tb: Optional[TracebackType]
    ) -> None:
        if self.connection:
            if exc_type is None:
                self.connection.commit()
            else:
                self.connection.rollback() # Cancela mudanças se houver erro
            self.connection.close()

    def executar(self, query: str, params: tuple = ()) -> Cursor:
        if self.connection:
            cursor: Cursor = self.connection.cursor()
            cursor.execute(query, params)
            return cursor
        raise ConnectionError("Banco de dados não conectado.")

    def buscar_tudo(self, query: str, params: tuple = ()) -> list[tuple]:
        if self.connection:
            cursor: Cursor = self.connection.cursor()
            cursor.execute(query, params)
            # Retorna lista de tuplas para bater com o desempacotamento do seu Model
            return [tuple(row) for row in cursor.fetchall()]
        raise ConnectionError("Banco de dados não conectado.")

def init_db() -> None:
    query = """
    CREATE TABLE IF NOT EXISTS tarefas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        tipo TEXT NOT NULL,
        indicado_por TEXT
    );
    """
    try:
        with Database() as db:
            db.executar(query)
    except Exception:
        print("Erro ao inicializar o banco de dados:")
        traceback.print_exc()