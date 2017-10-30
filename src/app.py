import sys
# required to load other directories modules
sys.path.insert(0, './services')

from flask import Flask, Blueprint
from .controllers.object_api import object

# initialize the flask app
app = Flask(__name__)

# register the blueprint
app.register_blueprint(object)

# setup default route
@app.route("/")
def hello():
    return "Hello World!"

# "main" function
if __name__ == "__main__":
    app.run()