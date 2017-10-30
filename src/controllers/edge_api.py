from flask import Blueprint, request, jsonify

edge = Blueprint('edge', __name__, url_prefix='/edges')

@edge.route("/", methods=['GET', 'POST'])
def getEdges():
	if request.method == 'POST':
		return 'posted'
	elif request.method == 'GET':
		return jsonify([])

@edge.route("/<edge_id>", methods=['GET', 'PUT', 'DELETE'])
def getEdge(edge_id):
	return edge_id