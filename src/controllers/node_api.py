from flask import Blueprint, request, jsonify

node = Blueprint('node', __name__, url_prefix='/nodes')


@node.route("/", methods=['GET', 'POST'])
def get_nodes():
    if request.method == 'POST':
        return 'posted'
    elif request.method == 'GET':
        return jsonify([])


@node.route("/<node_id>", methods=['GET', 'PUT', 'DELETE'])
def get_node(node_id):
    return node_id
