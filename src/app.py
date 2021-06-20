from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy #de esta forma interactuamos mas facil con la BBDD
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/sql_alchemy'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app) #instancia de baso de datos
ma = Marshmallow(app)

#Creamos tablas
class Ropa(db.Model):
    id = db.Column (db.Integer, primary_key = True) #Sera tipo int, first
    product = db.Column (db.String(70), unique = True) #Sera irrepetible, de long 70carac
    desc = db.Column (db.String(100))
    addres = db.Column (db.String(70), unique = True)

    def __init__(self, produc, desc, addres):
        self.product = produc
        self.desc = desc
        self.addres = addres

db.create_all() #Crea todas las tablas especificadas

#Esquema que interactua
class RopaInfo(ma.Schema):
    class Meta: 
        fields = ('id', 'produc', 'desc', 'addres') #campos

ropa_info = RopaInfo() #envia una sola respuesta
ropas_info = RopaInfo(many = True) #Devuelve varias respuesta

@app.route('/')
def index():
    return jsonify({'message':'Welcome to my API'})

@app.route('/POST-ropa', methods = ['POST'])
def create_ropa():
    product = request.json['product']
    desc = request.json['desc']
    addres = request.json['desc']

    new_Ropa = Ropa(product, desc, addres) #save is ropaif __name__ == "__main__":
    db.session.add(new_Ropa) #Asigna la tarea en BBDD
    db.session.commit() #termino operacion

    return ropa_info.jsonify(new_Ropa) #Vemos por consola lo que envias al bbdd

@app.route('/GET-ropa')
def get_ropa():
    all_ropas = Ropa.query.all()
    result = ropas_info.dump(all_ropas)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug = True)