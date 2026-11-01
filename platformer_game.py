import pygame
import sys

pygame.init()

# Ukuran layar
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Platformer Game")

# Warna
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)

# Font
font = pygame.font.SysFont(None, 36)

# Variabel pemain
player_width = 50
player_height = 50
player_x = 100
player_y = SCREEN_HEIGHT - player_height - 100
player_velocity_y = 0
jump = False
gravity = 1
player_speed = 5

# Musuh
enemy_width = 40
enemy_height = 40
enemy_speed = 2

# Status game
score = 0
lives = 3
level = 1
current_level = 0
game_over = False
game_start = False
game_won = False

# Invincibility (kebal sesaat)
invincible = False
invincible_timer = 0
INVINCIBLE_DURATION = 60

# Platform dan koin per level
level1 = {
    "platforms": [
        pygame.Rect(0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40),
        pygame.Rect(200, SCREEN_HEIGHT - 100, 100, 20),
        pygame.Rect(400, SCREEN_HEIGHT - 180, 100, 20),
        pygame.Rect(600, SCREEN_HEIGHT - 260, 100, 20)
    ],
    "coins": [
        pygame.Rect(210, SCREEN_HEIGHT - 130, 20, 20),
        pygame.Rect(410, SCREEN_HEIGHT - 210, 20, 20),
        pygame.Rect(610, SCREEN_HEIGHT - 290, 20, 20)
    ],
    "enemy": pygame.Rect(500, SCREEN_HEIGHT - 80, enemy_width, enemy_height)
}

level2 = {
    "platforms": [
        pygame.Rect(0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40),
        pygame.Rect(100, SCREEN_HEIGHT - 100, 120, 20),
        pygame.Rect(300, SCREEN_HEIGHT - 180, 120, 20),
        pygame.Rect(500, SCREEN_HEIGHT - 260, 120, 20),
        pygame.Rect(700, SCREEN_HEIGHT - 340, 80, 20)
    ],
    "coins": [
        pygame.Rect(110, SCREEN_HEIGHT - 130, 20, 20),
        pygame.Rect(310, SCREEN_HEIGHT - 210, 20, 20),
        pygame.Rect(510, SCREEN_HEIGHT - 290, 20, 20),
        pygame.Rect(710, SCREEN_HEIGHT - 370, 20, 20)
    ],
    "enemy": pygame.Rect(300, SCREEN_HEIGHT - 80, enemy_width, enemy_height)
}

level3 = {
    "platforms": [
        pygame.Rect(0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40),
        pygame.Rect(200, SCREEN_HEIGHT - 120, 100, 20),
        pygame.Rect(400, SCREEN_HEIGHT - 200, 100, 20),
        pygame.Rect(600, SCREEN_HEIGHT - 280, 100, 20),
        pygame.Rect(300, SCREEN_HEIGHT - 360, 100, 20),
        pygame.Rect(100, SCREEN_HEIGHT - 440, 100, 20),
    ],
    "coins": [
        pygame.Rect(210, SCREEN_HEIGHT - 150, 20, 20),
        pygame.Rect(410, SCREEN_HEIGHT - 230, 20, 20),
        pygame.Rect(610, SCREEN_HEIGHT - 310, 20, 20),
        pygame.Rect(310, SCREEN_HEIGHT - 390, 20, 20),
        pygame.Rect(110, SCREEN_HEIGHT - 470, 20, 20),
    ],
    "enemy": pygame.Rect(500, SCREEN_HEIGHT - 80, enemy_width, enemy_height)
}

level4 = {
    "platforms": [
        pygame.Rect(0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40),
        pygame.Rect(150, SCREEN_HEIGHT - 100, 500, 20)
    ],
    "coins": [],
    "enemy": pygame.Rect(350, SCREEN_HEIGHT - 130, 100, 100),
    "boss": True,
    "boss_health": 3
}

levels = [level1, level2, level3, level4]

