class Piece:
    def __init__(self, color, img):
        self.color = color  # True - white, False - black
        self.x = 0
        self.y = 0
        self.is_alive = True
        self.img = img

    def go(self, x, y, board):
        if board[x][y] is None:
            board[self.x][self.y] = None
            self.x = x
            self.y = y
            board[x][y] = self
            return True
        else:
            return False


class Pawn(Piece):
    def __init__(self, color):
        if color:
            super().__init__(color, "wp")
        else:
            super().__init__(color, "bp")


class King(Piece):
    def __init__(self, color):
        if color:
            super().__init__(color, "wK")
        else:
            super().__init__(color, "bK")


class Queen(Piece):
    def __init__(self, color):
        if color:
            super().__init__(color, "wQ")
        else:
            super().__init__(color, "bQ")


class Bishop(Piece):
    def __init__(self, color):
        if color:
            super().__init__(color, "wB")
        else:
            super().__init__(color, "bB")


class Knight(Piece):
    def __init__(self, color):
        if color:
            super().__init__(color, "wN")
        else:
            super().__init__(color, "bN")


class Rook(Piece):
    def __init__(self, color):
        if color:
            super().__init__(color, "wR")
        else:
            super().__init__(color, "bR")


def getBoard():
    b = [[None] * 8] * 8

    b[0][0] = Rook(True)
    b[1][0] = Knight(True)
    b[2][0] = Bishop(True)
    b[3][0] = Queen(True)
    b[4][0] = King(True)
    b[5][0] = Bishop(True)
    b[6][0] = Knight(True)
    b[7][0] = Rook(True)
    for i in range(8):
        b[i][1] = Pawn(True)

    b[0][7] = Rook(True)
    b[1][7] = Knight(True)
    b[2][7] = Bishop(True)
    b[3][7] = Queen(True)
    b[4][7] = King(True)
    b[5][7] = Bishop(True)
    b[6][7] = Knight(True)
    b[7][7] = Rook(True)
    for i in range(8):
        b[i][1] = Pawn(True)



