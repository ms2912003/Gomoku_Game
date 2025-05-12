import random
import pygame
import sys
import math
import time
from pygame.locals import *

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Constants
SIZE = WIDTH, HEIGHT = 600, 600
ROWS, COLS = 15, 15
SQUARE_SIZE = WIDTH // COLS
LINE_WIDTH = 2
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
EMPTY = 0
PLAYER = 1
AI = 2
AI_MINIMAX = 1  # AI using Minimax (in AI vs AI mode)
AI_ALPHABETA = 2
PLAYER1 = 'X'  # AI Minimax
PLAYER2 = 'O'  # AI Alpha-Beta
DEPTH = 1  # Reduced for speed

# Initialize screen
screen = pygame.display.set_mode(SIZE, RESIZABLE)
pygame.display.set_caption('Gomoku')
background = pygame.image.load('Images/wood_texture.jpeg')
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
menu_background = pygame.image.load('Images/menu.jpg')
menu_background = pygame.transform.scale(menu_background, (WIDTH, HEIGHT))

button_click_sound = pygame.mixer.Sound('Sounds/Mouse_Click.mp3')
win_sound = pygame.mixer.Sound('Sounds/Win_Sound.wav')
lose_sound = pygame.mixer.Sound('Sounds/Lose_Sound.wav')

# Initialize board
board = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]

font = pygame.font.SysFont(None, 60)
small_font = pygame.font.SysFont(None, 40)
MENU_FONT = pygame.font.SysFont(None, 40)


class Button:
    def __init__(self, text, x, y, width, height, color, hover_color, text_color=WHITE):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.font = pygame.font.SysFont(None, 36)
        self.is_hovered = False

    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=5)
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=5)  # Border

        label = self.font.render(self.text, True, self.text_color)
        label_rect = label.get_rect(center=self.rect.center)
        surface.blit(label, label_rect)

    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered

    def is_clicked(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pos)
        return False


