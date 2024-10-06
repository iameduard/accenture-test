from flask import Flask
from models import db
from resources.user import UserRegister, UserList
from auth import configure_auth

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
jwt = configure_auth(app)


with app.app_context():
	db.create_all()

app.add_url_rule('/register',view_func=UserRegister.as_view('user_register')) #vistas basadas en clases
app.add_url_rule('/users',view_func=UserList.as_view('user_list'))

if __name__ == '__main__':
	app.run(debug=True)