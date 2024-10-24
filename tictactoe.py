import math
import random

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """Returns the starting state of the board."""
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """Returns the player who has the next turn on a board. X always goes first."""
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    return O if x_count > o_count else X


def actions(board):
    """Returns set of all possible actions (i, j) available on the board."""
    available_actions = {(i, j) for i in range(3) for j in range(3) if board[i][j] == EMPTY}
    return available_actions


def result(board, action):
    """Returns the board that results from making move (i, j) on the board."""
    i, j = action
    if board[i][j] != EMPTY:
        raise ValueError("Invalid move: Cell already occupied.")
    new_board = [row[:] for row in board]
    new_board[i][j] = player(board)
    return new_board


def winner(board):
    """Returns the winner of the game, if there is one."""
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] is not None:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] is not None:
            return board[0][i]
    
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        return board[0][2]

    return None


def terminal(board):
    """Returns True if the game is over, False otherwise."""
    return winner(board) is not None or all(cell is not EMPTY for row in board for cell in row)


def utility(board):
    """Returns 1 if X has won the game, -1 if O has won, 0 otherwise."""
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    return 0

def minimax(board, randomness=0.3): #difficulty level (0 - )
    # (0 for optimal action, 1 for most random action)
    """Returns the optimal action for the current player on the board."""
    if terminal(board):
        return None

    # Compute best actions first (optimal actions without randomness)
    def max_value(board):
        if terminal(board):
            return utility(board)
        v = -math.inf
        for action in actions(board):
            v = max(v, min_value(result(board, action)))
        return v

    def min_value(board):
        if terminal(board):
            return utility(board)
        v = math.inf
        for action in actions(board):
            v = min(v, max_value(result(board, action)))
        return v

    current_player = player(board)
    best_actions = []

    if current_player == X:
        best_value = -math.inf
        for action in actions(board):
            action_value = min_value(result(board, action))
            if action_value > best_value:
                best_value = action_value
                best_actions = [action]  
            elif action_value == best_value:
                best_actions.append(action)
    else:
        best_value = math.inf
        for action in actions(board):
            action_value = max_value(result(board, action))
            if action_value < best_value:
                best_value = action_value
                best_actions = [action]  
            elif action_value == best_value:
                best_actions.append(action)

    optimal_action = random.choice(best_actions)
    print("\n=======================================")
    print("----- AI Decision Making -----")
    print(f"Optimal action would have been: {optimal_action}")   #best action

    random_value = random.random()  #randomness in decision-making
    print(f"Random value: {random_value} (randomness threshold: {randomness})")
    
    if random_value < randomness:
        available_actions = list(actions(board))
        random_action = random.choice(available_actions)
        print(f"Random action selected: {random_action}")
        return random_action

    print(f"Optimal action selected: {optimal_action}")
    return optimal_action
