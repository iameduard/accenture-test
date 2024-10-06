# models.py

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True, nullable=False)
	password = db.Column(db.String(120), nullable=False)


	def to_dict(self):
		return {"id":self.id, "username": self.username}

class Product(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(120), nullable=False)
	price = db.Column(db.Float, nullable=False)

	def to_dict(self):
		return {"id": self.id, "name": self.name, "price": self.price}

class Cart(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeingKey('user.id'), nullable=False)
	user = db.relationship('User',backref=db.backref('cart',lazy=True))
	products = db.relationship('CartProduct',back_populates='cart')

	def to_dict(self):
		return {
			"id": self.id,
			"user_id": self.user_id,
			"products": [cart_product.to_dict() for cart_product in self.products]
		}

class CartProduct(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	cart_id = db.Column(db.Integer, db.ForeingKey('cart.id'),nullable=False)
	product_id = db.Column(db.Integer, db.ForeingKey('product.id'),nullable=False)
	quantity = db.Column(db.Integer, nullable=False)
	cart = db.relationship('Cart',back_populates='products')
	product = db.relationship('Product')

	def to_dict(self):
		return {
			"product_id":self.product_id,
			"name":self.product.name,
			"price":self.product.price,
			"quantity":self.quantity
		}