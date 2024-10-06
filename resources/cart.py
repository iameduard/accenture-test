from flask import request, jsonify
from flask .views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Cart, CartProduct, Product, User
from schemas import CartSchema

cart_schema = CartSchema()


class CartView(MethodView):
	@jwt_required()
	def get(self):
		user_id = get_jwt_identity()
		print('user:',user_id)
		cart = Cart.query.filter_by(user_id=user_id).first()
		if not cart:
			return jsonify({"message":"Cart not found"}), 404

		return jsonify(cart_schema.dump(cart))

class CartCreate(MethodView):
	@jwt_required()
	def post(self):
		user_id = get_jwt_identity()
		data = request.get_json()
		errors = cart_schema.validate(data)
		if errors:
			return jsonify(errors), 400


		cart = Cart.query.filter_by(user_id=user_id).first()

		
		
		if not cart:
			cart = Cart(user_id=user_id)
			db.session.add(cart)
			db.session.commit()

		print(cart.to_dict())

		for item in data['products']:
			product = Product.query.get(item['product_id'])
			if not product:
				return jsonify({"messsage":f"Product with id {item['product_id']} not found"}), 400

			cart_product = CartProduct.query.filter_by(cart_id=cart.id, product_id=product.id).first()
			if cart_product:
				cart_product.quantity += item['quantity']
			else:
				cart_product = CartProduct(cart_id=cart.id,product_id=product.id, quantity=item['quantity'])
				db.session.add(cart_product)

		db.session.commit()

		return jsonify(cart_schema.dump(cart)), 201
