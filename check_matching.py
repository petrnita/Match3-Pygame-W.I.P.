from consts import GAME

mask = [
    [[0, 1, 0],
     [1, 0, 1]],

    [[1, 0, 1],
     [0, 1, 0]],

    [[1, 1, 0, 1]],

    [[1, 0, 1, 1]],

    [[1, 1, 0],
     [0, 0, 1]],

    [[0, 0, 1],
     [1, 1, 0]],

    [[1, 0, 0],
     [0, 1, 1]],

    [[0, 1, 1],
     [1, 0, 0]],

    [[1, 0],
     [1, 0],
     [0, 1]],

    [[0, 1],
     [0, 1],
     [1, 0]],

    [[1, 0],
     [0, 1],
     [0, 1]],

    [[0, 1],
     [1, 0],
     [1, 0]],

    [[0, 1],
     [1, 0],
     [0, 1]],

    [[1, 0],
     [0, 1],
     [1, 0]],

    [[1],
     [1],
     [0],
     [1]],

    [[1],
     [0],
     [1],
     [1]]
]


class Check_Matching():
    @classmethod
    def check(cls, board) -> bool:
        for x in range(int(GAME.BOARD_SIZE.x)):
            for y in range(int(GAME.BOARD_SIZE.y)):
                for m in mask:
                    masked = set()
                    for ir in range(len(m)):
                        for ic in range(len(m[0])):
                            if ir+y < int(GAME.BOARD_SIZE.y) and ic+x < int(GAME.BOARD_SIZE.x):
                                if board[ic+x][ir+y] != None:
                                    masked.add(board[ic+x][ir+y].number*m[ir][ic])
                                else:
                                    break
                            else:
                                masked.clear()
                                break
                    if len(masked) == 2:
                        return True
        return False