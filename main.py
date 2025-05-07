
import sys
import math
import random


BOARD_SIZE = 15
WIN_LENGTH = 5
EMPTY = ' '
PLAYER1 = 'X'  # Human
PLAYER2 = 'O'  # AI

PATTERNS = {
    # Immediate win/loss conditions
    f"{PLAYER2}{PLAYER2}{PLAYER2}{PLAYER2}{PLAYER2}": 1000000,  # AI win
    f"{PLAYER1}{PLAYER1}{PLAYER1}{PLAYER1}{PLAYER1}": -1000000,  # Block human win

    # Defensive patterns (blocking human)
    f"{EMPTY}{PLAYER1}{PLAYER1}{PLAYER1}{PLAYER1}{EMPTY}": -50000,
    f"{PLAYER1}{PLAYER1}{PLAYER1}{PLAYER1}{EMPTY}": -25000,
    f"{EMPTY}{PLAYER1}{PLAYER1}{PLAYER1}{PLAYER1}": -25000,
    f"{EMPTY}{PLAYER1}{PLAYER1}{PLAYER1}{EMPTY}": -5000,
    f"{PLAYER1}{PLAYER1}{PLAYER1}{EMPTY}": -2500,
    f"{EMPTY}{PLAYER1}{PLAYER1}{PLAYER1}": -2500,
    f"{EMPTY}{PLAYER1}{PLAYER1}{EMPTY}": -500,
    f"{PLAYER1}{PLAYER1}{EMPTY}": -250,
    f"{EMPTY}{PLAYER1}{PLAYER1}": -250,

    # Offensive patterns (AI building)
    f"{EMPTY}{PLAYER2}{PLAYER2}{PLAYER2}{PLAYER2}{EMPTY}": 10000,
    f"{PLAYER2}{PLAYER2}{PLAYER2}{PLAYER2}{EMPTY}": 5000,
    f"{EMPTY}{PLAYER2}{PLAYER2}{PLAYER2}{PLAYER2}": 5000,
    f"{EMPTY}{PLAYER2}{PLAYER2}{PLAYER2}{EMPTY}": 1000,
    f"{PLAYER2}{PLAYER2}{PLAYER2}{EMPTY}": 500,
    f"{EMPTY}{PLAYER2}{PLAYER2}{PLAYER2}": 500,
    f"{EMPTY}{PLAYER2}{PLAYER2}{EMPTY}": 100,
    f"{PLAYER2}{PLAYER2}{EMPTY}": 50,
    f"{EMPTY}{PLAYER2}{PLAYER2}": 50,

    f"{EMPTY}{PLAYER2}{EMPTY}": 10,
    f"{EMPTY}{PLAYER1}{EMPTY}": -5
}


def create_board():

    return [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]


def print_board(board):

    row_num_width = len(str(BOARD_SIZE - 1))
    print(" " * (row_num_width + 1), end="")
    for col in range(BOARD_SIZE):
        print(f" {col:2} ", end="")
    print()
    print(" " * (row_num_width + 1) + "┌" + ("───┬" * (BOARD_SIZE - 1)) + "───┐")

    for row in range(BOARD_SIZE):
        print(f"{row:{row_num_width}} │", end="")
        for col in range(BOARD_SIZE):
            cell = board[row][col]
            print(f" {cell} │", end="")
        print()
        if row < BOARD_SIZE - 1:
            print(" " * (row_num_width + 1) + "├" + ("───┼" * (BOARD_SIZE - 1)) + "───┤")
    print(" " * (row_num_width + 1) + "└" + ("───┴" * (BOARD_SIZE - 1)) + "───┘")


def is_valid_move(board, x, y):

    return 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE and board[x][y] == EMPTY


def make_move(board, x, y, player):
    board[x][y] = player


def check_win(board, player):
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            if board[x][y] != player:
                continue
            for dx, dy in directions:
                count = 0
                for k in range(WIN_LENGTH):
                    nx, ny = x + dx * k, y + dy * k
                    if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and board[nx][ny] == player:
                        count += 1
                    else:
                        break
                if count == WIN_LENGTH:
                    return True
    return False


def is_board_full(board):
    return all(cell != EMPTY for row in board for cell in row)


