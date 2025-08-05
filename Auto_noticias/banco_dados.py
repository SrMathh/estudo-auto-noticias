import sqlite3
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_name='noticias.db'):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def criar_tabela(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS resumos(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data_coleta TEXT NOT NULL,
                ativo_pesquisado TEXT NOT NULL,
                titulo_noticia TEXT NOT NULL,
                resumo_ia TEXT NOT NULL,
                url_noticia TEXT
                )'''
        )
        self.conn.commit()
        print("Tabela 'resumos' criada ou já existe.")

    def inserir_resumo(self, ativo_pesquisado, titulo_noticia, resumo_ia, url_noticia):
        data_atual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            self.cursor.execute('''
                INSERT INTO resumos(data_coleta, ativo_pesquisado, titulo_noticia, resumo_ia, url_noticia)
                VALUES (?, ?, ?, ?, ?)
            ''', (data_atual, ativo_pesquisado, titulo_noticia, resumo_ia, url_noticia))
            self.conn.commit()
            print("Resumo inserido com sucesso.")
        except Exception as e:
            print("Erro ao inserir resumo:", e)

    def fechar_conexao(self):
        self.conn.close()
        print("Conexão com o banco de dados fechada.")