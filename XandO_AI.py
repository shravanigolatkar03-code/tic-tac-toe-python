import pygame, sys, random

pygame.init()

SIZE = 600
CELL = SIZE // 3
screen = pygame.display.set_mode((SIZE, SIZE))
pygame.display.set_caption("Tic Tac Toe - AI (FIXED)")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HIGHLIGHT = (255, 255, 150)

font = pygame.font.SysFont(None, 42)

board = [[0]*3 for _ in range(3)]
game_over = False
message = ""
win_line = None

screen.fill(WHITE)

def draw_grid():
    for i in range(1, 3):
        pygame.draw.line(screen, BLACK, (0, i*CELL), (SIZE, i*CELL), 3)
        pygame.draw.line(screen, BLACK, (i*CELL, 0), (i*CELL, SIZE), 3)

def draw_marks():
    for r in range(3):
        for c in range(3):
            x, y = c*CELL, r*CELL
            if board[r][c] == 1:
                pygame.draw.line(screen, BLACK, (x+20,y+20), (x+CELL-20,y+CELL-20), 5)
                pygame.draw.line(screen, BLACK, (x+20,y+CELL-20), (x+CELL-20,y+20), 5)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, BLACK, (x+CELL//2,y+CELL//2), CELL//3, 5)

# ---------- PURE LOGIC (NO DRAWING) ----------
def check_win_logic(p):
    for i in range(3):
        if all(board[i][j] == p for j in range(3)): return True
        if all(board[j][i] == p for j in range(3)): return True
    if all(board[i][i] == p for i in range(3)): return True
    if all(board[i][2-i] == p for i in range(3)): return True
    return False

def get_win_line(p):
    for i in range(3):
        if all(board[i][j] == p for j in range(3)):
            y = i*CELL + CELL//2
            return ((20,y),(SIZE-20,y))
        if all(board[j][i] == p for j in range(3)):
            x = i*CELL + CELL//2
            return ((x,20),(x,SIZE-20))
    if all(board[i][i] == p for i in range(3)):
        return ((20,20),(SIZE-20,SIZE-20))
    if all(board[i][2-i] == p for i in range(3)):
        return ((20,SIZE-20),(SIZE-20,20))
    return None

def board_full():
    return all(cell != 0 for row in board for cell in row)

def draw_win_line():
    if win_line:
        pygame.draw.line(screen, BLACK, win_line[0], win_line[1], 6)

def show_message(text, y):
    label = font.render(text, True, BLACK)
    rect = label.get_rect(center=(SIZE//2, y))
    pygame.draw.rect(screen, HIGHLIGHT, rect.inflate(20,10))
    screen.blit(label, rect)

# ---------- AI ----------
def ai_move():
    for r in range(3):
        for c in range(3):
            if board[r][c] == 0:
                board[r][c] = 2
                if check_win_logic(2):
                    return
                board[r][c] = 0

    for r in range(3):
        for c in range(3):
            if board[r][c] == 0:
                board[r][c] = 1
                if check_win_logic(1):
                    board[r][c] = 2
                    return
                board[r][c] = 0

    empty = [(r,c) for r in range(3) for c in range(3) if board[r][c] == 0]
    if empty:
        r, c = random.choice(empty)
        board[r][c] = 2

def reset():
    global board, game_over, message, win_line
    board = [[0]*3 for _ in range(3)]
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
                board[r][c] = 1
                if check_win_logic(1):
                    win_line = get_win_line(1)
                    message = "You Win!"
                    game_over = True
                elif board_full():
                    message = "It's a Tie!"
                    game_over = True
                else:
                    ai_move()
                    if check_win_logic(2):
                        win_line = get_win_line(2)
                        message = "AI Wins!"
                        game_over = True
                    elif board_full():
                        message = "It's a Tie!"
                        game_over = True

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
