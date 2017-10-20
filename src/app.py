import sys
# required to load other directories modules
sys.path.insert(0, './network')

from flask import Flask, Blueprint

# load a controller blueprint
object_api = Blueprint('object_api', __name__, template_folder='network')

# initialize the flask app
app = Flask(__name__)

# register the blueprint
app.register_blueprint(object_api)

# setup default route
@app.route("/")
def hello():
    return "Hello World!"

# "main" function
if __name__ == "__main__":
    app.run()