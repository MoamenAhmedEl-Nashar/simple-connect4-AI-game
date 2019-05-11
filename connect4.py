import copy

MAX_LEVEL = 2

class Board:
    """
    the Board class contains one member variable , and it is th 2D board array,
    that simulates the shape of the connected4 game board.
    """
    def __init__(self):
        self.board = [
            [None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None]
        ]
    def print_board(self):
        """
        print board in a suitable shape on the console.
        """
        for row in self.board:
            print(row)
        print("-----------------------------------------")

    def get_col(self, col_num):
        """
        return a list that contains a specif column in the board
        column 0 is the most left one.
        """
        col = []
        for row in self.board:
            col.append(row[col_num])
        return col

    def insert(self, col_num, item_color):
        """
        insert an item of specific color in a specific column.
        """
        col = self.get_col(col_num)
        for i in range(5, -1, -1):
            if col[i] is None:
                self.board[i][col_num] = item_color
                break
        

def connected_items_in_list(items_list, item_color):
    """
    this is a helper function that used in utility function.
    it counts the maximum number of connected items of specific color in a list.
    inputs : 
    items_list : list of the game items : None, "RED", or "YEL"
    item_color : "RED", "YEL" to count

    outputs:
    max_connected_num : the maximum number of connected items of specific color in a list
    """
    max_connected_num = 0
    connected_num = 0
    for item in items_list:
        if item == item_color:
            connected_num += 1
            max_connected_num = connected_num if connected_num > max_connected_num else max_connected_num
        else:
            connected_num = 0
    return max_connected_num


def utility(board_object, item_color):
    """
    this function calculates the utility of any board state.
    inputs:
    board_object : the board state
    item_color : "RED" or "YEL"

    outputs:
    utility : integer from 1 to 4 .
    if utility is 4 it's a winning state for any of the two players. 
    """
    # horizontal connected items
    utility = 0
    for row in board_object.board:
        connected_items_in_row = connected_items_in_list(row, item_color)
        utility = connected_items_in_row if connected_items_in_row > utility else utility

    # vertical connected items
    pass
    # diagonal connected items 
    pass
    # utility is the maximum number of connected items in all dirctions
    pass
    return utility


def get_possible_boards(board_object, item_color):
    """
    this function gets all possible moves from a given board state.
    inputs:
    board_object : the state we want to get all possible moves from.
    item_color : "RED" or "YEL"

    outputs:
    possible_boards : list contains all next states. 
    """
    possible_boards = []
    moved_board_object = Board()
    for i in range(0, 7):
        moved_board_object = copy.deepcopy(board_object) 
        col = moved_board_object.get_col(i)
        moved_board_object.insert(i, item_color)
        possible_boards.append(moved_board_object)
    return possible_boards


def best_board(initial_board_object, level, type, alpha, beta, item_color):
    """
    this function simulates the mini-max with alpha-beta pruning algorithm,
    with depth first search.
    inputs:
    initial_board_object : root of the search tree.
    level : it should always be 1 at beginning , but recursive calls will increase 
    it until reach maximum level.
    type : Maximizer node or Minimizer node
    alpha : alpha is for the alpha-beta pruning algorithm.
    beta : beta is for the alpha-beta pruning algorithm.
    item_color : "RED" or "YEL"

    outputs:
    alpha, beta : the final values of alpha, beta for the initial board.
    next_board_object : the best next state to move to.
    """
    next_board_object = Board()
    possible_boards = get_possible_boards(initial_board_object, item_color)
    if level == MAX_LEVEL:
        for board_object in possible_boards:
            util = utility(board_object, item_color)
            if type == "MIN":
                if util < beta:
                    beta = util
                if beta <= alpha:  # cut-off
                    break
            elif type == "MAX":
                if util > alpha:
                    alpha = util
                if beta <= alpha:  # cut-off
                    break
    if level < MAX_LEVEL:
        for board_object in possible_boards:
            new_level = level + 1
            new_type = "MIN" if type == "MAX" else "MAX"
            #new_item_color = "YEL" if item_color == "RED" else "RED"
            child_alpha, child_beta, _ = best_board(board_object, new_level, new_type, alpha, beta, item_color)
            if type == "MAX" and alpha < child_beta:
                alpha = child_beta
                next_board_object = copy.deepcopy(board_object)
            if type == "MIN" and beta > child_alpha:
                beta = child_alpha
                next_board_object = copy.deepcopy(board_object)
    return alpha, beta, next_board_object


def play():
    """
    this is the main function that controls the game playing .
    it has no inputs or outputs.
    """
    board = Board()
    start_first = input("Who start first : you(y) or AI(a)")
    if start_first == "y":
        for i in range(5):  # for debugging only, it should be while until a winning state
            col_num = input("your color is yellow , insert in which column:")
            board.insert(int(col_num), "YEL")
            _, _, next_board = best_board(board, 1, "MAX", -100, 100, "RED")
            board = copy.deepcopy(next_board)
            board.print_board()
    if start_first == "a":  # for debugging only, it should be while until a winning state
        for i in range(5):
            _, _, next_board = best_board(board, 1, "MAX", -100, 100, "RED")
            board = copy.deepcopy(next_board)
            board.print_board()
            col_num = input("your color is yellow , insert in which column:")
            board.insert(int(col_num), "YEL")

play()
