#resources/user.py

from flask import request, jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from models import db, User

class UserRegister(MethodView):

	def post(self):
		data = request.get_json()
		new_user = User(username=data['username'], password=data['password'])
		db.session.add(new_user)
		db.session.commit()
		return jsonify({"message":"User created successfully"}), 201

class UserList(MethodView):
	@jwt_required()
	def get(self):
		users = User.query.all()
		return jsonify([user.to_dict() for user in users])