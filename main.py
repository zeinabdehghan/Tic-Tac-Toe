import copy

def print_board(board):
    # making a table for game
    n = len(board)
    for row in board:
        print(" | ".join(row))
        print("-" * (4 * n - 1))

def is_winner(board, player):
    n = len(board)
    # check rows and columns for a win
    for i in range(n):
        if all(board[i][j] == player for j in range(n)) or all(board[j][i] == player for j in range(n)):
            return True
    if all(board[i][i] == player for i in range(n)) or all(board[i][n - 1 - i] == player for i in range(n)):
        return True
    return False

def is_full(board):
    # check all the full cells and return them
    return all(board[i][j] != ' ' for i in range(len(board)) for j in range(len(board[0])))

def get_empty_cells(board):
    # check the empty cells and return them
    return [(i, j) for i in range(len(board)) for j in range(len(board[0])) if board[i][j] == ' ']

def minimax(board, depth, alpha, beta, maximizing_player):
    # checking if there is a winner.
    if is_winner(board, 'O'):
        return 1
    elif is_winner(board, 'X'):
        return -1
    elif is_full(board):
        return 0

    if depth == 0:
        return 0
    # if the current player is maximizing, find the maximum evaluation value
    if maximizing_player:
        max_eval = float('-inf')
        for i, j in get_empty_cells(board):
            new_board = copy.deepcopy(board)
            new_board[i][j] = 'O'
            eval = minimax(new_board, depth - 1, alpha, beta, False)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            print(f"Alpha value at depth {depth}: {alpha}")
            # if beta is less than or equal to alpha, cut off the search
            if beta <= alpha:
                print(f"Alpha cut at depth {depth}, alpha = {alpha}, beta = {beta}")
                break
        return max_eval
    else:
        # if the current player is minimizing, find the minimum evaluation value
        min_eval = float('inf')
        for i, j in get_empty_cells(board):
            new_board = copy.deepcopy(board)
            new_board[i][j] = 'X'
            eval = minimax(new_board, depth - 1, alpha, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            print(f"Beta value at depth {depth}: {beta}")
            # if beta is less than or equal to alpha, cut off the search
            if beta <= alpha:
                print(f"Beta cut at depth {depth}, alpha = {alpha}, beta = {beta}")
                break
        return min_eval

def get_best_move(board, depth_limit):
    # finds and return the best move for the algorithm using the minimax algorithm with alpha-beta pruning.
    best_eval = float('-inf')
    best_move = None
    alpha = float('-inf')
    beta = float('inf')

    for i, j in get_empty_cells(board):
        new_board = copy.deepcopy(board)
        new_board[i][j] = 'O'
        eval = minimax(new_board, depth_limit, alpha, beta, False)
        if eval > best_eval:
            best_eval = eval
            best_move = (i, j)
    return best_move

def get_player_move(board):
    # taking the moves from the player and checking if the cell is empty
    while True:
        try:
            move = input("Enter your move (row and column, e.g., 1 2): ")
            i, j = map(int, move.split())
            if board[i - 1][j - 1] == ' ':
                return i - 1, j - 1
            else:
                print("Cell already occupied. Try again.")
        except (ValueError, IndexError):
            print("Invalid input. Please enter row and column numbers.")

def play_game_with_algorithm(n, difficulty):

    # making a board for game
    board = [[' ' for _ in range(n)] for _ in range(n)]
    print_board(board)

    # checking what depth_limit should be passed
    if difficulty == 'easy':
        depth_limit = 1
    elif difficulty == 'hard' and n <= 3:
        depth_limit = float('inf')
    elif difficulty == 'hard' and n > 3:
        depth_limit = 1
    else:
        print("Invalid difficulty. Defaulting to hard.")
        depth_limit = float('inf')

    player_turn = True

    # checking if board is empty and no one has won yet and then make the moves
    while not is_full(board) and not any(is_winner(board, player) for player in ['X', 'O']):
        if player_turn:
            i, j = get_player_move(board)
            player = 'X'
        else:
            i, j = get_best_move(board, depth_limit)
            player = 'O'

        print(f"\n{player} plays at ({i + 1}, {j + 1}):")
        board[i][j] = player
        print_board(board)

        player_turn = not player_turn

    # finding the winner or if the game is even.
    winner = next((player for player in ['X', 'O'] if is_winner(board, player)), None)
    if winner:
        print(f"Player {winner} wins!")
    else:
        print("The game is even!")

def algorithm_play_with_algorithm():
    # a game between two algorithms using the minimax algorithm with alpha-beta pruning.

    n = 3  # assuming a 3x3 board for this example
    depth_limit = float('inf')  # using the maximum depth for both algorithms
    board = [[' ' for _ in range(n)] for _ in range(n)]
    print_board(board)

    while not is_full(board) and not any(is_winner(board, player) for player in ['X', 'O']):
        # Player X (Algorithm 1)
        i, j = get_best_move(board, depth_limit)
        player = 'X'
        print(f"\n{player} plays at ({i + 1}, {j + 1}):")
        board[i][j] = player
        print_board(board)

        if is_winner(board, player):
            print(f"Player {player} wins!")
            return

        if is_full(board):
            print("The game is even!")
            return

        # Player O (Algorithm 2)
        i, j = get_best_move(board, depth_limit)
        player = 'O'
        print(f"\n{player} plays at ({i + 1}, {j + 1}):")
        board[i][j] = player
        print_board(board)

        if is_winner(board, player):
            print(f"Player {player} wins!")
            return

        if is_full(board):
            print("The game is even!")
            return

if __name__ == "__main__":
    print("tic tac toe game.")

    while True:
        print("\nChoose an option:")
        print("1. Play with algorithm")
        print("2. Algorithm vs Algorithm")
        print("3. Quit")

        choice = input("Enter your choice (1/2/3): ")

        if choice == '1':
            n = int(input("Enter the board size (n): "))
            difficulty = input("Choose difficulty (easy/hard): ")
            play_game_with_algorithm(n, difficulty)
        elif choice == '2':
            algorithm_play_with_algorithm()

        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