def get_player_move(board, player):
    player_name = "Player 1 (X)" if player == PLAYER1 else "AI (O)"
    while True:
        try:
            if player == PLAYER1:
                move = input(f"{player_name}'s turn. Enter your move (row col): ").strip()
                if move.lower() == 'quit':
                    print("Game ended by player.")
                    sys.exit(0)
                x, y = map(int, move.split())
            else:
                x, y = find_best_move(board)
                print(f"AI plays at {x} {y}")

            if is_valid_move(board, x, y):
                return x, y
            elif player == PLAYER1:
                print("Invalid move. Try again or type 'quit' to exit.")
        except ValueError:
            if player == PLAYER1:
                print("Invalid input. Please enter two numbers separated by space (e.g., '7 8').")

def evaluate_board_fast(board):

    score = 0
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            if board[x][y] == EMPTY:
                continue

            for dx, dy in directions:
                sequence = []
                for i in range(6):
                    nx, ny = x + dx * i, y + dy * i
                    if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE:
                        sequence.append(board[nx][ny])
                    else:
                        sequence.append(None)

                seq_str = ''.join([cell if cell is not None else ' ' for cell in sequence])

                for pattern in PATTERNS:
                    if pattern in seq_str:
                        score += PATTERNS[pattern]
                        break

    return score

