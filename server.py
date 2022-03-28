from operator import truediv
from chessgame.board import Board
from repo.cache.cache import cache
from repo.db.db import db
from flask import Flask
from flask_restful import Resource, Api, reqparse
from utils.utils import defaulter
from chessgame.board import Board

import chess


# Initialize Flask
app = Flask(__name__)
api = Api(app)


class Message(Resource):
    def __init__(self) -> None:
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('msg', type = str, required=False, default="", location = 'json')
        self.reqparse.add_argument('id', type = str, required=True, help="Missing id", location = 'json')

        self.cache = cache()
        self.db = db()
        super(Message, self).__init__()


    def get(self):
        args = self.reqparse.parse_args()
        id = args['id']
        cached_msg = bytes(self.cache.client.get(name=id)).decode()
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


class ChessTwo(Resource):
    def __init__(self) -> None:
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('move', type = str, default="", location='json')

        self.board = chess.Board()

        super(ChessTwo, self).__init__()


    def get(self):
        print(self.board, flush=True)
        return {'board' : self.board.__str__()}


    def post(self):
        args = self.reqparse.parse_args()
        move = args['move']

        Nf3 = chess.Move.from_uci(move)
        self.board.push(Nf3)
        print(self.board, flush=True)

        if self.board.is_stalemate():
            return {'condition' : "board is in stalemate!"}

        if self.board.is_checkmate():
            return {'condition' : "board is in checkmate!"}

        return {'board' : self.board.__str__()}



class Chess(Resource):
    def __init__(self) -> None:
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('move', type = str, required=True, help='Missing move', location='json')

        self.board = Board()
        self.turn = 1
        self.last_move = []

        super(Chess, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()
        move = args['move']

        # Validate Input
        valid_input = self.board.validate_input(input=move)
        if not valid_input:
            return {'error' : "Invalid input, try again"}

        # Check if space is occupied
        occ = self.board.check_occ(move, self.turn)
        if occ == 'blocked':
            return {'error' : "Space occupied by same colour, try again"}
        taking = occ == 'take'

        # Check if move is valid
        valid = self.board.validate_move(move, self.turn, taking)
        if not valid:
            return {'error' : "Invalid move, try again"}

        curr_move = self.board.move(move=move)

        output = "White Pieces: "
        for key, piece in self.board.white_pieces.items():
            output += f'{key} : {piece.x}, {piece.y} '

        output += "Black Pieces: "
        for key, piece in self.board.black_pieces.items():
            output += f'{key} : {piece.x}, {piece.y} '

        return {'msg' : output}




api.add_resource(Chess, '/chess')
api.add_resource(ChessTwo, '/chesstwo')

if __name__ == '__main__':
    config = {
        "debug" : True,
        "host" : defaulter("HOST", "0.0.0.0"),
        "port" : defaulter("PORT", "8080")
    }
    app.run(**config)