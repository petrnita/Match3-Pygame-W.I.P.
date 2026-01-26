from consts import GAME
from game_assets import Gem

masks = [
    [[0, 1, 0], # <- mask_row
     [1, 0, 1]],
    # ^
    # L mask_column

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
'''
    The class checks whether there is at least one possible match on the game board.
        This check is performed using masks for 16 possible match combinations.
            If the ones in the mask overlap with stones of the same color,
        multiplying the mask by the board fields results in only two numbers:
        the value representing the stone paired with the one, and zero.
                    When the board fields do not match the mask,
        more than one number will be generated at the positions of the ones.
     Consequently, the set will contain values from the board fields and zero.
    The check() function verifies if a set containing exactly two numbers occurs.
                If so, the function terminates and returns True.
If this case is not detected after iterating through the entire board, it returns False.
'''

class Check_Matching():
    @classmethod
    def check(cls, board: list[Gem]) -> bool:
        for board_x in range(int(GAME.BOARD_SIZE.x)):
            for board_y in range(int(GAME.BOARD_SIZE.y)):
                for mask in masks:
                    masked = set()
                    for mask_row in range(len(mask)):
                        for mask_column in range(len(mask[0])):
                            masking_field = mask[mask_row][mask_column]
                            if mask_row+board_y < int(GAME.BOARD_SIZE.y) and mask_column+board_x < int(GAME.BOARD_SIZE.x):
                                field = board[mask_column+board_x][mask_row+board_y]
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
