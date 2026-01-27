from pygame.math import Vector2 as vec
from game_assets import Gem
import json

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

def load_masks(file: str) -> list:
    with open(file, 'r') as file:
        data = json.load(file)
    return data['masks']

class Check_Matching():
    masks = load_masks('json/masks.json')
    @classmethod
    def check(cls, board: list[Gem]) -> list[Gem, vec] | None:
        cls.move_help = None
        cls.direction_help = None
        for mask in cls.masks:
            for row, board_row in enumerate(board):
                for column, _ in enumerate(board_row):
                    lst = list(cls.get_mask_area_from_board(board, mask, (row, column)))
                    if len(lst) == len([item for row in mask for item in row]):
                        if len(set(lst)) == 2:
                            return (board[row+__class__.move_help[0]][column+__class__.move_help[1]],
                                    vec(__class__.direction_help[0]-__class__.move_help[0], __class__.direction_help[1]-__class__.move_help[1])) 
        return (None, None)

    @staticmethod
    def get_mask_area_from_board(board, mask, offset):
        for ir, row in enumerate(mask):
            for ic, column in enumerate(row):
                if column == 2: __class__.move_help = [ir, ic]
                if column == -1: __class__.direction_help = [ir, ic]
                if ir+offset[0] < len(board) and ic+offset[1] < len(board[0]):
                    mask_value = column // column if column > 0 else 0
                    yield board[ir+offset[0]][ic+offset[1]].number * mask_value