from flask import Flask, render_template
from flask_login import LoginManager
from models import Usuario
from auth import auth
from dashboard import dashboard
from db import get_conn 

app = Flask(__name__)
app.secret_key = 'sua-chave-secreta-aqui'  # troque para algo seguro

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    from models import Usuario
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, username, senha_hash FROM usuarios WHERE id = %s", (user_id,))
    data = cur.fetchone()
    conn.close()
    if data:
        return Usuario(id=data['id'], username=data['username'], senha_hash=data['senha_hash'])
    return None

# REGISTRAR OS BLUEPRINTS
app.register_blueprint(auth)
app.register_blueprint(dashboard)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
