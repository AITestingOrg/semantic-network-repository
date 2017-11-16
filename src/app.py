from flask import Flask
from flask import jsonify
from .controllers.node_api import node
from .controllers.edge_api import edge
from .analysis.nlp import NLP
import urllib


# initialize the flask app
app = Flask(__name__)

# register the blueprints from controllers
app.register_blueprint(node)
app.register_blueprint(edge)


# setup default route
@app.route("/")
def hello():
    return "Hello World!"

# prototype junk
@app.route('/api/query/<text>')
def text_input(text):
    text = urllib.parse.unquote(text)
    return jsonify(NLP().find_useful_stuff(text))



# "main" function
if __name__ == "__main__":
    app.run()
