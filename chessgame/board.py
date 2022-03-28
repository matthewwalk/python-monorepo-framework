class Piece(object):
    """
    Superclass for all chess piece objects
    x = x position on board
    y = y position on board
    colour = colour of piece
    active = true if on board, false otherwise
    moved = true if piece has been moved before (for pawn logic)
    """


    def __init__(self, x, y, colour=1) -> None:
        self.x = x
        self.y = y
        self.colour = colour
        self.active = True
        self.moved = False


    # to be overwritten
    def valid(self, x_p, y_p, taking=False):
        return True


    def move(self, x_p, y_p):
        self.moved = True
        self.x = x_p
        self.y = y_p
    

    def take(self):
        self.x = 0
        self.y = 0
        self.active = False


class King(Piece):


    def __init__(self, x, y, colour=1) -> None:
        self.type = 'K'
        super(King, self).__init__(x, y, colour)
    

    def valid(self, x_p, y_p, taking=False):
        x_delta = abs(x_p - self.x)
        y_delta = abs(y_p - self.y)
        return x_delta <= 1 and y_delta <= 1


class Queen(Piece):


    def __init__(self, x, y, colour=1) -> None:
        self.type = 'Q'
        super(Queen, self).__init__(x, y, colour)


    def valid(self, x_p, y_p, taking=False):
        x_delta = abs(x_p - self.x)
        y_delta = abs(y_p - self.y)
        return (x_delta == y_delta) or (x_delta == 0) or (y_delta == 0)

    
class Bishop(Piece):


    def __init__(self, x, y, colour=1) -> None:
        self.type = 'B'
        super(Bishop, self).__init__(x, y, colour)

    
    def valid(self, x_p, y_p, taking=False):
        x_delta = abs(x_p - self.x)
        y_delta = abs(y_p - self.y)
        return x_delta == y_delta


class Knight(Piece):

    def __init__(self, x, y, colour=1) -> None:
        self.type = 'K'
        super(Knight, self).__init__(x, y, colour)

    def valid(self, x_p, y_p, taking=False):
        x_delta = abs(x_p - self.x)
        y_delta = abs(y_p - self.y)
        return (x_delta == 2 and y_delta == 1) or (x_delta == 1 and y_delta == 2)


class Rook(Piece):

    def __init__(self, x, y, colour=1) -> None:
        self.type = 'R'
        super().__init__(x, y, colour)

    def valid(self, x_p, y_p, taking=False):
        x_delta = abs(x_p - self.x)
        y_delta = abs(y_p - self.y)
        return x_delta == 0 or y_delta == 0


class Pawn(Piece):
    def __init__(self, x, y, col=1):
        self.type = 'P'
        super(Pawn, self).__init__(x, y, col)

    def legal(self, x_p, y_p, taking=False):
        exp_dir = -2 * self.colour + 3 # white should be +1 while black should be -1

        x_delta = x_p - self.x
        y_delta = y_p - self.y

        # Might be better to have an or -> pawn can still only move one if they choose
        if (not taking) and (not self.moved) and (x_delta == 0) and (y_delta == 2 * exp_dir):
            return True
        elif taking:
            # diagonal
            if abs(x_delta) == 1 and (y_delta == exp_dir):
                return True
            else:
                return False
        else:
            return x_delta == 0 and (y_delta == exp_dir)

# TODO replace w/ dict

# Mappings -> for convention
A = 1
B = 2
C = 3
D = 4
E = 5
F = 6
G = 7
H = 8

# use as char array for valid rows
VALID_ROWS = '12345678'
VALID_COLS = 'ABCDEFGH'
PIECES = 'PRNBQK'


class Board():

    def __init__(self) -> None:
        self.white_pieces = {
            "wk" : King(E, 1),
            "wq" : Queen(D, 1),
            "wb1" : Bishop(C, 1),
            "wb2" : Bishop(F, 1),
            "wk1" : Knight(B, 1),
            "wk2" : Knight(G, 1),
            "wr1" : Rook(A, 1),
            "wr2" : Rook(H, 1),
            "wp1" : Pawn(A, 2),
            "wp2" : Pawn(B, 2),
            "wp3" : Pawn(C, 2),
            "wp4" : Pawn(D, 2),
            "wp5" : Pawn(E, 2),
            "wp6" : Pawn(F, 2),
            "wp7" : Pawn(G, 2),
            "wp8" : Pawn(H, 2)
        }
        
        self.black_pieces = {
            "bk" : King(E, 8, 2),
            "bq" : Queen(D, 8, 2),
            "bb1" : Bishop(C, 8, 2),
            "bb2" : Bishop(F, 8, 2),
            "bh1" : Knight(B, 8, 2),
            "bh2" : Knight(G, 8, 2),
            "br1" : Rook(A, 8, 2),
            "br2" : Rook(H, 8, 2),
            "bp1" : Pawn(A, 7, 2),
            "bp2" : Pawn(B, 7, 2),
            "bp3" : Pawn(C, 7, 2),
            "bp4" : Pawn(D, 7, 2),
            "bp5" : Pawn(E, 7, 2),
            "bp6" : Pawn(F, 7, 2),
            "bp7" : Pawn(G, 7, 2),
            "bp8" : Pawn(H, 7, 2)
        }
    


    def validate_input(self, input) -> bool:
        try:
            piece = input[0]
            col = input[1]
            row = input[2]
            if piece in PIECES and col in VALID_COLS and row in VALID_ROWS:
                return True
        except KeyError:
            return False

    
    # TODO implement
    def checkmate(self, turn) -> bool:
        pass

    
    def check_occ(self, move, turn) -> str:
        pos = self.get_pos(move)
        if turn % 2 == 1:
            for piece in self.black_pieces.values():
                if piece.x == pos[0] and piece.y == pos[1]:
                    return "take"
            for piece in self.white_pieces.values():
                if piece.x == pos[0] and piece.y == pos[1]:
                    return "blocked"
        else:
            for piece in self.black_pieces.values():
                if piece.x == pos[0] and piece.y == pos[1]:
                    return "blocked"
            for piece in self.white_pieces.values():
                if piece.x == pos[0] and piece.y == pos[1]:
                    return "take"
        return "empty"


    # TODO implement special moves -> swapping king and rook (I think?), etc.
    def validate_move(self, move, turn, taking):
        if turn % 2 == 1:
            pieces = self.white_pieces.values()
        else:
            pieces = self.black_pieces.values()
        valids = []
        pos = self.get_pos(move)
        p = move[0]
        # Get active pieces of type 
        potentials = [(index, piece) for index, piece in enumerate(pieces) if piece.type == p and piece.active]
        for _, piece in potentials: # Would include indicies w/ more time
            if piece.valid(pos[0], pos[1], taking): # probably should cast
                valids.append(piece)
        if len(valids) == 0:
            return False
        return True

    # todo - implement pawn to queen logic ?
    # todo PE4... example
    def move(self, move):
        return move

    # =========== helper functions =================

    def get_pos(self, move):
        return [VALID_COLS.index(move[1])+1, int(move[2])]

    def get_space(self, x, y):
        space = ''
        space += VALID_COLS[x-1]
        space += str(y)
        return space
    
    def check_space(self, x, y, type, turn):
        space = self.get_space(int(x), int(y))
        move = type + space
        status = self.check_occ(move, turn)
        if status != 'empty':
            return True
        return False