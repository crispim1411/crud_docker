#!/usr/bin/env python3
from flask import Flask, request
from flask_httpauth import HTTPBasicAuth
from flask_cors import CORS
from pymongo import MongoClient
import os

app = Flask(__name__)
CORS(app)

URI = os.environ.get('DB')
client = MongoClient(URI)
db = client.test_database
collection = db.test_collection

@app.route('/cadastrar',methods=['POST'])
def addUser():
	try:
		doc = request.json
		if 'username' not in doc:
			return 'Missing arguments',400

		username = doc['username']
		user = collection.find({'username':username})
		if user is None:
			return 'message: User already exists',200
		
		new = dict(doc)
		collection.insert_one(new)

		return f'message: User created: {username}',201
	
	except Exception as e:
		return f'Erro:{e}',400


@app.route('/mostrar',methods=['GET'])
def getUsers():
	try:
		query = collection.find({},{'_id':False})
		users = [user for user in query]
		str_users = f'{users}'.replace("'",'"')
		return str_users, 200

	except Exception as e:
		return f'Erro:{e}',400


@app.route('/mostrar/<username>',methods=['GET'])
def getUserByName(username):
	try:
		if username is None:
			return 'Missing arguments',400

		user = collection.find_one({'username':username},{'_id':False})
		if user is None:
			return 'message: User not found',404

		return f"{user}",200
	except Exception as e:
		return f'Erro:{e}',400


@app.route('/modificar',methods=['POST'])
def updateInfo():
	try:
		doc = request.json
		if 'username' not in doc:
			return 'Missing arguments',400

		username = doc['username']
		collection.update_one({'username':username},{'$set':doc})
		return f'User info update successfully',200
	
	except Exception as e:
		return f'Erro:{e}',400


@app.route('/deletar',methods=['POST'])
def delUSer(username):
	try:
		doc = request.json
		if 'username' not in doc:
			return 'Missing arguments',400

		username = doc['username']
		user = collection.find({'username':username})
		if user is None:
			return 'message: User not found',404

		collection.delete_one({'username':username})
		return f'message: User {username} deleted',200

	except Exception as e:
		return f'Erro:{e}',400


if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0',port=8081)
