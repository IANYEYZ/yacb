import chess

mvvLva = {
    chess.KING: {
        chess.KING: 0,
        chess.QUEEN: 0,
        chess.ROOK: 0,
        chess.BISHOP: 0,
        chess.KNIGHT: 0,
        chess.PAWN: 0
    },
    chess.QUEEN: {
        chess.KING: 50,
        chess.QUEEN: 51,
        chess.ROOK: 52,
        chess.BISHOP: 53,
        chess.KNIGHT: 54,
        chess.PAWN: 55
    },
    chess.ROOK: {
        chess.KING: 40,
        chess.QUEEN: 41,
        chess.ROOK: 42,
        chess.BISHOP: 43,
        chess.KNIGHT: 44,
        chess.PAWN: 45
    },
    chess.BISHOP: {
        chess.KING: 30,
        chess.QUEEN: 31,
        chess.ROOK: 32,
        chess.BISHOP: 33,
        chess.KNIGHT: 34,
        chess.PAWN: 35
    },
    chess.KNIGHT: {
        chess.KING: 20,
        chess.QUEEN: 21,
        chess.ROOK: 22,
        chess.BISHOP: 23,
        chess.KNIGHT: 24,
        chess.PAWN: 25
    },
    chess.PAWN: {
        chess.KING: 10,
        chess.QUEEN: 11,
        chess.ROOK: 12,
        chess.BISHOP: 13,
        chess.KNIGHT: 14,
        chess.PAWN: 15
    }
}

def moveScore(board: chess.Board, move: chess.Move):
    score = 0
    if board.is_capture(move):
        fr = board.piece_at(move.from_square)
        to = board.piece_at(move.to_square)
        if to == None and board.is_en_passant(move):
            to = chess.Piece(chess.PAWN, chess.WHITE)
        score += mvvLva[fr.piece_type][to.piece_type]
    if move.promotion != None:
        score += 50
    if board.gives_check(move):
        score += 10
    return score

