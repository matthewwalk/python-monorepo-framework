from repo.cache.cache import cache
from repo.db.db import db
from flask import Flask
from flask_restful import Resource, Api, reqparse
from utils.utils import defaulter


# Initialize Flask
app = Flask(__name__)
api = Api(app)


class Message(Resource):

    def __init__(self) -> None:
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('msg', type = str, required=False, default="", location = 'json')
        self.reqparse.add_argument('id', type = str, required=False, default="", location = 'json')

        self.cache = cache()
        self.db = db()
        super(Message, self).__init__()

    def get(self):
        args = self.reqparse.parse_args()
        id = args['id']
        cached_msg = self.cache.client.get(name=id).decode()
        if cached_msg is not None:
            return {'msg' : cached_msg}
        return {'msg': f'no message found with id {id}'}


    def post(self):
        args = self.reqparse.parse_args()
        id = args['id']
        msg = args['msg']
        res = self.cache.client.set(name=id, value=msg)
        if res:
            return {'msg': f'key, value pair {id}, {msg} was set successfully'}
        return {'msg': f'key, value pair {id}, {msg} could not be set'}

api.add_resource(Message, '/message')


if __name__ == '__main__':
    app.run(debug=True, host= '0.0.0.0', port='8080')