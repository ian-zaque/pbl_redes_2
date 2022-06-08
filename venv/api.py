from flask import Flask
from model.adm import Adm

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/')
def index():
    return '<h1>Encontre uma ONG</h1><p>Este site é um protótipo de API para encontrar ONGs pelo Brasil.</p>'

########## ROTAS LIXEIRA ##########
@app.route('/lixeiras/<number>', methods=['GET'])
def getLixeirasByNumber(number: int):
    try:
        lixeiras = Adm.getLixeirasByNumber(number)
        return str(lixeiras)
    except Exception as ex:
        return f"Erro: {ex}"

@app.route('/lixeira/<id>', methods=['GET'])
def getLixeiraByID(id):
    try:
        lixeiras = Adm.getLixeiraByID(id)
        return str(lixeiras)
    except Exception as ex:
        return f"Erro: {ex}"
########## ROTAS LIXEIRA ##########






























app.run()
