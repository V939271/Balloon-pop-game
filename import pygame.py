import pygame
import random
import sys
# Initialize Pygame
pygame.init()
# Game constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
TIMER = 120  # 2 minutes in seconds
BALLOON_SPEED = 0.7
POP_REWARD = 2
MISS_PENALTY = 1
BALLOON_SPAWN_DELAY = 1000  # Delay in milliseconds between balloon spawns
# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Balloon Pop Challenge")
# Fonts
font = pygame.font.Font(None, 36)
# Timer
timer = TIMER * 1000  # Convert to milliseconds
pygame.time.set_timer(pygame.USEREVENT, 1000)  # Timer event every second
# Balloon class
class Balloon(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 70), pygame.SRCALPHA)  # Oval shape with alpha channel
        pygame.draw.ellipse(self.image, RED, [0, 0, 50, 70])  # Draw oval balloon
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = SCREEN_HEIGHT
    def update(self):
        self.rect.y -= BALLOON_SPEED
        if self.rect.y < -self.rect.height:  # Remove balloon if it goes off-screen
            self.kill()
# Balloon group
balloons = pygame.sprite.Group()
# Game variables
score = 0
next_balloon_spawn_time = pygame.time.get_ticks() + BALLOON_SPAWN_DELAY  # Initial spawn time
# Game loop
running = True
while running:
    current_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.USEREVENT:
            timer -= 1000
            if timer <= 0:
                running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                for balloon in balloons:
                    if balloon.rect.collidepoint(event.pos):
                        balloon.kill()
                        score += POP_REWARD
    screen.fill(WHITE)
    # Spawn balloons with a delay
    if current_time >= next_balloon_spawn_time:
        new_balloon = Balloon()
        balloons.add(new_balloon)
        next_balloon_spawn_time = current_time + BALLOON_SPAWN_DELAY
    # Update and draw balloons
    balloons.update()
    balloons.draw(screen)
    # Draw score
    score_text = font.render(f"Score: {score}", True, RED)
    screen.blit(score_text, (10, 10))
    # Draw timer
    timer_text = font.render(f"Time: {timer // 1000}", True, RED)
    screen.blit(timer_text, (SCREEN_WIDTH - 150, 10))
    pygame.display.flip()
pygame.quit()
sys.exit()