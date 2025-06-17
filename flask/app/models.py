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
