from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user
from app.services.user import authenticate, register

from app.forms import LoginForm, RegisterForm
from app.models import User

from app.extensions import login_manager


auth_bp = Blueprint('auth', __name__)

login_manager.login_view = 'auth.login'

# Loader para recuperar el usuario de la sesión
@login_manager.user_loader
def load_user(username):
    return User.query.get(username)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        if authenticate(username, password):
            return redirect(url_for('symptoms.symptoms_history'))
        else:
            flash('Credenciales inválidas', 'danger')
    
    return render_template('login.html', form=form)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register_():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        status = register(username, password)
        
        if status == 200:
            flash('Registrado correctamente. Inicia sesión.', 'success')
            return redirect(url_for('auth.login'))
        elif status == 409:
            flash('Este usuario ya existe.', 'warning')
        else:
            flash('Error interno del servidor.', 'danger')
    
    return render_template('register.html', form=form)



@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión correctamente.', 'info')
    return redirect(url_for('auth.login'))
