from flask import Blueprint, request, jsonify

object = Blueprint('object', __name__, url_prefix='/objects')

@object.route("/", methods=['GET', 'POST'])
def getObjects():
	if request.method == 'POST':
		return 'posted'
	elif request.method == 'GET':
		return jsonify([])

@object.route("/<object_id>", methods=['GET', 'PUT', 'DELETE'])
def getObject(object_id):
	return object_id