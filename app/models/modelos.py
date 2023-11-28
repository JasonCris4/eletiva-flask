from app import db
from flask_login import UserMixin


class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    telefone = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    is_UserMaster = db.Column(db.Boolean, nullable=False)
    senha = db.Column(db.String(255), nullable=False)

    def init(self, nome, email, telefone, is_UserMaster, senha ):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.telefone = telefone
        self.is_UserMaster = is_UserMaster