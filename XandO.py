import pygame, sys

pygame.init()

SIZE = 600
CELL = SIZE // 3
screen = pygame.display.set_mode((SIZE, SIZE))
pygame.display.set_caption("Tic Tac Toe")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HIGHLIGHT = (255, 255, 150)   # highlighter yellow
LINE_COLOR = (50, 50, 50)

font = pygame.font.SysFont(None, 42)

board = [[0]*3 for _ in range(3)]
player = 1
game_over = False
message = ""
win_line = None

screen.fill(WHITE)

def draw_grid():
    for i in range(1, 3):
        pygame.draw.line(screen, LINE_COLOR, (0, i*CELL), (SIZE, i*CELL), 3)
        pygame.draw.line(screen, LINE_COLOR, (i*CELL, 0), (i*CELL, SIZE), 3)

def draw_marks():
    for r in range(3):
        for c in range(3):
            x, y = c*CELL, r*CELL
            if board[r][c] == 1:
                pygame.draw.line(screen, BLACK, (x+20,y+20), (x+CELL-20,y+CELL-20), 5)
                pygame.draw.line(screen, BLACK, (x+20,y+CELL-20), (x+CELL-20,y+20), 5)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, BLACK, (x+CELL//2,y+CELL//2), CELL//3, 5)

def check_win(p):
    global win_line

    for i in range(3):
        if all(board[i][j] == p for j in range(3)):
            y = i*CELL + CELL//2
            win_line = ((20,y),(SIZE-20,y))
            return True

        if all(board[j][i] == p for j in range(3)):
            x = i*CELL + CELL//2
            win_line = ((x,20),(x,SIZE-20))
            return True

    if all(board[i][i] == p for i in range(3)):
        win_line = ((20,20),(SIZE-20,SIZE-20))
        return True

    if all(board[i][2-i] == p for i in range(3)):
        win_line = ((20,SIZE-20),(SIZE-20,20))
        return True

    return False

def board_full():
    return all(cell != 0 for row in board for cell in row)

def draw_win_line():
    if win_line:
        pygame.draw.line(screen, BLACK, win_line[0], win_line[1], 6)

def show_message(text, y_pos):
    label = font.render(text, True, BLACK)
    box = label.get_rect(center=(SIZE//2, y_pos))
    pygame.draw.rect(screen, HIGHLIGHT, box.inflate(20, 10))
    screen.blit(label, box)

def reset():
    global board, player, game_over, message, win_line
    board = [[0]*3 for _ in range(3)]
    player = 1
    game_over = False
    message = ""
    win_line = None
    screen.fill(WHITE)
    draw_grid()

draw_grid()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mx, my = event.pos
            r, c = my//CELL, mx//CELL
            if board[r][c] == 0:
                board[r][c] = player
                if check_win(player):
                    message = "X Wins!" if player == 1 else "O Wins!"
                    game_over = True
                elif board_full():
                    message = "It's a Tie!"
                    game_over = True
                else:
                    player = 2 if player == 1 else 1

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset()
            if event.key == pygame.K_q:
                pygame.quit()
                sys.exit()

    draw_marks()
    draw_win_line()

    if game_over:
        show_message(message, SIZE//2 - 20)
        show_message("R = Restart   Q = Quit", SIZE//2 + 30)

    pygame.display.update()
