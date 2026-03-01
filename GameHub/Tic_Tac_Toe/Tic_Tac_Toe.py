import pygame

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 3, 3
RECT_HEIGHT = HEIGHT // ROWS
RECT_WIDTH = WIDTH // COLS

# Colors
BEIGE = (205, 192, 180)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

OUTLINE_THICKNESS = 10

# Board state
Board = [None, None, None,
         None, None, None,
         None, None, None]

# Players
P1 = 'X'
P2 = 'O'

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")

def draw_grid(screen):
    # Draw the grid lines
    for row in range(1, ROWS):
        y = row * RECT_HEIGHT
        pygame.draw.line(screen, BLACK, (0, y), (WIDTH, y), OUTLINE_THICKNESS)

    for col in range(1, COLS):
        x = col * RECT_WIDTH
        pygame.draw.line(screen, BLACK, (x, 0), (x, HEIGHT), OUTLINE_THICKNESS)

    pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, HEIGHT), OUTLINE_THICKNESS)

def get_cell_index(mouse_pos):
    # Get the index of the cell based on mouse position
    x, y = mouse_pos
    col = x // RECT_WIDTH
    row = y // RECT_HEIGHT
    return row * COLS + col

def draw_symbol(screen, index, symbol):
    # Draw the player's symbol (X or O) on the board
    row = index // COLS
    col = index % COLS
    center_x = col * RECT_WIDTH + RECT_WIDTH // 2
    center_y = row * RECT_HEIGHT + RECT_HEIGHT // 2

    if symbol == 'X':
        pygame.draw.line(screen, RED,
                         (center_x - 50, center_y - 50),
                         (center_x + 50, center_y + 50), 5)
        pygame.draw.line(screen, RED,
                         (center_x + 50, center_y - 50),
                         (center_x - 50, center_y + 50), 5)
    elif symbol == 'O':
        pygame.draw.circle(screen, BLUE, (center_x, center_y), 50, 5)

def check_winner(board):
    # Check if there is a winner
    win_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]              # Diagonals
    ]

    for combo in win_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] and board[combo[0]] is not None:
            return board[combo[0]]

    return None

def is_board_full(board):
    # Check if the board is full
    return all(cell is not None for cell in board)

def display_end_screen(window, message):
    # Display the end screen with the result
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))
    window.blit(overlay, (0, 0))

    end_font = pygame.font.SysFont("comicsans", 50, bold=True)
    text = end_font.render(message, True, (255, 255, 255))
    window.blit(
        text,
        (WIDTH // 2 - text.get_width() / 2, HEIGHT // 3 - text.get_height() // 2)
    )

    sub_font = pygame.font.SysFont("comicsans", 30, bold=True)
    sub_text = sub_font.render("Press R to Restart or Q to Quit", True, (200, 200, 200))
    window.blit(
        sub_text,
        (WIDTH / 2 - sub_text.get_width() // 2, HEIGHT // 2)
    )

    pygame.display.update()

def main_Tic_Tac_Toe():
    global Board

    screen.fill(BEIGE)
    draw_grid(screen)

    Board = [None] * 9
    running = True
    current_player = P1
    game_over = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()

            if game_over:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        Board = [None] * 9
                        screen.fill(BEIGE)
                        draw_grid(screen)
                        current_player = P1
                        game_over = False
                    if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        running = False
                        pygame.quit()
                        exit()
                continue

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                cell_index = get_cell_index(mouse_pos)

                if Board[cell_index] is None:
                    Board[cell_index] = current_player
                    draw_symbol(screen, cell_index, current_player)

                    winner = check_winner(Board)
                    if winner:
                        display_end_screen(screen, f"{winner} Wins!")
                        game_over = True
                    elif is_board_full(Board):
                        display_end_screen(screen, "It's a tie!")
                        game_over = True
                    else:
                        current_player = P2 if current_player == P1 else P1

                    pygame.display.flip()

        pygame.display.flip()

if __name__ == "__main__":
    main_Tic_Tac_Toe()