#!/usr/bin/env python3
from flask import Flask, Blueprint, request
from flask_httpauth import HTTPBasicAuth
from pymongo import MongoClient
import os

app = Flask(__name__)

URI = os.environ.get('DB')
client = MongoClient(URI)
db = client.test_database
collection = db.test_collection

#TODO: argumentos passados pelo request body

@app.route('/cadastrar/<username>',methods=['POST'])
def addUser(username):
	try:
		if username is None:
			return 'Missing arguments',400

		user = collection.find({'username':username})
		if user is None:
			return 'message: User already exists',200
		
		new = dict(username = username)
		collection.insert_one(new)

		return f'message: User created: {username}',201
	
	except Exception as e:
		return f'Erro:{e}',400


@app.route('/mostrar',methods=['GET'])
def getUsers():
	try:
		query = collection.find()
		users = [user for user in query]
		return f'users: {users}',200

	except Exception as e:
		return f'Erro:{e}',400


@app.route('/mostrar/<username>',methods=['GET'])
def getUserByName(username):
	try:
		if username is None:
			return 'Missing arguments',400

		user = collection.find_one({'username':username})
		if user is None:
			return 'message: User not found',404

		return f"User: {user['username']}",200
	except Exception as e:
		return f'Erro:{e}',400


@app.route('/modificar/<username>/<info>',methods=['POST'])
def updateInfo(username,info):
	try:
		if username is None or info is None:
			return 'Missing arguments',400

		collection.update_one({'username':username},{'$set':{'username':info}})
		return f'User info update successfully',200
	
	except Exception as e:
		return f'Erro:{e}',400


@app.route('/deletar/<username>',methods=['POST'])
def delUSer(username):
	try:
		if username is None:
			return 'Missing arguments',400

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
