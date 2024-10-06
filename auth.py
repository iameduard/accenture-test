# auth.py

from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, JWTManager
from models import db, User
from dotenv import load_dotenv
from datetime  import timedelta
import os

load_dotenv()


def configure_auth(app):

	jwt_secret_key = os.getenv('JWT_SECRET_KEY')

	app.config['JWT_SECRET_KEY'] = jwt_secret_key 
	app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
	print(jwt_secret_key )

	jwt = JWTManager(app)

	@app.route('/login',methods=['POST'])
	def login():
		data = request.get_json()
		user = User.query.filter_by(username=data['username']).first()

		if user and user.password == data['password']:
			access_token = create_access_token(identity=user.username)
			return jsonify(access_token=access_token)
		else:
			return jsonify({"message":"Invalid credentias"}), 401

	return jwt