# Reset level
def reset_level(index):
    global player_x, player_y, player_velocity_y, jump
    global current_level, invincible, invincible_timer
    player_x = 100
    player_y = SCREEN_HEIGHT - player_height - 100
    player_velocity_y = 0
    jump = False
    current_level = index
    invincible = False
    invincible_timer = 0
    if "boss_health" in levels[current_level]:
        levels[current_level]["boss_health"] = 3

# Tombol
def draw_text(text, size, color, x, y, center=True):
    font_obj = pygame.font.SysFont(None, size)
    text_surface = font_obj.render(text, True, color)
    text_rect = text_surface.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)

# Game loop
clock = pygame.time.Clock()

while True:
    screen.fill(BLACK)

    if not game_start:
        draw_text("Tekan [SPACE] untuk Memulai", 48, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_start = True
        continue

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
    if keys[pygame.K_SPACE] and not jump:
        player_velocity_y = -15
        jump = True

    # Update gravitasi
    player_velocity_y += gravity
    player_y += player_velocity_y

    # Cek platform
    platforms = levels[current_level]["platforms"]
    for plat in platforms:
        if pygame.Rect(player_x, player_y, player_width, player_height).colliderect(plat) and player_velocity_y >= 0:
            player_y = plat.top - player_height
            player_velocity_y = 0
            jump = False

    # Update musuh
    enemy = levels[current_level]["enemy"]
    if "boss" not in levels[current_level]:
        enemy.x += enemy_speed
        if enemy.left < 0 or enemy.right > SCREEN_WIDTH:
            enemy_speed *= -1

    # Cek tabrakan dengan musuh
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    if player_rect.colliderect(enemy) and not invincible:
        if "boss" in levels[current_level]:
            levels[current_level]["boss_health"] -= 1
            if levels[current_level]["boss_health"] <= 0:
                game_won = True
                game_over = True
        else:
            lives -= 1
        invincible = True
        invincible_timer = 0
        player_x = 100
        player_y = SCREEN_HEIGHT - player_height - 100
        player_velocity_y = 0

    if invincible:
        invincible_timer += 1
        if invincible_timer >= INVINCIBLE_DURATION:
            invincible = False
            invincible_timer = 0

    # Ambil koin
    coins = levels[current_level]["coins"]
    for coin in coins[:]:
        if player_rect.colliderect(coin):
            coins.remove(coin)
            score += 10

    # Lanjut level
    if not coins and "boss" not in levels[current_level]:
        current_level += 1
        if current_level >= len(levels):
            game_won = True
            game_over = True
        else:
            reset_level(current_level)

    # Game over
    if lives <= 0:
        game_over = True

    # Gambar semua elemen
    for plat in platforms:
        pygame.draw.rect(screen, GREEN, plat)

    for coin in coins:
        pygame.draw.rect(screen, YELLOW, coin)

    if not invincible or (invincible_timer % 10 < 5):
        pygame.draw.rect(screen, BLUE, (player_x, player_y, player_width, player_height))

    pygame.draw.rect(screen, RED if "boss" not in levels[current_level] else PURPLE, enemy)

    draw_text(f"Skor: {score}", 30, WHITE, 10, 10, center=False)
    draw_text(f"Nyawa: {lives}", 30, WHITE, 10, 40, center=False)
    draw_text(f"Level: {current_level + 1}", 30, WHITE, 10, 70, center=False)

    if "boss" in levels[current_level]:
        draw_text(f"Boss HP: {levels[current_level]['boss_health']}", 30, RED, SCREEN_WIDTH - 200, 10, center=False)

    # Game over screen
    if game_over:
        if game_won:
            draw_text("Selamat! Kamu menyelesaikan semua level!", 40, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30)
        else:
            draw_text("Game Over!", 48, RED, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30)
        draw_text("Tekan R untuk mengulang", 36, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            score = 0
            lives = 3
            current_level = 0
            game_over = False
            game_won = False
            reset_level(0)

    pygame.display.flip()
    clock.tick(60)
