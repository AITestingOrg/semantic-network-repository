from flask import Flask
from .controllers.object_api import object
from .controllers.edge_api import edge

# initialize the flask app
app = Flask(__name__)

# register the blueprints from controllers
app.register_blueprint(object)
app.register_blueprint(edge)

# setup default route
@app.route("/")
def hello():
    return "Hello World!"

# "main" function
if __name__ == "__main__":
    app.run()