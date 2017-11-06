from flask import Flask
from .controllers.node_api import node
from .controllers.edge_api import edge

def create_app(config=None, environment=None):
    app = Flask(__name__)
    app.config['ENVIRONMENT'] = environment
    app.config.update(config or {})

    app.register_blueprint(node)
    app.register_blueprint(edge)

    return app