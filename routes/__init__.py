from flask import Blueprint

main = Blueprint('main', __name__)
produtos = Blueprint('produtos', __name__)
fornecedores = Blueprint('fornecedores', __name__)
estoque = Blueprint('estoque', __name__)

from . import produtos, fornecedores, estoque