def draw_board():
    screen.fill(WHITE)
    screen.blit(background, (0, 0))
    for row in range(ROWS):
        pygame.draw.line(screen, BLACK, (0, row * SQUARE_SIZE), (WIDTH, row * SQUARE_SIZE), LINE_WIDTH)
    for col in range(COLS):
        pygame.draw.line(screen, BLACK, (col * SQUARE_SIZE, 0), (col * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == PLAYER or board[row][col] == AI_MINIMAX:  # Red for human or Minimax AI
                pygame.draw.circle(screen, RED,
                                   (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2),
                                   SQUARE_SIZE // 3)
            elif board[row][col] == AI or board[row][col] == AI_ALPHABETA:  # Blue for regular AI or Alpha-Beta AI
                pygame.draw.circle(screen, BLUE,
                                   (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2),
                                   SQUARE_SIZE // 3)


def display_message(text, y_pos=30):
    font = pygame.font.SysFont(None, 60)
    message = font.render(text, True, (0, 128, 0))  # Green text
    text_rect = message.get_rect(center=(WIDTH // 2, y_pos))
    screen.blit(message, text_rect)
    pygame.display.update()
    pygame.time.wait(3000)  # Show message for 3 seconds


def is_valid_move(row, col):
    return board[row][col] == EMPTY


def check_win(player):
    for row in range(ROWS):
        for col in range(COLS - 4):
            if all(board[row][col + i] == player for i in range(5)):
                return True
    for row in range(ROWS - 4):
        for col in range(COLS):
            if all(board[row + i][col] == player for i in range(5)):
                return True
    for row in range(ROWS - 4):
        for col in range(COLS - 4):
            if all(board[row + i][col + i] == player for i in range(5)):
                return True
    for row in range(4, ROWS):
        for col in range(COLS - 4):
            if all(board[row - i][col + i] == player for i in range(5)):
                return True
    return False


def get_valid_moves():
    moves = []
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == EMPTY:
                if any(board[r][c] != EMPTY for r in range(max(0, row - 1), min(ROWS, row + 2)) for c in
                       range(max(0, col - 1), min(COLS, col + 2))):
                    moves.append((row, col))
    return moves if moves else [(ROWS // 2, COLS // 2)]


def evaluate_board(player):
    opponent = PLAYER if player == AI else AI
    player_score = score_lines(player)
    opponent_score = score_lines(opponent)
    return player_score - opponent_score


def score_lines(player):
    score = 0
    lines = []

    # Horizontal, vertical, diagonal, anti-diagonal
    for row in range(ROWS):
        for col in range(COLS - 4):
            lines.append([board[row][col + i] for i in range(5)])
    for row in range(ROWS - 4):
        for col in range(COLS):
            lines.append([board[row + i][col] for i in range(5)])
    for row in range(ROWS - 4):
        for col in range(COLS - 4):
            lines.append([board[row + i][col + i] for i in range(5)])
    for row in range(4, ROWS):
        for col in range(COLS - 4):
            lines.append([board[row - i][col + i] for i in range(5)])

    for line in lines:
        count = line.count(player)
        if count == 5:
            score += 100000
        elif count == 4 and line.count(EMPTY) == 1:
            score += 10000
        elif count == 3 and line.count(EMPTY) == 2:
            score += 1000
        elif count == 2 and line.count(EMPTY) == 3:
            score += 100
        elif count == 1 and line.count(EMPTY) == 4:
            score += 10

    return score


def minimax(depth, maximizingPlayer):
    if check_win(AI):
        return None, None, 100000
    elif check_win(PLAYER):
        return None, None, -100000
    elif depth == 0:
        return None, None, evaluate_board(AI)

    valid_moves = get_valid_moves()
    best_move = None

    if maximizingPlayer:
        max_eval = -math.inf
        for move in valid_moves:
            row, col = move
            board[row][col] = AI
            _, _, eval = minimax(depth - 1, False)
            board[row][col] = EMPTY
            if eval > max_eval:
                max_eval = eval
                best_move = (row, col)
        return *best_move, max_eval
    else:
        min_eval = math.inf
        for move in valid_moves:
            row, col = move
            board[row][col] = PLAYER
            _, _, eval = minimax(depth - 1, True)
            board[row][col] = EMPTY
            if eval < min_eval:
                min_eval = eval
                best_move = (row, col)
        return *best_move, min_eval


def alphabeta(depth, alpha, beta, maximizingPlayer):
    if check_win(PLAYER2):
        return None, None, 100000
    elif check_win(PLAYER1):
        return None, None, -100000
    elif depth == 0:
        return None, None, evaluate_board(PLAYER2)

    valid_moves = get_valid_moves()
    best_moves = []

    if maximizingPlayer:
        max_eval = -math.inf
        for move in valid_moves:
            row, col = move
            board[row][col] = PLAYER2
            _, _, eval = alphabeta(depth - 1, alpha, beta, False)
            board[row][col] = EMPTY
            if eval > max_eval:
                max_eval = eval
                best_moves = [(row, col)]
            elif eval == max_eval:
                best_moves.append((row, col))
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return *random.choice(best_moves), max_eval
    else:
        min_eval = math.inf
        for move in valid_moves:
            row, col = move
            board[row][col] = PLAYER1
            _, _, eval = alphabeta(depth - 1, alpha, beta, True)
            board[row][col] = EMPTY
            if eval < min_eval:
                min_eval = eval
                best_moves = [(row, col)]
            elif eval == min_eval:
                best_moves.append((row, col))
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return *random.choice(best_moves), min_eval


def find_winning_move(player):
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == EMPTY:
                board[row][col] = player
                if check_win(player):
                    board[row][col] = EMPTY
                    return row, col
                board[row][col] = EMPTY
    return None


def display_menu():
    screen.blit(menu_background, (0, 0))

    # Create a semi-transparent background for the title
    title_bg = pygame.Surface((WIDTH - 100, 60), pygame.SRCALPHA)
    title_bg.fill((0, 0, 0, 150))
    title_bg_rect = title_bg.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    screen.blit(title_bg, title_bg_rect)

    # Render the title text with shadow for better visibility
    title = MENU_FONT.render("Choose a game mode:", True, WHITE)
    title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 4))

    shadow = MENU_FONT.render("Choose a game mode:", True, (50, 50, 50))
    screen.blit(shadow, (title_rect.x + 2, title_rect.y + 2))
    screen.blit(title, title_rect)

    # Create buttons
    button_width = WIDTH // 2
    button_height = 60
    start_y = HEIGHT // 2
    padding = 20

    human_vs_ai_button = Button("Human vs AI",
                                WIDTH // 2 - button_width // 2,
                                start_y,
                                button_width,
                                button_height,
                                (76, 175, 80),  # Green
                                (50, 150, 50))

    ai_vs_ai_button = Button("AI vs AI",
                             WIDTH // 2 - button_width // 2,
                             start_y + button_height + padding,
                             button_width,
                             button_height,
                             (33, 150, 243),  # Blue
                             (20, 120, 220))

    exit_button = Button("Exit",
                         WIDTH // 2 - button_width // 2,
                         start_y + 2 * (button_height + padding),
                         button_width,
                         button_height,
                         (244, 67, 54),  # Red
                         (200, 50, 50))

    # Draw buttons
    human_vs_ai_button.draw(screen)
    ai_vs_ai_button.draw(screen)
    exit_button.draw(screen)

    pygame.display.update()

    # Wait for user input
    waiting_for_choice = True
    game_mode = None
    while waiting_for_choice:
        mouse_pos = pygame.mouse.get_pos()
        human_vs_ai_button.check_hover(mouse_pos)
        ai_vs_ai_button.check_hover(mouse_pos)
        exit_button.check_hover(mouse_pos)

        # Redraw buttons to update hover state
        screen.blit(menu_background, (0, 0))
        screen.blit(title_bg, title_bg_rect)
        screen.blit(shadow, (title_rect.x + 2, title_rect.y + 2))
        screen.blit(title, title_rect)
        human_vs_ai_button.draw(screen)
        ai_vs_ai_button.draw(screen)
        exit_button.draw(screen)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if human_vs_ai_button.is_clicked(mouse_pos, event):
                    play_sound()
                    game_mode = 'Human vs AI'
                    waiting_for_choice = False
                elif ai_vs_ai_button.is_clicked(mouse_pos, event):
                    play_sound()
                    game_mode = 'AI vs AI'
                    waiting_for_choice = False
                elif exit_button.is_clicked(mouse_pos, event):
                    play_sound()
                    pygame.quit()
                    sys.exit()
    return game_mode


def show_pause_screen():
    pause_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    pause_surface.fill((0, 0, 0, 150))  # Semi-transparent black
    screen.blit(pause_surface, (0, 0))

    pause_text = font.render("PAUSED", True, WHITE)
    resume_text = small_font.render("Click anywhere to resume", True, WHITE)

    screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(resume_text, (WIDTH // 2 - resume_text.get_width() // 2, HEIGHT // 2 + 20))

    pygame.display.update()

    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                paused = False
                return True  # Game should continue
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return False  # Go back to menu

    return True


def play_sound():
    button_click_sound.play()


def reset_game():
    global board
    board = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]


def human_vs_ai_game():
    running = True
    player_turn = True
    game_active = True

    # Create buttons
    back_button = Button("Back to Menu", 10, 10, 150, 40, (100, 100, 100), (70, 70, 70))
    pause_button = Button("Pause", WIDTH - 110, 10, 100, 40, (100, 100, 100), (70, 70, 70))

    draw_board()
    back_button.draw(screen)
    pause_button.draw(screen)
    pygame.display.update()

    while running:
        mouse_pos = pygame.mouse.get_pos()
        back_button.check_hover(mouse_pos)
        pause_button.check_hover(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.is_clicked(mouse_pos, event):
                    play_sound()
                    return True  # Signal to go back to menu

                if pause_button.is_clicked(mouse_pos, event):
                    play_sound()
                    if not show_pause_screen():
                        return True  # Signal to go back to menu
                    # Redraw the game after pause
                    draw_board()
                    back_button.draw(screen)
                    pause_button.draw(screen)
                    pygame.display.update()
                    continue

            if game_active and player_turn and event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                # Check if click is on the board (not on buttons)
                if y > 60:  # Below the button area
                    row = y // SQUARE_SIZE
                    col = x // SQUARE_SIZE
                    if is_valid_move(row, col):
                        board[row][col] = PLAYER
                        draw_board()
                        back_button.draw(screen)
                        pause_button.draw(screen)
                        pygame.display.update()
                        if check_win(PLAYER):
                            win_sound.play()
                            display_message("YOU WON!")
                            game_active = False
                        player_turn = False

        if game_active and not player_turn:
            start_time = time.time()

            # 1. AI can win now?
            winning_move = find_winning_move(AI)
            if winning_move:
                row, col = winning_move
            else:
                # 2. Human is about to win? Block it.
                block_move = find_winning_move(PLAYER)
                if block_move:
                    row, col = block_move
                else:
                    # 3. Minimax or Alpha-Beta decision
                    if random.choice([True, False]):
                        row, col, _ = minimax(DEPTH, True)
                    else:
                        row, col, _ = alphabeta(DEPTH, -math.inf, math.inf, True)

            # Execute the AI move
            board[row][col] = AI
            draw_board()
            back_button.draw(screen)
            pause_button.draw(screen)
            pygame.display.update()

            if check_win(AI):
                lose_sound.play()
                display_message("AI WON!")
                game_active = False
            player_turn = True
            print(f"AI Move completed in {time.time() - start_time:.2f}s")

        # Redraw buttons to update hover state
        draw_board()
        back_button.draw(screen)
        pause_button.draw(screen)
        pygame.display.update()

    return False  # Game ended normally


def ai_vs_ai_game():
    print("Starting AI vs AI (Minimax vs Alpha-Beta)...")
    draw_board()

    # Create buttons
    back_button = Button("Back to Menu", 10, 10, 150, 40, (100, 100, 100), (70, 70, 70))
    pause_button = Button("Pause", WIDTH - 110, 10, 100, 40, (100, 100, 100), (70, 70, 70))

    back_button.draw(screen)
    pause_button.draw(screen)
    pygame.display.update()

    turn = AI_MINIMAX
    move_count = 0
    game_over = False
    game_active = True

    while not game_over:
        mouse_pos = pygame.mouse.get_pos()
        back_button.check_hover(mouse_pos)
        pause_button.check_hover(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.is_clicked(mouse_pos, event):
                    play_sound()
                    return True  # Signal to go back to menu
                if pause_button.is_clicked(mouse_pos, event):
                    play_sound()
                    if not show_pause_screen():
                        return True  # Signal to go back to menu
                    # Redraw the game after pause
                    draw_board()
                    back_button.draw(screen)
                    pause_button.draw(screen)
                    pygame.display.update()

        if game_active and not game_over:
            start = time.time()
            if turn == AI_MINIMAX:
                row, col, _ = minimax(DEPTH, True)
                print(f"AI (Minimax) plays: ({row}, {col})")
                player_marker = AI_MINIMAX
            else:
                row, col, _ = alphabeta(DEPTH, -math.inf, math.inf, True)
                print(f"AI (Alpha-Beta) plays: ({row}, {col})")
                player_marker = AI_ALPHABETA

            if row is not None and col is not None:
                board[row][col] = player_marker
                draw_board()
                back_button.draw(screen)
                pause_button.draw(screen)
                pygame.display.update()
                move_count += 1
                print(f"Move {move_count} completed in {time.time() - start:.2f}s")

                if check_win(player_marker):
                    win_sound.play()
                    winner = "Minimax AI" if turn == AI_MINIMAX else "Alpha-Beta AI"
                    print(f"{winner} WINS!")
                    display_message(f"{winner} WINS!", y_pos=100)
                    game_over = True
                elif all(cell != EMPTY for row in board for cell in row):
                    print("It's a draw!")
                    display_message("It's a draw!", y_pos=100)
                    game_over = True

                turn = AI_ALPHABETA if turn == AI_MINIMAX else AI_MINIMAX
                pygame.time.delay(500)  # Delay between AI moves

        # Redraw buttons to update hover state
        draw_board()
        back_button.draw(screen)
        pause_button.draw(screen)
        pygame.display.update()
    if game_over:
        waiting_for_menu = True
        while waiting_for_menu:
            mouse_pos = pygame.mouse.get_pos()
            back_button.check_hover(mouse_pos)
            back_button.draw(screen)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button.is_clicked(mouse_pos, event):
                        play_sound()
                        waiting_for_menu = False
                        return True  # Return to menu
    return False  # Game ended normally


def main():
    while True:
        game_mode = display_menu()
        reset_game()
        if game_mode == "Human vs AI":
            should_return = human_vs_ai_game()
            if not should_return:
                break
        elif game_mode == "AI vs AI":
            should_return = ai_vs_ai_game()
            if not should_return:
                break
if __name__ == "__main__":
    main()