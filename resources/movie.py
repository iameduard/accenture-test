from flask import request, jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from services.exception_manage import exception_manage
from models import db
import requests
import json

account_id = '21558553'
session_id = '9dcbc75cda55966c14124c8cb92d1280f97ca806'
API_KEY = 'b05b2952674ff7e2b60023bf82b45ff5'
token = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzNGM5Y2MyZjdkNjk4YjI5YzM1MWE5NTUyNzgxNTBmOSIsIm5iZiI6MTcyODUwOTgyOC45MTg5NzksInN1YiI6IjY3MDNmMzI5YjZmNTg3ZWRlODEzYTJhOSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.9yy9_Sw3pvABYubtzL93-BZe9Lc1dhDwYQ2fA6DJ7SU'

class MovieList(MethodView):
	@jwt_required()
	@exception_manage
	def get(self):
		url = f"https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}"
		headers = {
		    "accept": "application/json",
		    "Authorization": f"Bearer {token}"
		}
		response = requests.get(url, headers=headers)
		return response.json()


class MovieRating(MethodView):
	@jwt_required()
	@exception_manage
	def post(self):
		data = request.get_json()
		movie_id=data['movie_id']
		value=data['value']
		print(movie_id)
		print(value)
		url = f"https://api.themoviedb.org/3/movie/{movie_id}/rating"
		payload = json.dumps({
		  "value": value
		})
		headers = {
		  'Content-Type': 'application/json',
		  'Authorization': f"Bearer {token}"
		}
		response = requests.request("POST", url, headers=headers, data=payload)
		return response.json()

class MovieRatedList(MethodView):
	@jwt_required()
	@exception_manage
	def get(self):
		url = f"https://api.themoviedb.org/3/account/{account_id}/rated/movies?api_key={API_KEY}&session_id={session_id}"
		payload = ""
		headers = {
		  'Content-Type': 'application/json',
		  'Authorization': f"Bearer {token}"
		}
		response = requests.request("GET", url, headers=headers, data=payload)
		return response.json()


class MovieRateConsult(MethodView):
	@jwt_required()
	@exception_manage
	def get(self):
		data = request.get_json()
		movie_id=data['movie_id']
		url = f"https://api.themoviedb.org/3/movie/{movie_id}/account_states?api_key={API_KEY}&session_id={session_id}"
		payload = ""
		headers = {
		  'Content-Type': 'application/json',
		  'Authorization': f"Bearer {token}"
		}
		response = requests.request("GET", url, headers=headers, data=payload)
		return response.json()
