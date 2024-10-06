from marshmallow import Schema, fields, validate

class UserSchema(Schema):
	id = fields.Int(dump_only=True)
	username = fields.Str(required=True, validate=validate.Length(min=1))
	password = fields.Str(required=True, validate=validate.Length(min=5))

class ProductSchema(Schema):
	id = fields.Int(dump_only=True)
	name = fields.Str(required=True, validate=validate.Length(min=1))
	price = fields.Float(required=True)

class CartProductSchema(Schema):
	product_id = fields.Int(required=True)
	quantity = fields.Int(required=True, validate=validate.Range(min=1))

class CartSchema(Schema):
	id = fields.Int(dump_only=True)
	user_id = fields.Int(required=True)
	products = fields.List(fields.Nested(CartProductSchema),required=True)

