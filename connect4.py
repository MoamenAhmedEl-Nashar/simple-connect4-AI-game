import copy
import time

# Global variables initiation
MAX_LEVEL = 2
TIME_LIMIT = 10


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
        print("< 0 > < 1 > < 2 > < 3 > < 4 > < 5 > < 6 >")
        for row in self.board:
            print(row)
        print("-----------------------------------------")

    def get_col(self, col_num):
        """
        return a list that contains a specific column in the board
        column 0 is the most left one.
        """
        col = []
        for row in self.board:
            col.append(row[col_num])
        return col

    def get_possible_diag(self):
        """
        returns a list contains all possible diagonal items in the board.
        """
        diagonals_list = []
        for i in range(1, 4):
            diagonal = []
            x = 0
            for j in range(i, 7):
                # print(self.board[x])
                diagonal.append(self.board[x][j])
                x += 1
            diagonals_list.append(diagonal)
        for i in range(0, 3):
            x = 0
            diagonal = []
            for j in range(i, 6):
                diagonal.append(self.board[j][x])
                x += 1
            diagonals_list.append(diagonal)

        for i in range(4, 6):
            diagonal = []
            x = 0
            for j in range(i, -1, -1):
                diagonal.append(self.board[x][j])
                x += 1
            diagonals_list.append(diagonal)
        for i in range(0, 3):
            x = 6
            diagonal = []
            for j in range(i, 6):
                diagonal.append(self.board[j][x])
                x -= 1
            diagonals_list.append(diagonal)
        return diagonals_list

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


