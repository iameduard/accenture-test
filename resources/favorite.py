from flask import request, jsonify
from flask import current_app as app
from flask .views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from resources.movie import MovieList, MovieRating, MovieRatedList, MovieRateConsult
from services.exception_manage import exception_manage
import pandas as pd
import requests
import json


account_id = '21558553'
session_id = '9dcbc75cda55966c14124c8cb92d1280f97ca806'
api_key = '34c9cc2f7d698b29c351a955278150f9'
token = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzNGM5Y2MyZjdkNjk4YjI5YzM1MWE5NTUyNzgxNTBmOSIsIm5iZiI6MTcyODQ5NzI1NC4xNTA0NTgsInN1YiI6IjY3MDNmMzI5YjZmNTg3ZWRlODEzYTJhOSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.cuqEPlTQFjc8JgQ8TKIoV4BFAW-x14KnFLlXmfDdEg0'


class FavoriteList(MethodView):
	@jwt_required()
	@exception_manage
	def get(self):
		url = f"https://api.themoviedb.org/3/account/{account_id}/favorite/movies?session_id={session_id}&api_key={api_key}"

		payload = ""
		headers = {
		  'Authorization':  f"Bearer {token}"
		}
		response = requests.request("GET", url, headers=headers, data=payload)
		return response.json()


class FavoriteAdd(MethodView):
	@jwt_required()
	@exception_manage
	def post(self):
		data = request.get_json()
		media_id = data['media_id']
		url = F"https://api.themoviedb.org/3/account/{account_id}/favorite?session_id={session_id}"
		payload = json.dumps({
		  "media_type": "movie",
		  "media_id": media_id,
		  "favorite": True
		})
		headers = {
		  'Content-Type': 'application/json',
		  'Authorization': f"Bearer {token}"
		}
		response = requests.request("POST", url, headers=headers, data=payload)
		return response.json()


class FavoriteDelete(MethodView):
	@jwt_required()
	@exception_manage
	def post(self):
		data = request.get_json()
		media_id = data['media_id']
		url = f"https://api.themoviedb.org/3/account/{account_id}/favorite?session_id={session_id}"
		payload = json.dumps({
		  "media_type": "movie",
		  "media_id": media_id,
		  "favorite": False
		})
		headers = {
		  'Content-Type': 'application/json',
		  'Authorization': f"Bearer {token}"
		}
		response = requests.request("POST", url, headers=headers, data=payload)
		return response.json()

class FavoriteClear(MethodView):
	@jwt_required()
	@exception_manage
	def post(self):
		
		favorite_list_view = FavoriteList.as_view('favoritos_listar')
		with app.test_request_context('/favoritos/listar', method='GET'):
			favorite_list_response = favorite_list_view()

		print(favorite_list_response)
		
		favoritos = favorite_list_response.get('results', [])

		print(favoritos)
		
		if not favoritos:
			return jsonify({"message": "No existen favoritos"}), 200

		favorite_delete_view = FavoriteDelete.as_view('favoritos_eliminar')

		for movie in favoritos:
			movie_id = movie['id']
			print(movie_id)
			
			with app.test_request_context('/favoritos/eliminar', method='POST', json={'media_id': movie_id}):
				delete_response = favorite_delete_view()

			if 'error' in delete_response:
				return jsonify({'error': f'No pudo eliminar el favorito movie_id: {movie_id}'})

		return jsonify({"message": "Se eliminaron todos los favoritos"}), 200


class FavoriteConsult(MethodView):
	@jwt_required()
	@exception_manage
	def get(self):
		
		favorite_list_view = FavoriteList.as_view('favoritos_listar')
		with app.test_request_context('/favoritos/listar', method='GET'):
			favorite_list_response = favorite_list_view()
		
		favoritos = favorite_list_response.get('results', [])
		
		if not favoritos:
			return jsonify({"message": "No existen favoritos"}), 200

		favorite_delete_view = FavoriteDelete.as_view('favoritos_eliminar')

		favoritos_info = list()

		for movie in favoritos:
			movie_id = movie['id']
			title = movie['title']
			overview = movie['overview']
			adult = movie['adult']
			release_date = movie['release_date']

			pelicula_estrellas_view = MovieRateConsult.as_view('pelicula_estrellas')


			with app.test_request_context('/peliculas/estrellas', method='GET', json={'movie_id': movie_id}):
				estrellas_response = pelicula_estrellas_view()

			print("estrellas_response:",estrellas_response)

			estrellas_dic = estrellas_response.get('rated', [])
			estrellas = estrellas_dic.get('value', [])

			print(estrellas)

			favoritos_info.append({'movie_id':movie_id,
								   'title':title,
								   'overview':overview, 
								   'adult':adult, 
								   'release_date':release_date,
								   'estrellas':estrellas})

		df = pd.DataFrame(favoritos_info)
		df['release_date'] = pd.to_datetime(df['release_date'])
		df_sorted = df.sort_values(by=['release_date','estrellas'],ascending=True)
		print(df_sorted)

		return jsonify(df_sorted.to_dict(orient='records')), 200