import pygame
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Setup the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Move the Bar!!")

# load game sound
gameOverSound = pygame.mixer.Sound('./Media/gameOverSound.wav')
gameOpenSound = pygame.mixer.Sound('./Media/openingSound.wav')

# Bar settings
BAR_WIDTH = 100
BAR_HEIGHT = 20
barX = WIDTH // 2 - BAR_WIDTH // 2
barY = HEIGHT - BAR_HEIGHT - 10
bar_speed = 10

# Ball settings
BALL_RADIUS = 15
ballX = WIDTH // 2
ballY = HEIGHT // 2
ballSpeedX = 5
ballSpeedY = 5

# Score settings
score = 0
font = pygame.font.SysFont(None, 55)
small_font = pygame.font.SysFont(None, 35)
high_scores_file = "high_scores.txt"

# Timing
clock = pygame.time.Clock()
FPS = 60


def drawText(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


def saveHighScore(name, score):
    if not os.path.exists(high_scores_file):
        with open(high_scores_file, "w") as f:
            f.write("Anonymous 0\n" * 5)
    with open(high_scores_file, "r") as f:
        high_scores = [line.strip() for line in f]
    high_scores.append(f"{name}{score}")
    #high_scores = sorted(high_scores, key=lambda x: int(x.split()[1]), reverse=True)[:5]
    with open(high_scores_file, "w") as f:
        for s in high_scores:
            f.write(f"{s}\n")


def gameOverScreen():
    pygame.mixer.Sound.play(gameOverSound)
    screen.fill(WHITE)
    drawText("Game Over", font, BLACK, screen, WIDTH // 2 - 100, HEIGHT // 2 - 50)
    drawText(f"Score: {score}", font, BLACK, screen, WIDTH // 2 - 100, HEIGHT // 2)
    pygame.display.update()
    pygame.time.wait(2000)

    name = ""
    input_active = True
    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += event.unicode

        screen.fill(WHITE)
        drawText("Enter your name:", font, BLACK, screen, WIDTH // 2 - 150, HEIGHT // 2 - 50)
        drawText(name, font, BLACK, screen, WIDTH // 2 - 150, HEIGHT // 2)
        pygame.display.update()

    saveHighScore(name if name else "Anonymous", score)
    pygame.time.wait(1000)


def showHighScores():
    screen.fill(WHITE)
    drawText("High Scores", font, BLACK, screen, WIDTH // 2 - 100, HEIGHT // 4)
    if os.path.exists(high_scores_file):
        with open(high_scores_file, "r") as f:
            high_scores = [line.strip() for line in f]
        for i, hs in enumerate(high_scores):
            drawText(f"{i + 1}. {hs}", small_font, BLACK, screen, WIDTH // 2 - 100, HEIGHT // 2 + i * 30)
    else:
        drawText("No high scores yet.", small_font, BLACK, screen, WIDTH // 2 - 100, HEIGHT // 2)
    pygame.display.update()
    pygame.time.wait(3000)


def menuScreen():
    screen.fill(WHITE)
    drawText("Main Menu", font, BLACK, screen, WIDTH // 2 - 100, HEIGHT // 4)
    drawText("1. Start Game", small_font, BLACK, screen, WIDTH // 2 - 100, HEIGHT // 2)
    drawText("2. Show High Scores", small_font, BLACK, screen, WIDTH // 2 - 100, HEIGHT // 2 + 40)
    drawText("3. Quit", small_font, BLACK, screen, WIDTH // 2 - 100, HEIGHT // 2 + 80)
    pygame.display.update()


def gameLoop():
    global barX, barY, ballX, ballY, ballSpeedX, ballSpeedY, score
    running = True
    barX = WIDTH // 2 - BAR_WIDTH // 2
    barY = HEIGHT - BAR_HEIGHT - 10
    ballX = WIDTH // 2
    ballY = HEIGHT // 2
    ballSpeedX = 5
    ballSpeedY = 5
    score = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False

        # Get keys
        keys = pygame.key.get_pressed()

        # Bar movement
        if keys[pygame.K_LEFT] and barX > 0:
            barX -= bar_speed
        if keys[pygame.K_RIGHT] and barX < WIDTH - BAR_WIDTH:
            barX += bar_speed

        # Ball movement
        ballX += ballSpeedX
        ballY += ballSpeedY

        # Ball collision with walls
        if ballX - BALL_RADIUS <= 0 or ballX + BALL_RADIUS >= WIDTH:
            ballSpeedX = -ballSpeedX
        if ballY - BALL_RADIUS <= 0:
            ballSpeedY = -ballSpeedY
        if ballY + BALL_RADIUS >= HEIGHT:
            gameOverScreen()
            running = False

        # Ball collision with bar
        if barY <= ballY + BALL_RADIUS <= barY + BAR_HEIGHT and barX <= ballX <= barX + BAR_WIDTH:
            ballSpeedY = -ballSpeedY
            score += 1

        # Draw background
        screen.fill(WHITE)

        # Draw bar
        pygame.draw.rect(screen, BLACK, (barX, barY, BAR_WIDTH, BAR_HEIGHT))

        # Draw ball
        pygame.draw.circle(screen, RED, (ballX, ballY), BALL_RADIUS)

        # Draw score
        drawText(f"Score: {score}", font, BLUE, screen, 10, 10)

        # Update display
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()


def main():
    pygame.mixer.Sound.play(gameOpenSound)
    while True:
        menuScreen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    gameLoop()
                elif event.key == pygame.K_2:
                    showHighScores()
                elif event.key == pygame.K_3:
                    pygame.quit()
                    return


if __name__ == "__main__":
    main()
