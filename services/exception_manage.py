import functools
import requests
from flask import jsonify, request


def exception_manage(func):
	@functools.wraps(func)
	def wrapper_exception_manage(*args, **kwargs):
		try:
			return func(*args, **kwargs)
		except IOError as io_error:
			return jsonify({
				"error":"No se pudo recuperar la informacion de TMDB."
				}), 500

	return wrapper_exception_manage