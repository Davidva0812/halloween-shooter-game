import random
import sys
from settings_and_ui import *


# States
MENU_STATE = "menu_state"
GAME_STATE = "game_state"
GAME_OVER_STATE = "game_over_state"
CONFIRM_EXIT_STATE = "confirm_exit_state"
game_status = MENU_STATE
previous_game_state = None
yes_button_rect = None
no_button_rect = None

# Sprite groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, name, images, x, y, hp, speed):
        super().__init__()
        self.name  = name
        self.images = images
        self.image_index = 0
        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.hp = hp
        self.speed = speed
        self.frame_counter = 0

    def update(self):
        global game_status, game_end_time
        self.rect.y += float(self.speed)
        self.frame_counter += 1
        if self.frame_counter >= 10:  # switch image in every 10 frame
            self.frame_counter = 0
            self.image_index = (self.image_index + 1) % len(self.images)
            self.image = self.images[self.image_index]
        if self.rect.y > HEIGHT:
            self.kill()
            game_status = GAME_OVER_STATE
            game_end_time = pygame.time.get_ticks()

    def take_damage(self):
        self.hp -= 1
        if self.hp <= 0:
            self.kill()
            return True  #If died, return True
        return False  #If not dead, return False


def spawn_enemy():
    available_enemies = ["Bat", "Zombie", "Skeleton"]
    if score >= 100:
        available_enemies.append("Wraith")
    if score >= 200:
        available_enemies.append("Jack")

    enemy_type = random.choice(available_enemies)
    x_pos = random.randint(50, WIDTH - 100)

    if enemy_type == "Bat":
        opponent = Enemy("Bat", bat_surf, x_pos, -50, 1, 4)
    elif enemy_type == "Skeleton":
        opponent = Enemy("Skeleton", skeleton_surf, x_pos, -50, 2, 2.5)
    elif enemy_type == "Zombie":
        opponent = Enemy("Zombie", zombie_surf, x_pos, -50, 3, 2)
    elif enemy_type == "Wraith":
        opponent = Enemy("Wraith", wraith_surf, x_pos, -50, 2, 3.5)
    elif enemy_type == "Jack":
        opponent = Enemy("Jack", jack_surf, x_pos, -50, 4, 3)

    all_sprites.add(opponent)
    enemies.add(opponent)


def toggle_mute():
    global mute
    mute = not mute
    if mute:
        pygame.mixer.music.set_volume(0)  # Mute music
    else:
        pygame.mixer.music.set_volume(0.5)


score = 0
game_start_time = 0
game_end_time = 0
mute = False
bat_index, zombie_index, skeleton_index, wraith_index, jack_index = 0, 0, 0, 0, 0

# Spawner event configuration
ENEMY_SPAWN_EVENT = pygame.USEREVENT + 1
enemy_spawn_interval = 2000
pygame.time.set_timer(ENEMY_SPAWN_EVENT, enemy_spawn_interval)  # Enemy in every 2 mp


# Load the highest score
def load_highscore():
    global highscore
    try:
        with open("highscore.txt", "r") as file:
            highscore = int(file.read())  # Read and convert to integer
    except (FileNotFoundError, ValueError):
        highscore = 0
    return highscore


# Refresh the highest score
def save_highscore():
    global highscore
    highscore = load_highscore()  # Reads the actual highest score
    if score > highscore:  # If actual score is higher:
        with open("highscore.txt", "w") as file:
            file.write(str(score))  #
        highscore = score
    return highscore


def draw_button(text, x, y, width, height):
    """Draws buttons and checks clicking"""
    mouse_x, mouse_y = pygame.mouse.get_pos()
    button_rect = pygame.Rect(x, y, width, height)
    # If the mouse is over it, a faint overlay effect (e.g., darker overlay)
    # pygame.SRCALPHA: supports the hover effect
    if button_rect.collidepoint(mouse_x, mouse_y):
        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 50))  #darker overlay
        screen.blit(overlay, (x, y))
    # Text in the middle
    text_surface = exit_font.render(text, True, RED)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)
    return button_rect


