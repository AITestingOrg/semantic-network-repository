from flask import Blueprint

object = Blueprint('object', __name__, url_prefix='/object')

@object.route("/<object_id>")
def getObject(object_id):
	return object_id