def find_best_move(board):
    best_score = -math.inf
    best_move = None
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            if is_valid_move(board, x, y):
                board[x][y] = PLAYER2
                if check_win(board, PLAYER2):
                    board[x][y] = EMPTY
                    return (x, y)
                board[x][y] = EMPTY

    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            if is_valid_move(board, x, y):
                board[x][y] = PLAYER1
                if check_win(board, PLAYER1):
                    board[x][y] = EMPTY
                    return (x, y)
                board[x][y] = EMPTY

    possible_moves = get_possible_moves(board)
    if not possible_moves:
        empty_cells = [(x, y) for x in range(BOARD_SIZE) for y in range(BOARD_SIZE) if is_valid_move(board, x, y)]
        return random.choice(empty_cells) if empty_cells else (BOARD_SIZE // 2, BOARD_SIZE // 2)

    random.shuffle(possible_moves)

    for move in possible_moves:
        x, y = move
        board[x][y] = PLAYER2
        score = minimax(board, 2, False)
        board[x][y] = EMPTY

        if score > best_score:
            best_score = score
            best_move = move
        elif score == best_score and random.random() < 0.3:
            best_move = move

    return best_move if best_move else possible_moves[0]


def minimax(board, depth, is_maximizing):

    if check_win(board, PLAYER2):
        return 1000000
    if check_win(board, PLAYER1):
        return -1000000
    if depth == 0 or is_board_full(board):
        return evaluate_board_fast(board)

    if is_maximizing:
        best_score = -math.inf
        for move in get_possible_moves(board):
            x, y = move
            board[x][y] = PLAYER2
            score = minimax(board, depth - 1, False)
            board[x][y] = EMPTY
            best_score = max(score, best_score)

        return best_score
    else:
        best_score = math.inf
        for move in get_possible_moves(board):
            x, y = move
            board[x][y] = PLAYER1
            score = minimax(board, depth - 1, True)
            board[x][y] = EMPTY
            best_score = min(score, best_score)
        return best_score


################################
def find_best_move_alphabeta(board):
    best_score = -math.inf
    best_move = None
    alpha = -math.inf
    beta = math.inf

    # Check for immediate winning move for AI
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            if is_valid_move(board, x, y):
                board[x][y] = PLAYER2
                if check_win(board, PLAYER2):
                    board[x][y] = EMPTY
                    return (x, y)
                board[x][y] = EMPTY

    # Check for immediate block of opponent's win
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            if is_valid_move(board, x, y):
                board[x][y] = PLAYER1
                if check_win(board, PLAYER1):
                    board[x][y] = EMPTY
                    return (x, y)
                board[x][y] = EMPTY

    # Alpha-Beta search for best move
    possible_moves = get_possible_moves(board)
    if not possible_moves:
        empty_cells = [(x, y) for x in range(BOARD_SIZE) for y in range(BOARD_SIZE) if is_valid_move(board, x, y)]
        return random.choice(empty_cells) if empty_cells else (BOARD_SIZE // 2, BOARD_SIZE // 2)

    random.shuffle(possible_moves)

    for move in possible_moves:
        x, y = move
        board[x][y] = PLAYER2
        score = alpha_beta(board, 3, alpha, beta, False)
        board[x][y] = EMPTY

        if score > best_score:
            best_score = score
            best_move = move
        elif score == best_score and random.random() < 0.3:
            best_move = move

        alpha = max(alpha, best_score)
        if beta <= alpha:
            break

    return best_move if best_move else possible_moves[0]

def alpha_beta(board, depth, alpha, beta, maximizing_player):

    if depth == 0 or is_board_full(board):
        return evaluate_board_fast(board)

    if check_win(board, PLAYER2):
        return 1000000
    if check_win(board, PLAYER1):
        return -1000000

    if maximizing_player:
        value = -math.inf
        for move in get_candidate_moves(board):
            x, y = move
            board[x][y] = PLAYER2
            value = max(value, alpha_beta(board, depth - 1, alpha, beta, False))
            board[x][y] = EMPTY
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value
    else:
        value = math.inf
        for move in get_candidate_moves(board):
            x, y = move
            board[x][y] = PLAYER1
            value = min(value, alpha_beta(board, depth - 1, alpha, beta, True))
            board[x][y] = EMPTY
            beta = min(beta, value)
            if alpha >= beta:
                break
        return value




def get_candidate_moves(board):
    """Get high-quality candidate moves with aggressive pruning"""
    moves = set()
    danger_moves = set()
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            if board[x][y] != EMPTY:
                for dx, dy in directions:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and board[nx][ny] == EMPTY:
                        if board[x][y] == PLAYER1:
                            danger_moves.add((nx, ny))
                        moves.add((nx, ny))


    if danger_moves:
        return list(danger_moves)
    elif moves:
        return list(moves)
    elif is_valid_move(board, BOARD_SIZE // 2, BOARD_SIZE // 2):
        return [(BOARD_SIZE // 2, BOARD_SIZE // 2)]
    else:
        return [(x, y) for x in range(BOARD_SIZE) for y in range(BOARD_SIZE) if is_valid_move(board, x, y)]

def get_possible_moves(board):
    moves = set()
    danger_zones = set()
    directions = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1), (0, 1),
                  (1, -1), (1, 0), (1, 1)]

    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            if board[x][y] == PLAYER1:
                for dx, dy in directions:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and board[nx][ny] == EMPTY:
                        danger_zones.add((nx, ny))

    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            if board[x][y] != EMPTY:
                for dx, dy in directions:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and board[nx][ny] == EMPTY:
                        moves.add((nx, ny))

    combined_moves = list(danger_zones.union(moves)) if danger_zones else list(moves)

    if not combined_moves and is_valid_move(board, BOARD_SIZE // 2, BOARD_SIZE // 2):
        return [(BOARD_SIZE // 2, BOARD_SIZE // 2)]

    return combined_moves if combined_moves else None


def game_loop():

    board = create_board()
    current_player = PLAYER1

    print("Welcome to Gomoku Game!")
    print("Enter your moves as 'row column' (e.g., '7 8')")
    print("Type 'quit' to exit the game.\n")
    print_board(board)

    while True:
        x, y = get_player_move(board, current_player)
        make_move(board, x, y, current_player)
        print_board(board)

        if check_win(board, current_player):
            winner = "Player 1 (X)" if current_player == PLAYER1 else "AI (O)"
            print(f"\n{winner} wins!")
            break

        if is_board_full(board):
            print("\nThe game is a draw!")
            break

        current_player = PLAYER2 if current_player == PLAYER1 else PLAYER1

def game_loop_ai_vs_ai():
    board = create_board()
    current_player = PLAYER1
    print_board(board)
    while True:
        if current_player == PLAYER1:
            x, y = find_best_move(board)
            print(f"AI 1 (Minimax) plays at: {x}, {y}")
        else:
            x, y = find_best_move_alphabeta(board)
            print(f"AI 2 (Alpha-Beta) plays at: {x}, {y}")

        make_move(board, x, y, current_player)
        print_board(board)

        if check_win(board, current_player):
            winner = "AI 1 (Minimax)" if current_player == PLAYER1 else "AI 2 (Alpha-Beta)"
            print(f"{winner} wins!")
            break
        if is_board_full(board):
            print("It's a draw!")
            break

        current_player = PLAYER2 if current_player == PLAYER1 else PLAYER1


if __name__ == "__main__":
    print("Welcome to Gomoku Game!")
    print("Choose Game Mode:")
    print("1-->Human vs AI")
    print("2-->AI vs AI")

    choice = input("Enter 1 or 2: ").strip()

    if choice == '1':
        game_loop()
    elif choice == '2':
        game_loop_ai_vs_ai()
    else:
        print("Invalid choice. Please run the program again and enter 1 or 2.")