from pygame.math import Vector2 as vec
from game_assets import Gem
import numpy as np

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
masks = [
    [[0, 0, 2, 0, 0],
    [1, 1, -1, 1, 1],
    [0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0]],
        
    [[0, 2, 0, 0],
    [1, -1, 1, 1],
    [0, 1, 0, 0],
    [0, 1, 0, 0]],

    [[0, 0, 2, 0],
    [1, 1, -1, 1],
    [0, 0, 1, 0],
    [0, 0, 1, 0]],

    [[2, -1, 1, 1],
    [0, 1, 0, 0],
    [0, 1, 0, 0]],

    [[0, 1, 0, 0],
    [0, 1, 0, 0],
    [2, -1, 1,1]],

    [[0, 1, 0, 0],
    [2, -1, 1, 1],
    [0, 1, 0, 0]],

    [[0, 0, 2, 0, 0],
    [1, 1, -1, 1, 1]],

    [[0, 2, 0, 0],
    [1, -1, 1, 1]],

    [[0, 0, 2, 0],
    [1, 1, -1, 1]],
        
    [[1, 1, -1, 2]],

    [[0, 2, 0],
    [1, -1, 1]],
 
    [[2, 0, 0],
    [-1, 1, 1]],

    [[0, 0, 2],
    [1, 1, -1]],
]

def load_masks(data: list) -> list:
    _np_data = np.zeros([len(data)*4], dtype=object)
    for i, d in enumerate(data):
        _np_d = np.array(d)
        _np_data[i*4] = _np_d
        for j in range(1, 4):
            _np_data[i*4+j] = np.rot90(_np_d, k=j)
    return _np_data.tolist()


class Check_Matching():
    _masks = load_masks(masks)
    @classmethod
    def check(cls, board: list[Gem]) -> list[Gem, vec] | list[None]:
        # rng = np.random.default_rng()
        # if np.random.choice([False, True]):
        #     rng.shuffle(masks)
        for mask in cls._masks:
            for row, board_row in enumerate(board):
                for column, _ in enumerate(board_row):
                    lst = list(cls.get_mask_area_from_board(board, mask, (row, column)))
                    numbers = [x[0] for x in lst]
                    ids = [x[1] for x in lst]
                    if len(numbers) == len([item for row in mask for item in row]):
                        if len(set(numbers)) == 2:
                            # print(time.time())
                            # print(f'{np.transpose(np.array(numbers).reshape([len(mask), len(mask[0])]), (1, 0))} > [{row=} {column=}]')
                            # print(f'{np.transpose(np.array(ids).reshape([len(mask), len(mask[0])]), (1, 0))}')
                            find_gem = np.where(np.array(mask, dtype=int)==2)
                            direction = np.where(np.array(mask, dtype=int)==-1)
                            return (board[row+find_gem[0][0]][column+find_gem[1][0]],
                                    vec(direction[0]-find_gem[0][0], direction[1]-find_gem[1][0]))
                
        return [None, None]

    @staticmethod
    def get_mask_area_from_board(board: list[Gem], mask, offset):
        for ir, row in enumerate(mask):
            for ic, column in enumerate(row):
                if ir+offset[0] < len(board) and ic+offset[1] < len(board[0]):
                    mask_value = column // column if column > 0 else 0
                    yield board[ir+offset[0]][ic+offset[1]].number * mask_value, board[ir+offset[0]][ic+offset[1]].id