class YACB:
    def __init__(self, color = chess.WHITE, board = chess.Board()):
        self.board = board
        self.values = {
            chess.PAWN: 100,
            chess.KNIGHT: 320,
            chess.BISHOP: 330,
            chess.ROOK: 500,
            chess.QUEEN: 900,
            chess.KING: 20000
        }
        self.positionalValue = {
            chess.PAWN: [
                [  0,   0,   0,   0,   0,   0,   0,   0],
                [  5,  10,  10, -20, -20,  10,  10,   5],
                [  5,  -5, -10,   0,   0, -10,  -5,   5],
                [  0,   0,   0,  20,  20,   0,   0,   0],
                [  5,   5,  10,  25,  25,  10,   5,   5],
                [ 10,  10,  20,  30,  30,  20,  10,  10],
                [ 50,  50,  50,  50,  50,  50,  50,  50],
                [  0,   0,   0,   0,   0,   0,   0,   0],
            ],

            chess.KNIGHT: [
                [-50, -40, -30, -30, -30, -30, -40, -50],
                [-40, -20,   0,   5,   5,   0, -20, -40],
                [-30,   5,  10,  15,  15,  10,   5, -30],
                [-30,   0,  15,  20,  20,  15,   0, -30],
                [-30,   5,  15,  20,  20,  15,   5, -30],
                [-30,   0,  10,  15,  15,  10,   0, -30],
                [-40, -20,   0,   0,   0,   0, -20, -40],
                [-50, -40, -30, -30, -30, -30, -40, -50],
            ],

            chess.BISHOP: [
                [-20, -10, -10, -10, -10, -10, -10, -20],
                [-10,   5,   0,   0,   0,   0,   5, -10],
                [-10,  10,  10,  10,  10,  10,  10, -10],
                [-10,   0,  10,  10,  10,  10,   0, -10],
                [-10,   5,   5,  10,  10,   5,   5, -10],
                [-10,   0,   5,  10,  10,   5,   0, -10],
                [-10,   0,   0,   0,   0,   0,   0, -10],
                [-20, -10, -10, -10, -10, -10, -10, -20],
            ],

            chess.ROOK: [
                [  0,   0,   5,  10,  10,   5,   0,   0],
                [ -5,   0,   0,   0,   0,   0,   0,  -5],
                [ -5,   0,   0,   0,   0,   0,   0,  -5],
                [ -5,   0,   0,   0,   0,   0,   0,  -5],
                [ -5,   0,   0,   0,   0,   0,   0,  -5],
                [ -5,   0,   0,   0,   0,   0,   0,  -5],
                [  5,  10,  10,  10,  10,  10,  10,   5],
                [  0,   0,   0,   5,   5,   0,   0,   0],
            ],

            chess.QUEEN: [
                [-20, -10, -10,  -5,  -5, -10, -10, -20],
                [-10,   0,   5,   0,   0,   0,   0, -10],
                [-10,   5,   5,   5,   5,   5,   0, -10],
                [  0,   0,   5,   5,   5,   5,   0,  -5],
                [ -5,   0,   5,   5,   5,   5,   0,  -5],
                [-10,   0,   5,   5,   5,   5,   0, -10],
                [-10,   0,   0,   0,   0,   0,   0, -10],
                [-20, -10, -10,  -5,  -5, -10, -10, -20],
            ],

            # Middlegame king table.
            # This deliberately encourages castling and discourages
            # walking toward the centre.
            chess.KING: [
                [ 20,  30,  10,   0,   0,  10,  30,  20],
                [ 20,  20,   0,   0,   0,   0,  20,  20],
                [-10, -20, -20, -20, -20, -20, -20, -10],
                [-20, -30, -30, -40, -40, -30, -30, -20],
                [-30, -40, -40, -50, -50, -40, -40, -30],
                [-30, -40, -40, -50, -50, -40, -40, -30],
                [-30, -40, -40, -50, -50, -40, -40, -30],
                [-30, -40, -40, -50, -50, -40, -40, -30],
            ],
        }
        self.color = color
        if self.color == chess.BLACK:
            self.positionalValue[chess.PAWN].reverse()
            self.positionalValue[chess.ROOK].reverse()
            self.positionalValue[chess.KING].reverse()
        self.opponentPositionalValue = {
            typ: table[::-1]
            for typ, table in self.positionalValue.items()
        }
    def evaluate(self, board: chess.Board):
        if board.can_claim_draw() and board.turn != self.color:
            # It's bad
            return -10000
        if board.is_checkmate():
            if board.turn == self.color:
                # My turn, but I have no legal move => I got mated
                return -10000
            else:
                return 10000
        evaluation = 0
        for typ, val in self.values.items():
            for i in board.pieces(typ, self.color):
                rk, fl = chess.square_rank(i), chess.square_file(i)
                evaluation += self.positionalValue[typ][rk][fl] + val
            # evaluation += len(board.pieces(typ, self.color)) * val
            for i in board.pieces(typ, not self.color):
                rk, fl = chess.square_rank(i), chess.square_file(i)
                evaluation -= self.opponentPositionalValue[typ][rk][fl] + val
            # evaluation -= len(board.pieces(typ, not self.color)) * val
        direction = 1 if self.color == chess.WHITE else -1
        for i in board.pieces(chess.ROOK, self.color):
            rk, fl = chess.square_rank(i), chess.square_file(i)
            blocked = False
            while 0 <= rk < 8:
                piece = board.piece_at(chess.square(fl, rk))
                if piece != None:
                    if piece.piece_type == chess.PAWN and piece.color != self.color:
                        blocked = True
                rk += direction
            if blocked:
                evaluation -= 20
        for i in board.pieces(chess.ROOK, not self.color):
            rk, fl = chess.square_rank(i), chess.square_file(i)
            blocked = False
            while 0 <= rk < 8:
                piece = board.piece_at(chess.square(fl, rk))
                if piece != None:
                    if piece.piece_type == chess.PAWN and piece.color == self.color:
                        blocked = True
                rk -= direction
            if blocked:
                evaluation += 20
        return evaluation
    def minimax(self, board: chess.Board, depth, alpha = -float("inf"), beta = float("inf")):
        self.tot += 1
        if depth == 0 or board.is_game_over():
            return [self.evaluate(board), None]
        moves = list(board.legal_moves)
        moves.sort(key = lambda m: moveScore(board, m))
        if board.turn == self.color:
            best = -float("inf")
            bestMove = None
            for move in moves:
                board.push(move)
                score = self.minimax(board, depth - 1, alpha, beta)[0]
                board.pop()
                if score > best:
                    best = score
                    bestMove = move
                alpha = max(alpha, best)
                if alpha >= beta:
                    break
            return [best, bestMove]
        else:
            best = float("inf")
            bestMove = None
            for move in moves:
                board.push(move)
                score = self.minimax(board, depth - 1, alpha, best)[0]
                board.pop()
                if score < best:
                    best = score
                    bestMove = move
                beta = min(beta, best)
                if alpha >= beta:
                    break
            return [best, bestMove]
    def getNextMove(self):
        self.tot = 0
        mv = self.minimax(self.board, 4)[1]
        print(self.tot)
        return mv
    def move(self, move):
        self.board.push(move)