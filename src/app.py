from flask import Flask
from flask import jsonify
from .controllers.node_api import node
from .controllers.edge_api import edge
from .analysis.nlp import NLP
from flask_cors import CORS
from .common.persitence.wrapper_factory import WrapperFactory
from nltk.corpus import brown
import re

# init db constraints
init_db = WrapperFactory.build_neo4j_init_wrapper('localhost', 7687, 'neo4j', 'test')
init_db.initialize_db()

# initialize the flask app
app = Flask(__name__)
CORS(app)

# register the blueprints from controllers
app.register_blueprint(node)
app.register_blueprint(edge)

#for sent in brown.sents():
#    NLP().find_useful_stuff(re.sub(r'[^\w]', ' ', ' '.join(sent)), False, True)

# setup default route
@app.route("/")
def hello():
    return "Hello World!"

# prototype junk
@app.route('/api/query/<text>')
def text_input(text):
    return jsonify(NLP().find_useful_stuff(text))

# prototype junk
@app.route('/api/query/--debug/<text>')
def text_input_debug(text):
    return jsonify(NLP().find_useful_stuff(text, True))

@app.route('/api/statement/<text>')
def text_statement(text):
    return jsonify(NLP().find_useful_stuff(text, False, True))

@app.route('/api/statement/--debug/<text>')
def text_statement_debug(text):
    return jsonify(NLP().find_useful_stuff(text, True, True))



# "main" function
if __name__ == "__main__":
    app.run()
