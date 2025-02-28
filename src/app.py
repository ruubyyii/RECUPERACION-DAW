from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_pymongo import PyMongo
from bson import ObjectId

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb+srv://minguitojefe:12345@cluster0.nxdnc.mongodb.net/RECUPERACION-DAW'
mongo = PyMongo(app)

app.config['MYSQL_HOST'] = 'bhdjodozhpq3ald4sdwh-mysql.services.clever-cloud.com'
app.config['MYSQL_USER'] = 'uzc0jbgvcd51eamd'
app.config['MYSQL_PASSWORD'] = 'cVSD4YIxtnz8eqPI3cDB'
app.config['MYSQL_DB'] = 'bhdjodozhpq3ald4sdwh'

db = MySQL(app)

######################### MONGO #########################

@app.route('/addUser_m', methods=['POST'])
def addUser_m():
    
    nombre = request.json['nombre']
    apellido = request.json['apellido']
    color = request.json['color']
    numero = request.json['numero']

    if id and nombre and apellido and color:

        mongo.db.users.insert_one({'nombre': nombre, 'apellido': apellido, 'color': color, 'numero': numero})
        return jsonify({'message': 'Se ha insertado con exito!'})
    return jsonify({'message': 'Error al insertar usuario!!'})

@app.route('/getUsers_m')
def getUsers_m():

    users =  mongo.db.users.find()
    return jsonify(users)

@app.route('/getUser_m/<id>')
def getUser_m(id):

    user =  mongo.db.users.find_one({'_id': ObjectId(id)})
    return jsonify(user)

@app.route('/deleteUser_m/<id>', methods=['DELETE'])
def deleteUser_m(id):
    
    mongo.db.users.delete_one({'_id': ObjectId(id)})
    return jsonify({'message': 'Se ha eliminado con exito!'})

@app.route('/updateUser_m/<id>', methods=['PUT'])
def updateUser_m(id):

    nombre = request.json['nombre']
    apellido = request.json['apellido']
    color = request.json['color']
    numero = request.json['numero']

    if nombre and apellido and color and numero:
        
        mongo.db.users.update_one({'_id': ObjectId(id)}, {'$set': {'nombre': nombre, 'apellido': apellido, 'color': color, 'numero': numero}})
        return jsonify({'message': 'Se ha actualizado con exito!'})
    return jsonify({'message': 'Error al actualizar usuario!!'})

######################### MYSQL #########################

@app.route('/addUser_s', methods=['POST'])
def addUser_s():
    
    nombre = request.json['nombre']
    apellido = request.json['apellido']
    color = request.json['color']
    numero = request.json['numero']

    if id and nombre and apellido and color:

        cur = db.connection.cursor()
        cur.execute('INSERT INTO users VALUES (NULL, %s, %s, %s, %s)', (nombre, apellido, color, numero))
        db.connection.commit()

        return jsonify({'message': 'Se ha insertado con exito!'})
    return jsonify({'message': 'Error al insertar usuario!!'})

@app.route('/getUsers_s')
def getUsers_s():

    cur = db.connection.cursor()
    cur.execute('SELECT * from users')
    users = cur.fetchall()

    return jsonify(users)

@app.route('/getUser_s/<id>')
def getUser_s(id):

    cur = db.connection.cursor()
    cur.execute('SELECT * FROM users WHERE id = %s', (id,))
    user = cur.fetchone()

    return jsonify(user)

@app.route('/deleteUser_s/<id>', methods=['DELETE'])
def deleteUser_s(id):

    cur = db.connection.cursor()
    cur.execute('DELETE FROM users WHERE id = %s', (id,))
    db.connection.commit()

    return jsonify({'message': 'Usuario eliminado con exito!'})

@app.route('/updateUser_s/<id>', methods=['PUT'])
def updateUser_s(id):

    nombre = request.json['nombre']
    apellido = request.json['apellido']
    color = request.json['color']
    numero = request.json['numero']

    cur = db.connection.cursor()
    cur.execute('UPDATE users SET nombre=%s, apellido = %s, color = %s, numero = %s WHERE id = %s', (nombre, apellido, color, numero, id))
    db.connection.commit()

    return jsonify({'message': 'Usuario actualizado con exito!'})

@app.route('/updateUserColor_s/<id>', methods=['PUT'])
def updateUserColor_s(id):

    color = request.json['color']

    cur = db.connection.cursor()
    cur.execute('UPDATE user SET color = %s WHERE id = %s', (color, id))
    db.connection.commit()

    return jsonify({'message': 'Usuario actualizado con exito!'})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')