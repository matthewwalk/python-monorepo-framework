from repo.cache.cache import cache
from repo.db.db import db
from flask import Flask
from flask_restful import Resource, Api
from utils.utils import defaulter


# Initialize Flask
app = Flask(__name__)
api = Api(app)


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


api.add_resource(HelloWorld, '/')


if __name__ == '__main__':
    app.run(debug=True, host= '0.0.0.0', port='8080')