import pygame, sys, time

# Initialize Pygame
pygame.init()

# the constants (no pun intended)
WIDTH, HEIGHT = 600, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRID_SIZE = 11  # 11x11 grid
CELL_SIZE = WIDTH // GRID_SIZE
FONT = pygame.font.Font(None, 40)

# Colors for the moving square
COLORS = [
    (255, 0, 0), (0, 255, 0), (0, 0, 255),
    (255, 255, 0), (255, 0, 255), (0, 255, 255)
]

# Helper functions
def draw_grid(screen):
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, BLACK, (x, 0), (x, HEIGHT), 2 if x % (CELL_SIZE * 3) == 0 else 1)
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, BLACK, (0, y), (WIDTH, y), 2 if y % (CELL_SIZE * 3) == 0 else 1)

def draw_numbers(screen, board):
    for y in range(1, GRID_SIZE - 1):
        for x in range(1, GRID_SIZE - 1):
            if board[y][x] != 0:
                text = FONT.render(str(board[y][x]), True, BLACK)
                screen.blit(text, (x * CELL_SIZE + 20, y * CELL_SIZE + 15))

def is_valid(board, num, pos):
    for i in range(1, GRID_SIZE - 1):
        if board[pos[0]][i] == num and pos[1] != i:
            return False
    for i in range(1, GRID_SIZE - 1):
        if board[i][pos[1]] == num and pos[0] != i:
            return False
    box_x = (pos[1] - 1) // 3
    box_y = (pos[0] - 1) // 3
    for i in range(box_y * 3 + 1, box_y * 3 + 4):
        for j in range(box_x * 3 + 1, box_x * 3 + 4):
            if board[i][j] == num and (i, j) != pos:
                return False
    return True

def find_empty(board):
    for i in range(1, GRID_SIZE - 1):
        for j in range(1, GRID_SIZE - 1):
            if board[i][j] == 0:
                return (i, j)
    return None

def solve(board):
    find = find_empty(board)
    if not find:
        return True
    else:
        row, col = find
    for i in range(1, 10):
        if is_valid(board, i, (row, col)):
            board[row][col] = i
            if solve(board):
                return True
            board[row][col] = 0
    return False

# Initialize the board (9x9 Sudoku with a border)
board = [
    [0] * GRID_SIZE,
    [0, 5, 3, 0, 0, 7, 0, 0, 0, 0, 0],
    [0, 6, 0, 0, 1, 9, 5, 0, 0, 0, 0, 0],
    [0, 0, 9, 8, 0, 0, 0, 6, 0, 0, 0, 0],
    [0, 8, 0, 0, 0, 6, 0, 0, 0, 3, 0, 0],
    [0, 4, 0, 0, 8, 0, 3, 0, 0, 1, 0, 0],
    [0, 7, 0, 0, 0, 2, 0, 0, 0, 6, 0, 0],
    [0, 0, 6, 0, 0, 0, 2, 8, 0, 0, 0, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5, 0, 0, 0],
    [0, 0, 0, 0, 8, 0, 0, 7, 9, 0, 0, 0],
    [0] * GRID_SIZE
]

# Main function
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sudoku")

    running = True
    selected = None
    key = None

    square_pos = [1, 1]
    color_index = 0
    color_change_time = time.time()
    color_change_interval = 0.5  # Change color every 0.5 seconds

    # Directions for moving around the border (right, down, left, up)
    # Didn't work as expected so didn't use it
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    current_direction = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                selected = (pos[1] // CELL_SIZE, pos[0] // CELL_SIZE)
                if selected[0] == 0 or selected[0] == GRID_SIZE - 1 or selected[1] == 0 or selected[1] == GRID_SIZE - 1:
                    selected = None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_DELETE:
                    if selected:
                        board[selected[0]][selected[1]] = 0
                if event.key == pygame.K_RETURN:
                    solve(board)
                if event.key == pygame.K_BACKSPACE:
                    if selected:
                        board[selected[0]][selected[1]] = 0

        if selected and key:
            if 1 <= selected[0] < GRID_SIZE - 1 and 1 <= selected[1] < GRID_SIZE - 1:
                board[selected[0]][selected[1]] = key
            key = None

        # Updates the color and position of the moving square
        if time.time() - color_change_time > color_change_interval:
            color_index = (color_index + 1) % len(COLORS)
            square_pos[1] += 1
            if square_pos[1] >= GRID_SIZE - 1:
                square_pos[1] = 1
                square_pos[0] += 1
                if square_pos[0] >= GRID_SIZE - 1:
                    square_pos[0] = 1
            color_change_time = time.time()

        screen.fill(WHITE)
        draw_grid(screen)
        draw_numbers(screen, board)

        # Draw the moving square
        pygame.draw.rect(screen, COLORS[color_index], (square_pos[1] * CELL_SIZE, square_pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
