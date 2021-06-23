#!/usr/bin/python3
""" running flask """
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def teardown(error):
    """ calling close"""
    storage.close()


@app.errorhandler(404)
def error_handler(error):
    """ 404 error page redirection """
    return jsonify({"error": "Not found"}), 404

if __name__ == '__main__':
    app.run(host=getenv('HBNB_API_HOST', '0.0.0.0'),
            port=getenv('HBNB_API_PORT', '5000'), threaded=True, debug=True)
