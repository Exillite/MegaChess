class Piece:
    def __init__(self, color, img, x, y):
        self.color = color  # True - white, False - black
        self.x = x
        self.y = y
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
    def __init__(self, color, x, y):
        if color:
            super().__init__(color, "wp", x, y)
        else:
            super().__init__(color, "bp", x, y)


class King(Piece):
    def __init__(self, color, x, y):
        if color:
            super().__init__(color, "wK", x, y)
        else:
            super().__init__(color, "bK", x, y)


class Queen(Piece):
    def __init__(self, color, x, y):
        if color:
            super().__init__(color, "wQ", x, y)
        else:
            super().__init__(color, "bQ", x, y)


class Bishop(Piece):
    def __init__(self, color, x, y):
        if color:
            super().__init__(color, "wB", x, y)
        else:
            super().__init__(color, "bB", x, y)


class Knight(Piece):
    def __init__(self, color, x, y):
        if color:
            super().__init__(color, "wN", x, y)
        else:
            super().__init__(color, "bN", x, y)


class Rook(Piece):
    def __init__(self, color, x, y):
        if color:
            super().__init__(color, "wR", x, y)
        else:
            super().__init__(color, "bR", x, y)


class Spase:
    def __init__(self):
        self.img = "bQ"

    def __str__(self):
        return "no_piece"


def getBoard():
    b = []
    for i in range(8):
        b.append([])
        for j in range(8):
            b[i].append(Spase())

    b[0][0] = Rook(True, 0, 0)
    b[1][0] = Knight(True, 1, 0)
    b[2][0] = Bishop(True, 2, 0)
    b[3][0] = Queen(True, 3, 0)
    b[4][0] = King(True, 4, 0)
    b[5][0] = Bishop(True, 5, 0)
    b[6][0] = Knight(True, 6, 0)
    b[7][0] = Rook(True, 7, 0)
    for i in range(8):
        b[i][1] = Pawn(True, i, 1)

    b[0][7] = Rook(False, 0, 7)
    b[1][7] = Knight(False, 1, 7)
    b[2][7] = Bishop(False, 2, 7)
    b[3][7] = Queen(False, 3, 7)
    b[4][7] = King(False, 4, 7)
    b[5][7] = Bishop(False, 5, 7)
    b[6][7] = Knight(False, 6, 7)
    b[7][7] = Rook(False, 7, 7)
    for i in range(8):
        b[i][6] = Pawn(False, i, 6)

    return b
