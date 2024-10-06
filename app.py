from flask import Flask
from models import db
from resources.user import UserRegister, UserList
from resources.product import ProductList, ProductCreate
from resources.cart import CartView, CartCreate
from auth import configure_auth

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
jwt = configure_auth(app)


with app.app_context():
	db.create_all()

#Registrat rutas de usuarios
app.add_url_rule('/register',view_func=UserRegister.as_view('user_register')) #vistas basadas en clases
app.add_url_rule('/users',view_func=UserList.as_view('user_list'))

#Registrar rutas de productos
app.add_url_rule('/create_product',view_func=ProductCreate.as_view('create_product'))
app.add_url_rule('/products',view_func=ProductList.as_view('product_list'))

#Registrar ruta de carrito
app.add_url_rule('/create_cart',view_func=CartCreate.as_view('create_cart'))
app.add_url_rule('/carts',view_func=CartView.as_view('cart_list'))

if __name__ == '__main__':
	app.run(debug=True)