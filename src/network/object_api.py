from flask import Blueprint

object_api = Blueprint('object_api', __name__)

@object_api.route("/object")
def getObject():
	return 'Object'