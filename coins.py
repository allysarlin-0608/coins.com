import pygame
import random

# 1. Initialize Pygame
pygame.init()

# Game Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BAG_WIDTH = 100
BAG_HEIGHT = 60
FPS = 60

# Colors (R, G, B)
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)
COPPER = (184, 115, 51)
BLACK = (0, 0, 0)

# Setup Screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Coin Catcher")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 32)

# Coin Types: (Color, Value, Speed)
COIN_TYPES = [
    (GOLD, 10, 7),
    (SILVER, 5, 5),
    (COPPER, 1, 3)
]

# Game Variables
bag_x = (SCREEN_WIDTH - BAG_WIDTH) // 2
bag_y = SCREEN_HEIGHT - BAG_HEIGHT - 10
score = 0
coins = [] # List to store active coins

def spawn_coin():
    color, value, speed = random.choice(COIN_TYPES)
    x_pos = random.randint(20, SCREEN_WIDTH - 20)
    return {"rect": pygame.Rect(x_pos, -20, 20, 20), "color": color, "value": value, "speed": speed}

# Main Game Loop
running = True
while running:
    screen.fill(BLACK)
    
    # 2. Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 3. Movement Logic
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and bag_x > 0:
        bag_x -= 8
    if keys[pygame.K_RIGHT] and bag_x < SCREEN_WIDTH - BAG_WIDTH:
        bag_x += 8

    # 4. Coin Logic (Spawn & Move)
    if random.randint(1, 30) == 1: # Randomly spawn coins
        coins.append(spawn_coin())

    bag_rect = pygame.Rect(bag_x, bag_y, BAG_WIDTH, BAG_HEIGHT)

    for coin in coins[:]:
        coin["rect"].y += coin["speed"]
        
        # Check Collision
        if bag_rect.colliderect(coin["rect"]):
            score += coin["value"]
            coins.remove(coin)
        # Remove if off-screen
        elif coin["rect"].y > SCREEN_HEIGHT:
            coins.remove(coin)

    # 5. Drawing
    # Draw Bag
    pygame.draw.rect(screen, (100, 50, 0), bag_rect) 
    
    # Draw Coins
    for coin in coins:
        pygame.draw.circle(screen, coin["color"], coin["rect"].center, 10)

    # Draw Score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
