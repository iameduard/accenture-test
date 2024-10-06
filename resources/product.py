from flask import request, jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from models import db, Product
from schemas import ProductSchema

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


class ProductList(MethodView):
	print('listar productos')
	@jwt_required()
	def get(self):
		products = Product.query.all()
		return jsonify(products_schema.dump(products))

class ProductCreate(MethodView):
	print('crear product')
	@jwt_required()
	def post(self):
		data = request.get_json()
		errors = product_schema.validate(data)
		if errors:
			return jsonify(errors), 400

		new_product = Product(**data)
		db.session.add(new_product)
		db.session.commit()

		# dump para convertir el objeto a JSON serializable

		product_data = product_schema.dump(new_product)
		return jsonify(product_data), 201