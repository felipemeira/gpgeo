from flask_login import UserMixin
from werkzeug.security import check_password_hash
from db import get_conn

class Usuario(UserMixin):
    def __init__(self, id, username, senha_hash):
        self.id = id
        self.username = username
        self.senha_hash = senha_hash

    @staticmethod
    def get_by_username(username):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT id, username, senha_hash FROM usuarios WHERE username = %s", (username,))
        data = cur.fetchone()
        conn.close()
        if data:
            return Usuario(id=data['id'], username=data['username'], senha_hash=data['senha_hash'])
        return None

    def check_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

class Projeto:
    def __init__(self, id, nome):
        self.id = id
        self.nome = nome
        self.mapas = []

    @staticmethod
    def get_by_usuario(usuario_id):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            SELECT p.id, p.nome
            FROM projetos p
            JOIN usuarios_projetos up ON up.projeto_id = p.id
            WHERE up.usuario_id = %s
        """, (usuario_id,))
        projetos = []
        for row in cur.fetchall():
            projeto = Projeto(id=row['id'], nome=row['nome'])
            projeto.mapas = Mapa.get_by_projeto(row['id'])
            projetos.append(projeto)
        conn.close()
        return projetos

class Mapa:
    def __init__(self, id, nome, camada_geoserver=None):
        self.id = id
        self.nome = nome
        self.camada_geoserver = camada_geoserver

    @staticmethod
    def get_by_projeto(projeto_id):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            SELECT id, nome
            FROM mapas
            WHERE projeto_id = %s
        """, (projeto_id,))
        mapas = []
        for row in cur.fetchall():
            mapas.append(Mapa(id=row['id'], nome=row['nome']))
        conn.close()
        return mapas