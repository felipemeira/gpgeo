from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models import Projeto

dashboard = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard.route('/')
@login_required
def dashboard_home():
    projetos = Projeto.get_by_usuario(current_user.id)
    return render_template('dashboard.html', projetos=projetos)
