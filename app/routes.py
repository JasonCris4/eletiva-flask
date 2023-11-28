from flask import request, jsonify, make_response, redirect, url_for, render_template
from app import app, db
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_login import login_user, login_required, current_user, logout_user
from app.models.modelos import Usuario

bcrypt = Bcrypt(app)

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
        return redirect('/login', info= 'Sucesso ao cadastar')
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
        return render_template('index.html')
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

    return jsonify(lista_Usuarios)

@app.route("/ADM", methods=['POST'])
def create_Usuario():
    dados = request.json
    _nome = dados["nome"]
    _email = dados["email"]
    _senha = dados["senha"]
    _telefone = dados["telefone"]

    usuario = Usuario(nome=_nome, senha=_senha, email=_email, telefone=_telefone)
    db.session.add(Usuario)
    db.session.commit()

    return jsonify({'status': 201, 'message': 'Usuario criado com sucesso', 'data': usuario.id}), 201


@app.route("/Usuarios/<int:Usuario_id>", methods=['PUT'])
def update_Usuario(Usuario_id):
    
    usuario = Usuario.query.get(Usuario_id)
    if not usuario:
        return jsonify({'status': 404, 'message': 'Usuario não encontrado'}), 404
    
    dados = request.json

   
    usuario.nome = dados.get("nome", usuario.nome)
    usuario.senha = dados.get("senha", usuario.senha)
    usuario.email = dados.get("email", usuario.email)
    usuario.telefone = dados.get("telefone", usuario.telefone)


    db.session.commit()

    return jsonify({'status': 200, 'message': 'Usuario atualizado com sucesso'}), 200


# Remover Usuario
@app.route("/Usuarios/<int:Usuario_id>", methods=['DELETE'])
def delete_Usuario(Usuario_id):
    usuario = Usuario.query.get(Usuario_id)
    if not usuario:
        return jsonify({'status': 404, 'message': 'Usuario não encontrado'}), 404

    db.session.delete(usuario)
    db.session.commit()
    return jsonify({'status': 200, 'message': 'Usuario deletado com sucesso'}), 200





