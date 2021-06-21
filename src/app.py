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
    addres = db.Column (db.String(70))

    def __init__(self, product, desc, addres):
        self.product = product
        self.desc = desc
        self.addres = addres

db.create_all() #Crea todas las tablas especificadas

#Esquema que interactua
class RopaInfo(ma.Schema): #necesario para ver informacion de la base luego de eliminar algo
    class Meta: 
        fields = ('id', 'product', 'desc', 'addres') #campos, info

ropa_info = RopaInfo() #envia una sola respuesta
ropas_info = RopaInfo(many = True) #Devuelve varias respuesta

@app.route('/')
def index():
    return jsonify({'message':'Welcome to my API'})

@app.route('/POST-ropa', methods = ['POST'])
def create_ropa():
    product = request.json['product']
    desc = request.json['desc']
    addres = request.json['addres']

    new_Ropa = Ropa(product, desc, addres) #save is ropaif __name__ == "__main__":
    db.session.add(new_Ropa) #Asigna la tarea en BBDD
    db.session.commit() #termino operacion

    return ropa_info.jsonify(new_Ropa) #Vemos por consola lo que envias al bbdd

@app.route('/GET-ropa')
def get_ropas():
    all_ropas = Ropa.query.all()
    result = ropas_info.dump(all_ropas)
    return jsonify(result)

@app.route('/GET-ropa/<id>')
def get_ropa(id):
    ropa = Ropa.query.get(id)
    return ropa_info.jsonify(ropa)

#actualizar mediante ID
@app.route('/PUT-ropa/<id>', methods = ['PUT'])
def update_ropa(id):
    ropa = Ropa.query.get(id) #Obtener, peticion

    product = request.json['product'] #Traigo el dato, y lo guardo en variables
    desc = request.json['desc']
    addres = request.json['addres']

    ropa.product = product #Asigno los valores a la tabla
    ropa.desc = desc
    ropa.addres = addres

    db.session.commit()
    return ropa_info.jsonify(ropa) #Traeme el dato actualizado

@app.route('/DELETE-ropa/<id>', methods = ['DELETE'])
def delete_ropa(id):
    ropa = Ropa.query.get(id) #Obtengo ropa/ Get cloting
    db.session.delete(ropa) #delete cloting
    db.session.commit() #close operation

    return ropa_info.jsonify(ropa)

if __name__ == "__main__":
    app.run(debug = True)