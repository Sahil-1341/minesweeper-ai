import pygame
import sys

from minesweeper import Minesweeper, MinesweeperAI

# ======================
# GAME CONFIGURATION
# ======================
HEIGHT = 4
WIDTH = 4
MINES = 2

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
BOARD_PADDING = 20

# Colors
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
WHITE = (255, 255, 255)

# ======================
# INITIALIZE GAME
# ======================
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Minesweeper AI")

clock = pygame.time.Clock()

# ======================
# LOAD FONTS
# ======================
OPEN_SANS = "assets/fonts/OpenSans-Regular.ttf"

try:
    smallFont = pygame.font.Font(OPEN_SANS, 20)
    mediumFont = pygame.font.Font(OPEN_SANS, 28)
    largeFont = pygame.font.Font(OPEN_SANS, 40)
except:
    smallFont = pygame.font.SysFont(None, 20)
    mediumFont = pygame.font.SysFont(None, 28)
    largeFont = pygame.font.SysFont(None, 40)

# ======================
# BOARD CALCULATION
# ======================
board_width = ((2 / 3) * SCREEN_WIDTH) - (BOARD_PADDING * 2)
board_height = SCREEN_HEIGHT - (BOARD_PADDING * 2)
cell_size = int(min(board_width / WIDTH, board_height / HEIGHT))
board_origin = (BOARD_PADDING, BOARD_PADDING)

# ======================
# LOAD IMAGES
# ======================
flag = pygame.image.load("assets/images/flag.png")
flag = pygame.transform.scale(flag, (cell_size, cell_size))

mine = pygame.image.load("assets/images/mine.png")
mine = pygame.transform.scale(mine, (cell_size, cell_size))

# ======================
# CREATE GAME & AI
# ======================
game = Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)
ai = MinesweeperAI(height=HEIGHT, width=WIDTH)

revealed = set()
flags = set()
lost = False
instructions = True

CLICK_DELAY = 200
last_click_time = 0

# ======================
# MAIN LOOP
# ======================
while True:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(BLACK)

    # ======================
    # INSTRUCTIONS SCREEN
    # ======================
    if instructions:
        title = largeFont.render("Play Minesweeper", True, WHITE)
        screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 50)))

        rules = [
            "Left click to reveal a cell",
            "Right click to flag a mine",
            "Mark all mines to win"
        ]

        for i, rule in enumerate(rules):
            text = smallFont.render(rule, True, WHITE)
            screen.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, 150 + i * 30)))

        play_button = pygame.Rect(
            SCREEN_WIDTH // 4, SCREEN_HEIGHT * 3 // 4,
            SCREEN_WIDTH // 2, 50
        )
        pygame.draw.rect(screen, WHITE, play_button)

        button_text = mediumFont.render("Play Game", True, BLACK)
        screen.blit(button_text, button_text.get_rect(center=play_button.center))

        if pygame.mouse.get_pressed()[0]:
            if play_button.collidepoint(pygame.mouse.get_pos()):
                instructions = False

        pygame.display.flip()
        continue

    # ======================
    # DRAW BOARD
    # ======================
    cells = []
    for i in range(HEIGHT):
        row = []
        for j in range(WIDTH):
            rect = pygame.Rect(
                board_origin[0] + j * cell_size,
                board_origin[1] + i * cell_size,
                cell_size,
                cell_size
            )

            pygame.draw.rect(screen, GRAY, rect)
            pygame.draw.rect(screen, WHITE, rect, 2)

            if (i, j) in flags:
                screen.blit(flag, rect)
            elif (i, j) in revealed:
                count = game.nearby_mines((i, j))
                text = smallFont.render(str(count), True, BLACK)
                screen.blit(text, text.get_rect(center=rect.center))
            elif lost and game.is_mine((i, j)):
                screen.blit(mine, rect)

            row.append(rect)
        cells.append(row)

    # ======================
    # BUTTONS
    # ======================
    ai_button = pygame.Rect(
        (2 / 3) * SCREEN_WIDTH + BOARD_PADDING,
        SCREEN_HEIGHT // 3 - 50,
        SCREEN_WIDTH // 3 - BOARD_PADDING * 2,
        50
    )
    pygame.draw.rect(screen, WHITE, ai_button)
    screen.blit(
        mediumFont.render("AI Move", True, BLACK),
        mediumFont.render("AI Move", True, BLACK).get_rect(center=ai_button.center)
    )

    reset_button = pygame.Rect(
        (2 / 3) * SCREEN_WIDTH + BOARD_PADDING,
        SCREEN_HEIGHT // 3 + 20,
        SCREEN_WIDTH // 3 - BOARD_PADDING * 2,
        50
    )
    pygame.draw.rect(screen, WHITE, reset_button)
    screen.blit(
        mediumFont.render("Reset", True, BLACK),
        mediumFont.render("Reset", True, BLACK).get_rect(center=reset_button.center)
    )

    # ======================
    # GAME STATUS
    # ======================
    status = "Lost" if lost else "Won" if game.won() else ""
    status_text = mediumFont.render(status, True, WHITE)
    screen.blit(
        status_text,
        status_text.get_rect(center=((5 / 6) * SCREEN_WIDTH, (2 / 3) * SCREEN_HEIGHT))
    )

    # ======================
    # MOUSE HANDLING
    # ======================
    current_time = pygame.time.get_ticks()
    if current_time - last_click_time > CLICK_DELAY:

        left, _, right = pygame.mouse.get_pressed()
        mouse = pygame.mouse.get_pos()

        # RIGHT CLICK → FLAG
        if right and not lost:
            for i in range(HEIGHT):
                for j in range(WIDTH):
                    if cells[i][j].collidepoint(mouse) and (i, j) not in revealed:
                        if (i, j) in flags:
                            flags.remove((i, j))
                            game.mines_found.discard((i, j))
                        else:
                            flags.add((i, j))
                            game.mines_found.add((i, j))
                        last_click_time = current_time

        # LEFT CLICK
        if left:
            # AI MOVE
            if ai_button.collidepoint(mouse) and not lost:
                move = ai.make_safe_move() or ai.make_random_move()
                if move:
                    if game.is_mine(move):
                        lost = True
                    else:
                        revealed.add(move)
                        ai.add_knowledge(move, game.nearby_mines(move))
                last_click_time = current_time

            # RESET
            elif reset_button.collidepoint(mouse):
                game = Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)
                ai = MinesweeperAI(height=HEIGHT, width=WIDTH)
                revealed.clear()
                flags.clear()
                lost = False
                last_click_time = current_time

            # USER MOVE
            elif not lost:
                for i in range(HEIGHT):
                    for j in range(WIDTH):
                        if (cells[i][j].collidepoint(mouse)
                                and (i, j) not in flags
                                and (i, j) not in revealed):
                            if game.is_mine((i, j)):
                                lost = True
                            else:
                                revealed.add((i, j))
                                ai.add_knowledge((i, j), game.nearby_mines((i, j)))
                            last_click_time = current_time

    pygame.display.flip()