from flask import Flask
from models import db
from auth import configure_auth
from resources.movie import MovieList, MovieRating, MovieRatedList, MovieRateConsult
from resources.favorite import FavoriteList, FavoriteAdd, FavoriteDelete, FavoriteClear, FavoriteConsult
from resources.user import UserRegister, UserList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
jwt = configure_auth(app)


#Registrat rutas de usuarios
app.add_url_rule('/register',view_func=UserRegister.as_view('user_register')) #vistas basadas en clases
app.add_url_rule('/users',view_func=UserList.as_view('user_list'))


#Movie endpoints
app.add_url_rule('/peliculas/popular',view_func=MovieList.as_view('peliculas_popular'))
app.add_url_rule('/peliculas/estrellas',view_func=MovieRating.as_view('peliculas_estrellas'))
app.add_url_rule('/peliculas/estrellas/list',view_func=MovieRatedList.as_view('peliculas_estrellas_listar'))
app.add_url_rule('/pelicula/estrellas',view_func=MovieRateConsult.as_view('pelicula_estrellas'))

#Favorite endpoints
app.add_url_rule('/favoritos/listar',view_func=FavoriteList.as_view('favoritos_listar'))
app.add_url_rule('/favoritos/agregar',view_func=FavoriteAdd.as_view('favoritos_agregar'))
app.add_url_rule('/favoritos/eliminar',view_func=FavoriteDelete.as_view('favoritos_eliminar'))
app.add_url_rule('/favorites/limpiar', view_func=FavoriteClear.as_view('favoritos_limpiar'))
app.add_url_rule('/favorites/consultar', view_func=FavoriteConsult.as_view('favoritos_consultar'))



if __name__ == '__main__':
	app.run(debug=True)