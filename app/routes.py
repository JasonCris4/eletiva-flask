from flask import request, jsonify, make_response, redirect, url_for, render_template
from app import app, db
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_login import login_user, login_required, current_user, logout_user
from app.models.modelos import Usuario

bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return redirect(url_for('login_Usuarios'))

#-------------------------LOGIN USUARIOS -------------------------------
@app.route("/login", methods=['GET', 'POST'])
def login_Usuarios():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        usuario = Usuario.query.filter_by(email=email).first()

        if usuario and bcrypt.check_password_hash(usuario.senha, senha):
            
            login_user(usuario)
            return redirect(url_for('home'))
        else:
            return redirect(url_for('login_Usuarios'))
    else:
        return render_template('login.html')

@app.route("/criar-conta", methods=['GET', 'POST'])
def criar_conta():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        senha = request.form['senha']
        # Verificar se o e-mail já está cadastrado
        if Usuario.query.filter_by(email=email).first() is not None:
            return "E-mail já cadastrado", 400
        # Criação do usuário
        senhaHash=bcrypt.generate_password_hash(senha).decode('utf-8')
        print(senhaHash)
        novo_usuario = Usuario(nome=nome, email=email, is_UserMaster = False, senha=senhaHash, telefone=telefone)
        db.session.add(novo_usuario)
        db.session.commit()
        return render_template('login.html', info= 'Sucesso ao cadastar')
    else:
        return render_template('cadastrar.html')

@app.route("/sair")
def sair():
    logout_user()
    return redirect(url_for('login_Usuarios'))

@app.route("/home")
@login_required
def home():
    if current_user.is_authenticated:
        return render_template('index.html', usuario = current_user.is_UserMaster)
    else:
        return redirect(url_for('login_Usuarios'))



@app.route("/ADMIN", methods=['GET'])
@login_required
def get_Usuarios():
    Usuarios = Usuario.query.all()
    lista_Usuarios = []

    for usuario in Usuarios:
        lista_Usuarios.append({
            'id': usuario.id,
            'nome': usuario.nome,
            'telefone': usuario.telefone,
            'email': usuario.email,
            'senha': usuario.senha

        })

    return render_template('admin.html', usuarios= lista_Usuarios)


@app.route("/editar-usuario/<int:user_id>", methods=['GET', 'POST'])
@login_required
def editar_usuario(user_id):
    usuario = Usuario.query.get(user_id)

    if request.method == 'POST':
        # Atualizar informações do usuário com base nos dados do formulário
        usuario.nome = request.form['nome']
        usuario.telefone = request.form['telefone']
        usuario.email = request.form['email']
        
        # Verifique se a senha foi alterada antes de gerar o hash novamente
        if request.form['senha']:
            senha_hash = bcrypt.generate_password_hash(request.form['senha']).decode('utf-8')
            usuario.senha = senha_hash
        
        # Salvar no banco de dados
        db.session.commit()

        return redirect(url_for('get_Usuarios'))

    return render_template('atualizar.html', usuario=usuario)


@app.route("/remover-usuario/<int:user_id>", methods=['GET'])
@login_required
def remover_usuario(user_id):
    usuario = Usuario.query.get(user_id)
    
    db.session.delete(usuario)
    db.session.commit()

    return redirect(url_for('get_Usuarios'))


# Remover Usuario
@app.route("/Usuarios/<int:Usuario_id>", methods=['DELETE'])
def delete_Usuario(Usuario_id):
    usuario = Usuario.query.get(Usuario_id)
    if not usuario:
        return jsonify({'status': 404, 'message': 'Usuario não encontrado'}), 404

    db.session.delete(usuario)
    db.session.commit()
    return jsonify({'status': 200, 'message': 'Usuario deletado com sucesso'}), 200




#@app.route('/ADMIN', methods=['GET', 'POST'])
#@login_required  # Supondo que você tenha um sistema de login
#def admin_panel():
    if current_user.is_authenticated and current_user.is_admin:  # Verificação do usuário administrador
        if request.method == 'POST':
            if request.form['_method'] == 'DELETE':
                user_id = int(request.form['user_id'])
                user_to_delete = Usuario.query.get_or_404(user_id)
                db.session.delete(user_to_delete)
                db.session.commit()
                return redirect(url_for('admin_panel'))

            elif request.form['_method'] == 'PUT':
                user_id = int(request.form['user_id'])
                user_to_update = Usuario.query.get_or_404(user_id)
                new_username = request.form['new_username']
                user_to_update.nome = new_username  # Ajustar para o campo correto
                db.session.commit()
                return redirect(url_for('admin_panel'))

        usuarios = Usuario.query.all()
        return render_template('admin.html', usuarios=usuarios)
    else:
        return redirect(url_for('login_Usuarios'))