def connected_items_in_board(board_object, item_color):
    """
    this is a helper function that used in utility function.
    it counts the maximum number of connected items of specific color in a board state.
    inputs :
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
    for index in range(0, 7):
        connected_items_in_column = connected_items_in_list(board_object.get_col(index), item_color)
        utility = connected_items_in_column if connected_items_in_column > utility else utility

    # diagonal connected items

    for diag in board_object.get_possible_diag():
        connected_items_in_diag = connected_items_in_list(diag, item_color)
        utility = connected_items_in_diag if connected_items_in_diag > utility else utility
    # utility is the maximum number of connected items in all directions
    pass
    return utility


def utility(board_object, item_color):
    """
    this function calculates the utility of any board state.
    inputs:
    board_object : the board state
    item_color : "RED" or "YEL"
    outputs:
    utility : integer between 0, 4

    """
    vs_item_color = "YEL" if item_color == "RED" else "RED"
    utility = connected_items_in_board(board_object, item_color)
    if connected_items_in_board(board_object, vs_item_color) == 4:
        utility = 0
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
        if moved_board_object.board == board_object.board:  # col is complete
            continue
        possible_boards.append(moved_board_object)
    return possible_boards


def best_board(initial_board_object, level, type, alpha, beta, item_color, root_item_color):
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
            util = utility(board_object, root_item_color)
            if type == "MIN":
                if util < beta:
                    beta = util
                    next_board_object = copy.deepcopy(board_object)
                if beta <= alpha:  # cut-off
                    break
            elif type == "MAX":
                if util > alpha:
                    alpha = util
                    next_board_object = copy.deepcopy(board_object)
                if beta <= alpha:  # cut-off
                    break

    if level < MAX_LEVEL:
        for board_object in possible_boards:
            new_level = level + 1
            new_type = "MIN" if type == "MAX" else "MAX"
            new_item_color = "YEL" if item_color == "RED" else "RED"
            child_alpha, child_beta, _ = best_board(board_object, new_level, new_type, alpha, beta, new_item_color,
                                                    root_item_color)
            if type == "MAX" and alpha < child_beta:
                alpha = child_beta
                next_board_object = copy.deepcopy(board_object)
            if type == "MIN" and beta > child_alpha:
                beta = child_alpha
                next_board_object = copy.deepcopy(board_object)
    return alpha, beta, next_board_object


def best_board_Iterative_Deepening(initial_board_object, level, type, alpha, beta, item_color, root_item_color):
    """
    this function simulates the mini-max with alpha-beta pruning algorithm,
    with iterative deepening search.
    inputs:
    initial_board_object : root of the search tree.
    level : it should always be 1 at beginning , but recursive calls will increase
    it until reach maximum level.
    type : Maximizer node or Minimizer node
    alpha : alpha is for the alpha-beta pruning algorithm.
    beta : beta is for the alpha-beta pruning algorithm.
    item_color : "RED" or "YEL"
    outputs:
    next_board_object : the best next state to move to.
    """
    global MAX_LEVEL
    while True:
        start = time.time()
        _, _, next_board = best_board(initial_board_object, level, type, alpha, beta, item_color, root_item_color)
        end = time.time()
        if (int(end - start) >= (TIME_LIMIT - 2)) or (connected_items_in_board(next_board, 'RED') == 4):
            return next_board
        MAX_LEVEL += 1


def play_PlayNOW_mode():
    """
    this is the main function that controls the game playing .
    it has no inputs or outputs.
    """
    board = Board()
    start_first = input("Who start first : you(y) or AI(a)")
    if start_first == "y":
        board.print_board()
        while True:
            col_num = input("your color is yellow , insert in which column:")
            board.insert(int(col_num), "YEL")
            if connected_items_in_board(board, 'YEL') == 4:
                board.print_board()
                print('NICE, You Won')
                break
            _, _, next_board = best_board(board, 1, "MAX", -100, 100, "RED", "RED")
            board = copy.deepcopy(next_board)
            if connected_items_in_board(board, 'RED') == 4:
                board.print_board()
                print('Game Over, You Lose')
                break
            board.print_board()
    if start_first == "a":
        while True:
            _, _, next_board = best_board(board, 1, "MAX", -100, 100, "RED", "RED")
            board = copy.deepcopy(next_board)
            if connected_items_in_board(board, 'RED') == 4:
                board.print_board()
                print('Game Over, You Lose')
                break
            board.print_board()
            col_num = input("your color is yellow , insert in which column:")
            board.insert(int(col_num), "YEL")
            if connected_items_in_board(board, 'YEL') == 4:
                board.print_board()
                print('NICE, You Won')
                break


def play_Time_Mode():
    """
    this is the main function that controls the game playing .
    it has no inputs or outputs.
    """
    board = Board()
    start_first = input("Who start first : you(y) or AI(a)")
    if start_first == "y":
        board.print_board()
        while True:
            col_num = input("your color is yellow , insert in which column:")
            board.insert(int(col_num), "YEL")
            if connected_items_in_board(board, 'YEL') == 4:
                board.print_board()
                print('NICE, You Won')
                break
            next_board = best_board_Iterative_Deepening(board, 1, "MAX", -100, 100, "RED", "RED")
            board = copy.deepcopy(next_board)
            if connected_items_in_board(board, 'RED') == 4:
                board.print_board()
                print('Game Over, You Lose')
                break
            board.print_board()
    if start_first == "a":
        while True:
            next_board = best_board_Iterative_Deepening(board, 1, "MAX", -100, 100, "RED", "RED")
            board = copy.deepcopy(next_board)
            if connected_items_in_board(board, 'RED') == 4:
                board.print_board()
                print('Game Over, You Lose')
                break
            board.print_board()
            col_num = input("your color is yellow , insert in which column:")
            board.insert(int(col_num), "YEL")
            if connected_items_in_board(board, 'YEL') == 4:
                board.print_board()
                print('NICE, You Won')
                break


if __name__ == '__main__':
    while True:
        mode = input('Choose Mode: TimeLimit(t) or PlayNow(p)')
        if mode == 'p':
            level = input('Choose your level: easy(e) or medium(m) or hard(h)')
            if level == 'e':
                MAX_LEVEL = 1
            if level == 'm':
                MAX_LEVEL = 3
            if level == 'h':
                MAX_LEVEL = 4
            play_PlayNOW_mode()
            print('\nIt was a Good Game, See You later :)\n')
            again = input('Play again now? YES(y) or NO(n)')
            if again == 'y':
                print('\n')
                continue
            if again == 'n':
                break
        if mode == 't':
            timeLimit = input('Enter the time limit 2 or more seconds: ')
            TIME_LIMIT = int(timeLimit)
            play_Time_Mode()
            print('\nIt was a Good Game, See You later :)\n')
            again = input('Play again now? YES(y) or NO(n)')
            if again == 'y':
                print('\n')
                continue
            if again == 'n':
                break
