from flask import Flask
from flask_restful import Api
from resources import HealthCheck, ML
from model_handler import Model


def create_app():
    app = Flask(__name__)
    app.model_handler = Model('./model_dir')
    api = Api(app)
    api.add_resource(HealthCheck, '/health')
    api.add_resource(ML, '/')
    return app


# app = create_app()
# app.run(host='0.0.0.0',port=5555)
