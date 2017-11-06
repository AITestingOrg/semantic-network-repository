from flask import Blueprint, request
from .api import Api

edge = Blueprint('edge', __name__, url_prefix='/edges')


@edge.route("/", methods=['GET', 'POST'])
def get_edges():
    if request.method == 'POST':
        return 'posted'
    elif request.method == 'GET':
        return Api.respond([], True)


@edge.route("/<edge_id>", methods=['GET', 'PUT', 'DELETE'])
def get_edge(edge_id):
    return Api.respond({}, True)
