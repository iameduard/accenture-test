from flask import Flask, jsonify, request

app = Flask(__name__)

#Ruta de bienvenida
@app.route('/')
def home():
	return "Bienvenidos a la API con Flask"

@app.route('/api/v1/data',methods=['GET'])
def get_data():
	data={
	"nombre":"Juan",
	"edad":30,
	"ocupacion":"Ingeniero"
	}
	return jsonify(data)

@app.route('/api/v1/data',methods=['POST'])
def create_data():
	new_data = request.get_json()
	response = {
		"message":"Datos recibidos",
		"data":new_data
	}
	return jsonify(response), 201

if __name__ == '__main__':
	app.run(debug=True)