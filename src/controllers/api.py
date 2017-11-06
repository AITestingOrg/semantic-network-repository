from flask import jsonify

class Api:
    @staticmethod
    def respond(payload, success):
        return jsonify({ 'payload': payload, 'success': success })