# Main loop of the game
running = True
while running:
    highscore = save_highscore()
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            previous_game_state = game_status
            game_status = CONFIRM_EXIT_STATE
        if game_status != CONFIRM_EXIT_STATE:
            yes_button_rect = None
            no_button_rect = None
        if event.type == pygame.MOUSEMOTION:
            crosshair_rect = crosshair_surf.get_rect(center=event.pos)
        if event.type == pygame.KEYDOWN and game_status == MENU_STATE:
            if event.key == pygame.K_SPACE:
                game_status = GAME_STATE
                game_start_time = pygame.time.get_ticks()
                score = 0
        if event.type == ENEMY_SPAWN_EVENT and game_status == GAME_STATE:
            spawn_enemy()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = event.pos
            if mute_rect.collidepoint(mouse_x, mouse_y):
                toggle_mute()
            elif unmute_rect.collidepoint(mouse_x, mouse_y):
                toggle_mute()
            if yes_button_rect and yes_button_rect.collidepoint(mouse_x,mouse_y):
                running = False
            elif no_button_rect and no_button_rect.collidepoint(mouse_x,mouse_y):
                if previous_game_state is not None:
                    game_status = previous_game_state
            for enemy in enemies:
                if enemy.rect.collidepoint(mouse_x, mouse_y):
                    if enemy.take_damage():  # If True, enemy is dead
                        if enemy.name == "Jack":
                            score += 30
                        else:
                            score += 10
                        enemies.remove(enemy)
                        all_sprites.remove(enemy)

    if game_status == MENU_STATE:
        screen.blit(bg_img, (0, 0))
        screen.blit(title_surf, title_rect)
        screen.blit(press_space_surf, press_space_rect)
        if mute:
            screen.blit(mute_img, mute_rect)
        else:
            screen.blit(unmute_img, unmute_rect)
        screen.blit(crosshair_surf, crosshair_rect)
        bat_index += 1
        zombie_index += 1
        wraith_index += 1
        skeleton_index += 1
        jack_index += 1
        if bat_index > len(bat_surf) - 1:
            bat_index = 0
        if zombie_index > len(zombie_surf) - 1:
            zombie_index = 0
        if wraith_index > len(wraith_surf) - 1:
            wraith_index = 0
        if skeleton_index > len(skeleton_surf) - 1:
            skeleton_index = 0
        if jack_index > len(jack_surf) - 1:
            jack_index = 0

    elif game_status == GAME_STATE:
        screen.blit(cemetery_bg, (0, 0))
        all_sprites.update()
        all_sprites.draw(screen)

        # Count elapsed time in (mp)
        elapsed_time = (pygame.time.get_ticks() - game_start_time) // 1000  # ms -> s
        new_interval = enemy_spawn_interval
        # Control spawn system based on elapsed time
        if elapsed_time >= 60:
            new_interval = 700
        elif elapsed_time >= 30:
            new_interval = 1000
        elif elapsed_time >= 10:
            new_interval = 1500
        elif elapsed_time >= 5:
            new_interval = 2000

        if new_interval != enemy_spawn_interval:
            enemy_spawn_interval = new_interval
            pygame.time.set_timer(ENEMY_SPAWN_EVENT, enemy_spawn_interval)

        if mute:
            screen.blit(mute_img, mute_rect)
        else:
            screen.blit(unmute_img, unmute_rect)
        screen.blit(crosshair_surf, crosshair_rect)
        score_surf = score_font.render(f"Score: {score}", True, (255, 255, 255))
        score_rect = score_surf.get_rect(topleft=(10, 10))
        screen.blit(score_surf, score_rect)
        time_surf = score_font.render(f"Time: {elapsed_time}", True, (255, 255, 255))
        time_rect = score_surf.get_rect(topleft=(10, 50))
        screen.blit(time_surf, time_rect)

    elif game_status == CONFIRM_EXIT_STATE:
        screen.fill(DARK_GRAY)
        confirm_text = exit_font.render("Are you sure?", True, RED)
        screen.blit(confirm_text,(WIDTH // 2 - confirm_text.get_width() // 2, 100))
        yes_button_rect = draw_button("Yes", 300, 250, 200, 50)
        no_button_rect = draw_button("No", 300, 320, 200, 50)
        screen.blit(crosshair_surf, crosshair_rect)

    elif game_status == GAME_OVER_STATE:
        screen.fill(BLACK)
        game_over_font = pygame.font.Font("font/BLOODY.TTF", 72)
        game_over_surf = game_over_font.render("Game over", True, RED)
        game_over_rect = game_over_surf.get_rect(center=(WIDTH / 2, HEIGHT / 3))
        screen.blit(game_over_surf, game_over_rect)
        pygame.mixer.music.stop()

        # Reveal score
        score_surf = score_font.render(f"Score: {score}", True, WHITE)
        score_rect = score_surf.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        screen.blit(score_surf, score_rect)

        # Show the highest score
        highest_score_surf = score_font.render(f"Highest score: {highscore}",
                                               True,WHITE)
        highest_score_rect = highest_score_surf.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 50))
        screen.blit(highest_score_surf, highest_score_rect)

        # Elapsed time
        elapsed_time = (game_end_time - game_start_time) // 1000  # mp-ben
        time_surf = score_font.render(f"Elapsed time: {elapsed_time} sec",
                                      True, (255, 255, 255))
        time_rect = time_surf.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 100))
        screen.blit(time_surf, time_rect)

        # Restart opportunity
        restart_surf = score_font.render("Press 'R' to Restart!", True, RED)
        restart_rect = restart_surf.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 150))
        screen.blit(restart_surf, restart_rect)

        # Exit opportunity
        exit_surf = score_font.render("Press 'E' to Exit!", True, RED)
        exit_rect = exit_surf.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 200))
        screen.blit(exit_surf, exit_rect)

        # If 'R' pressed, restart  game
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            game_status = MENU_STATE
            score = 0
            game_start_time = pygame.time.get_ticks()
            game_end_time = 0
            pygame.time.set_timer(ENEMY_SPAWN_EVENT, 2000)

            all_sprites.empty()
            enemies.empty()
            pygame.mixer.music.play()

        # If 'E' pressed, exit game
        if keys[pygame.K_e]:
            running = False

    pygame.display.update()
    clock.tick(FPS)


pygame.quit()
sys.exit()

