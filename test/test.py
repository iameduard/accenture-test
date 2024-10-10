import unittest
import json
from app import app

class FlaskAppTest(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		app.config['TESTING'] = True
		cls.client = app.test_client()
	def test_pelicula_popular(self):
		response = self.client.get('/peliculas/popular')
		self.assertEqual(response.status_code, 200)
		self.assertIn('application/json', response.content_type)
	def test_pelicula_estrellas(self):
		data = {"movie_id":1125510,"value": 4.5}
		response = self.client.post('/peliculas/estrellas',data=json.dumps(data),content_type='application/json')
		self.assertEqual(response.status_code, 200)
	def test_peliculas_estrellas_listar(self):
		response = self.client.get('/peliculas/estrellas/list')
		self.assertEqual(response.status_code, 200)
