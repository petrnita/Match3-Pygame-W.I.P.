from consts import GAME
from game_assets import Gem

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
    def check(cls, board: list[Gem]) -> bool:
        for field_x in range(int(GAME.BOARD_SIZE.x)):
            for field_y in range(int(GAME.BOARD_SIZE.y)):
                for _mask in mask:
                    masked = set()
                    for row in range(len(_mask)):
                        for column in range(len(_mask[0])):
                            masking_field = _mask[row][column]
                            if row+field_y < int(GAME.BOARD_SIZE.y) and column+field_x < int(GAME.BOARD_SIZE.x):
                                field = board[column+field_x][row+field_y]
                                if field != None:
                                    masked.add(field.number*masking_field)
                                else:
                                    break
                            else:
                                masked.clear()
                                break
                    if len(masked) == 2:
                        return True
        return False
