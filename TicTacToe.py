import pygame
import random

def game():
    # Initialize Pygame
    pygame.init()

    # Constants
    WIDTH, HEIGHT = 300, 300
    LINE_COLOR = (0, 0, 0)
    LINE_WIDTH = 15
    BOARD_SIZE = 3
    SQUARE_SIZE = WIDTH // BOARD_SIZE

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    # Initialize the screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tic-Tac-Toe")

    # Fonts
    font = pygame.font.Font(None, 36)

    # Function to draw the Tic-Tac-Toe board
    def draw_board(board):
        screen.fill(WHITE)
        for i in range(1, BOARD_SIZE):
            pygame.draw.line(screen, LINE_COLOR, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, HEIGHT), LINE_WIDTH)
            pygame.draw.line(screen, LINE_COLOR, (0, i * SQUARE_SIZE), (WIDTH, i * SQUARE_SIZE), LINE_WIDTH)
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if board[row][col] == 1:
                    draw_symbol(row, col, 1)
                elif board[row][col] == 2:
                    draw_symbol(row, col, 2)    

    # Function to check for a win
    def check_win(board, player):
        for i in range(BOARD_SIZE):
            if all(board[i][j] == player for j in range(BOARD_SIZE)) or all(board[j][i] == player for j in range(BOARD_SIZE)):
                return True

        if all(board[i][i] == player for i in range(BOARD_SIZE)) or all(board[i][BOARD_SIZE - 1 - i] == player for i in range(BOARD_SIZE)):
            return True

        return False

    # Function to check for a tie
    def check_tie(board):
        return all(all(cell != 0 for cell in row) for row in board)

    # Function to draw X or O on the board
    def draw_symbol(row, col, player):
        x = col * SQUARE_SIZE + SQUARE_SIZE // 2
        y = row * SQUARE_SIZE + SQUARE_SIZE // 2

        if player == 1:
            pygame.draw.line(screen, BLACK, (x - 50, y - 50), (x + 50, y + 50), LINE_WIDTH)
            pygame.draw.line(screen, BLACK, (x + 50, y - 50), (x - 50, y + 50), LINE_WIDTH)
        else:
            pygame.draw.circle(screen, BLACK, (x, y), 50, LINE_WIDTH)

    # Function to make a move for the AI
    def make_ai_move(board):
        # Check for a winning move
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board[i][j] == 0:
                    board[i][j] = 2
                    if check_win(board, 2):
                        board[i][j] = 0  # Undo the move
                        return i, j
                    board[i][j] = 0  # Undo the move

        # Check for a blocking move
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board[i][j] == 0:
                    board[i][j] = 1
                    if check_win(board, 1):
                        board[i][j] = 0  # Undo the move
                        return i, j
                    board[i][j] = 0  # Undo the move

        # If no winning or blocking move, make a random move
        empty_cells = [(i, j) for i in range(BOARD_SIZE) for j in range(BOARD_SIZE) if board[i][j] == 0]
        return random.choice(empty_cells)

    # Main game loop
    def main():
        # Initialize the board
        board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]

        # Randomly choose the starting player
        current_player = random.choice([1, 2])

        # Game state
        game_over = False

        # Game loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN and current_player == 1 and not game_over:
                    col = event.pos[0] // SQUARE_SIZE
                    row = event.pos[1] // SQUARE_SIZE

                    if board[row][col] == 0:
                        board[row][col] = 1
                        draw_symbol(row, col, 1)

                        if check_win(board, 1):
                            print("You win!")
                            game_over = True
                            break
                        elif check_tie(board):
                            print("It's a tie!")
                            game_over = True
                            break

                        current_player = 2

                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and game_over:
                    # Restart the game
                    board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
                    current_player = random.choice([1, 2])
                    game_over = False

                if current_player == 2 and not game_over:
                    row, col = make_ai_move(board)

                    if board[row][col] == 0:
                        board[row][col] = 2
                        draw_symbol(row, col, 2)

                        if check_win(board, 2):
                            print("AI wins!")
                            game_over = True
                            break
                        elif check_tie(board):
                            print("It's a tie!")
                            game_over = True
                            break

                        current_player = 1

            draw_board(board)
            pygame.display.flip()
            
    main()        

# Call the game function
if __name__ == "__main__":
    game()
