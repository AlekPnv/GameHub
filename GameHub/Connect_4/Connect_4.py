import pygame
import sys
import numpy as np

# Constants
ROWS = 6
COLS = 7
SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 5)
width = COLS * SQUARESIZE
height = (ROWS + 1) * SQUARESIZE
size = (width, height)
BLUE = (0, 0, 255)
BLACK = "#A4A4A4" # Gray -> too much work to change it
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
turn = 0
game_over = False

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Connect 4")
myfont = pygame.font.SysFont("monospace", 75)

# Create the board
class Board:
    def __init__(self):
        self.board = np.zeros((ROWS, COLS))  # Initialize the board with zeros

    def draw_board(self):
        # Draw the board and pieces
        for c in range(COLS):
            for r in range(ROWS):
                pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
                pygame.draw.circle(screen, BLACK, (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)
        for c in range(COLS):
            for r in range(ROWS):
                if self.board[r][c] == 1:
                    pygame.draw.circle(screen, RED, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
                elif self.board[r][c] == 2:
                    pygame.draw.circle(screen, YELLOW, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
        pygame.display.update()

    def drop_piece(self, row, col, piece):
        self.board[row][col] = piece  # Drop the piece in the board

    def is_valid_location(self, col):
        return self.board[ROWS - 1][col] == 0  # Check if the column is valid for a move

    def get_next_open_row(self, col):
        for r in range(ROWS):
            if self.board[r][col] == 0:
                return r  # Get the next open row in the column

    def print_board(self):
        print(np.flip(self.board, 0))  # Print the board

    def winning_move(self, piece):
        # Check horizontal locations for win
        for c in range(COLS - 3):
            for r in range(ROWS):
                if self.board[r][c] == piece and self.board[r][c + 1] == piece and self.board[r][c + 2] == piece and self.board[r][c + 3] == piece:
                    return True

        # Check vertical locations for win
        for c in range(COLS):
            for r in range(ROWS - 3):
                if self.board[r][c] == piece and self.board[r + 1][c] == piece and self.board[r + 2][c] == piece and self.board[r + 3][c] == piece:
                    return True

        # Check positively sloped diagonals
        for c in range(COLS - 3):
            for r in range(ROWS - 3):
                if self.board[r][c] == piece and self.board[r + 1][c + 1] == piece and self.board[r + 2][c + 2] == piece and self.board[r + 3][c + 3] == piece:
                    return True

        # Check negatively sloped diagonals
        for c in range(COLS - 3):
            for r in range(3, ROWS):
                if self.board[r][c] == piece and self.board[r - 1][c + 1] == piece and self.board[r - 2][c + 2] == piece and self.board[r - 3][c + 3] == piece:
                    return True

    def is_draw(self):
        return not any(self.board[ROWS - 1][c] == 0 for c in range(COLS))  # Check if the game is a draw

def display_message(message):
    # Display a message on the screen
    label = myfont.render(message, 1, RED if "Red" in message else YELLOW)
    screen.blit(label, (40, 10))
    pygame.display.update()
    pygame.time.wait(1250)

def play_again_screen():
    # Display the play again screen
    screen.fill(BLACK)
    label = myfont.render("Play Again?", 1, RED)
    label_y = myfont.render("Y/N", 1, YELLOW)
    screen.blit(label, (120, 220))
    screen.blit(label_y, (270, 330))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    return True
                elif event.key == pygame.K_n or event.key == pygame.K_ESCAPE:
                    return False

board = Board()
board.draw_board()

# Main game loop
def main_Connect_4():
    global turn, game_over, board
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                # Draw the piece that follows the mouse
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                posx = event.pos[0]
                if turn == 0:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
                else:
                    pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over and event.button == 1:
                # Handle the mouse button down event
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                posx = event.pos[0]
                col = int(posx / SQUARESIZE)

                if board.is_valid_location(col):
                    row = board.get_next_open_row(col)
                    if turn == 0:
                        board.drop_piece(row, col, 1)
                        if board.winning_move(1):
                            display_message("Red wins!")
                            game_over = True
                    else:
                        board.drop_piece(row, col, 2)
                        if board.winning_move(2):
                            display_message("Yellow wins!")
                            game_over = True

                    if board.is_draw():
                        display_message("Draw!")
                        game_over = True

                    board.print_board()
                    board.draw_board()

                    turn += 1
                    turn = turn % 2

                    if game_over:
                        if play_again_screen():
                            board = Board()
                            board.draw_board()
                            game_over = False
                            turn = 0
                        else:
                            pygame.quit()
                            sys.exit()

if __name__ == "__main__":
    main_Connect_4()