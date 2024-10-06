#pytest
import unittest
from app import app, db
from models import User, Product, Cart, CartProduct
import json


class FlaskAppTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Configurar la aplicación para testing
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqllite://memory'
        cls.client = app.test_client()
        with app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        # Se limpia la base de datos al terminar los test
        with app.app_context():
            db.drop_all()

    def test_user_creation(self):
        response = self.client.post('/register',data=json.dumps({
        'username': 'testuser123',
        'password': 'password'
        }), content_type='application/json')

        self.asserEqual(response.status_code, 201)
        self.assertIn('User created successfully', response.get_data(as_text=True))

    def test_login_and_token(self):
        self.client.post('/register',data=json.dumps({
        'username':'testuser123',
        'password':'password'
        }), content_type='application/json')

        response=self.client.post('/login',data=json.dumps({
        'username':'testuser123',
        'password':'password'
        }),content_type='application/json')

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertIn('access_token',data)
        self.token = data['access_token']

	def test_create_product(self):
        self.test_login_and_token()
        response = self.client.post('/login', data=json.dumps({
        'username': 'testuser123',
        'password': 'password'
    	}), content_type='application/json')
        data = json.loads(response.get_data(as_text=True))
        token = data['access_token']
        response = self.client.post('/products',headers={
								'Authorization':f'Bearer {self.token}'
								},data=json.dumps({
								'name':'zapatillas',
								'price':20.0
								}),content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('zapatillas',response.get_data(as_text=True))


if __name__=='__main__':
	unittest.main()


