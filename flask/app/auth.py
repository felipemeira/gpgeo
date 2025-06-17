from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from models import Usuario

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        senha = request.form['senha']

        usuario = Usuario.get_by_username(username)
        if usuario and usuario.check_senha(senha):
            login_user(usuario)
            return redirect(url_for('dashboard.dashboard_home'))
        else:
            flash('Credenciais inválidas', 'error')

    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
