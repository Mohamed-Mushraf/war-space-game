import pygame
import random
import time


# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


# Game settings
FPS = 60
PLAYER_SPEED = 5
ENEMY_SPEED = 2

# Load assets
BACKGROUND_IMAGE = pygame.image.load("assets/background3.jpg")
PLAYER_IMAGE = pygame.image.load("assets/player.png")
ENEMY_IMAGE = pygame.image.load("assets/enemy.png")
BULLET_IMAGE = pygame.image.load("assets/bullet1.png")
EXPLOSION_IMAGE = pygame.image.load("assets/explosion.png")
MUSIC = pygame.mixer.Sound("assets/music1.wav")
BULLET_SOUND = pygame.mixer.Sound("assets/bullet1.wav")
EXPLOSION_SOUND = pygame.mixer.Sound("assets/explosion.wav")

# Game variables
score = 0
done = False
clock = pygame.time.Clock()
game_active = False
game_over = False
replay_cost = 100  # Initial replay cost

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("War Space")

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = PLAYER_IMAGE
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed_x = 0

    def update(self):
        self.speed_x = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.speed_x = -PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.speed_x = PLAYER_SPEED
        self.rect.x += self.speed_x
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        BULLET_SOUND.play()

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = ENEMY_IMAGE
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed_y = ENEMY_SPEED + random.uniform(-1, 1)

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.y = random.randint(-100, -40)
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
            global score
            score -= 1

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = BULLET_IMAGE
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed_y = -10

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0:
            self.kill()

# Explosion class
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.image = EXPLOSION_IMAGE
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.kill()

# Button class
class Button:
    def __init__(self, text, pos, font, bg_color=BLUE, text_color=WHITE):
        self.x, self.y = pos
        self.font = pygame.font.Font(None, font)
        self.bg_color = bg_color
        self.text_color = text_color
        self.change_text(text)

    def change_text(self, text):
        self.text = self.font.render(text, True, self.text_color)
        self.size = self.text.get_size()
        self.surface = pygame.Surface((self.size[0] + 20, self.size[1] + 20))
        self.surface.fill(self.bg_color)
        self.surface.blit(self.text, (10, 10))
        self.rect = self.surface.get_rect(center=(self.x, self.y))

    def show(self, screen):
        screen.blit(self.surface, self.rect.topleft)

    def click(self, event):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.rect.collidepoint(x, y):
                    return True
        return False

# Sprite groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

def start_game():
    global all_sprites, enemies, bullets, player, score, game_over, game_active, replay_cost
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    player = Player()
    all_sprites.add(player)
    for i in range(8):
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)
    score = 0
    replay_cost = 100
    game_over = False
    game_active = True

# Play background music
MUSIC.play(-1)

# Create the "Play" button and welcome message
play_button = Button("Play", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), font=74)
restart_button = Button("Restart", (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2), font=50)
quit_button = Button("Quit", (3 * SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2), font=50)
welcome_text = "Welcome to War Space!"
# Add button areas
left_button = pygame.Rect(50, SCREEN_HEIGHT - 100, 100, 50)
right_button = pygame.Rect(200, SCREEN_HEIGHT - 100, 100, 50)
fire_button = pygame.Rect(SCREEN_WIDTH - 150, SCREEN_HEIGHT - 100, 100, 50)

# Draw buttons function (updated for transparent buttons)
def draw_buttons():
    font = pygame.font.Font(None, 36)
    left_text = font.render("Left", True, WHITE)
    right_text = font.render("Right", True, WHITE)
    fire_text = font.render("Fire", True, WHITE)

    # Render text directly onto the screen at the button locations
    screen.blit(left_text, (left_button.x + 25, left_button.y + 10))
    screen.blit(right_text, (right_button.x + 20, right_button.y + 10))
    screen.blit(fire_text, (fire_button.x + 20, fire_button.y + 10))


# Speed increment for button-based movement
BUTTON_MOVEMENT_SPEED = 35  # Increased speed for button clicks

# Game loop (modified)
while not done:
    screen.fill(BLACK)
    screen.blit(BACKGROUND_IMAGE, (0, 0))

    if not game_active and not game_over:
        font = pygame.font.Font(None, 74)
        text = font.render(welcome_text, True, WHITE)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() - 100))
        play_button.show(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.click(event):
                    start_game()
    elif game_over:
        if score >= replay_cost:
            restart_button.show(screen)
            quit_button.show(screen)
            font = pygame.font.Font(None, 36)
            text = font.render(f"Use {replay_cost} score points to replay?", True, WHITE)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_button.click(event):
                        score -= replay_cost
                        replay_cost += 100
                        start_game()
                    elif quit_button.click(event):
                        done = True
        else:
            font = pygame.font.Font(None, 36)
            text = font.render("Not enough score for replay. Exiting in 5 seconds.", True, RED)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
            pygame.display.flip()
            time.sleep(5)
            # Transition back to home screen
            game_active = False
            game_over = False
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if left_button.collidepoint(event.pos):
                    player.rect.x -= BUTTON_MOVEMENT_SPEED
                elif right_button.collidepoint(event.pos):
                    player.rect.x += BUTTON_MOVEMENT_SPEED
                elif fire_button.collidepoint(event.pos):
                    player.shoot()

        all_sprites.update()
        hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
        for hit in hits:
            score += 1
            explosion = Explosion(hit.rect.center)
            all_sprites.add(explosion)
            EXPLOSION_SOUND.play()
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)

        hits = pygame.sprite.spritecollide(player, enemies, True)
        if hits:
            game_over = True

        all_sprites.draw(screen)
        font = pygame.font.Font(None, 36)
        text = font.render("Score: " + str(score), True, WHITE)
        screen.blit(text, (10, 10))

        draw_buttons()  # Draw buttons

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
