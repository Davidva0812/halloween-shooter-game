import pygame


# Constants
WIDTH, HEIGHT =  800, 600
RED = (214, 2, 2)
BLACK = (0, 0, 0)
DARK_GRAY = (89, 89, 87)
WHITE = (255, 255, 255)
FPS = 60

# Initialization
pygame.init()
pygame.mouse.set_visible(False)  # Hide mouse button
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Halloween Night")
halloween_icon = pygame.image.load("images/pumpkin.png")
pygame.display.set_icon(halloween_icon)
clock = pygame.time.Clock()

# Music
volume_level = 0.5
pygame.mixer.init()
pygame.mixer.music.load("sounds/CrEEP.mp3")
pygame.mixer.music.set_volume(volume_level)
pygame.mixer.music.play(-1)  # Infinite repeat

# Images: bat, zombie, wraith, crosshair
bg_img = pygame.image.load("images/halloween.png").convert()
bg_img = pygame.transform.scale(bg_img, (800, 600))
cemetery_bg = pygame.image.load("images/cemetery_bg.jpg")
cemetery_bg = pygame.transform.scale(cemetery_bg, (800, 600))
bat_surf = [pygame.image.load(f"images/bat_{i}.png").convert_alpha() for i in range(1, 6)]
zombie_surf = [pygame.image.load(f"images/zombie_{i}.png").convert_alpha() for i in range(1, 5)]
zombie_surf = [pygame.transform.scale(image, (100, 100)) for image in zombie_surf]
wraith_surf = [pygame.image.load(f"images/wraith_{i}.png").convert_alpha() for i in range(1, 11)]
wraith_surf = [pygame.transform.scale(image, (100, 100)) for image in wraith_surf]
skeleton_surf = [pygame.image.load(f"images/skeleton_{i}.png").convert_alpha() for i in range(1, 11)]
skeleton_surf = [pygame.transform.scale(image, (100, 100)) for image in skeleton_surf]
jack_surf = [pygame.image.load(f"images/jack_{i}.png").convert_alpha() for i in range(1, 11)]
jack_surf = [pygame.transform.scale(image, (100, 100)) for image in jack_surf]
crosshair_surf = pygame.image.load("images/crosshair.png").convert_alpha()
crosshair_rect = crosshair_surf.get_rect(center=(WIDTH / 2, HEIGHT / 2))
mute_img = pygame.image.load("images/mute.png").convert()
mute_img = pygame.transform.scale(mute_img, (40, 40))
mute_rect = mute_img.get_rect(center=(770, 570))
unmute_img = pygame.image.load("images/unmute.png").convert()
unmute_img = pygame.transform.scale(unmute_img, (40, 40))
unmute_rect = mute_img.get_rect(center=(770, 570))
yes_button_rect = pygame.Rect(300, 250, 200, 50)
no_button_rect = pygame.Rect(300, 320, 200, 50)

# Fonts
title_font = pygame.font.Font("font/BLOODY.TTF", 82)
title_surf = title_font.render("Halloween Night", True, RED)
title_rect = title_surf.get_rect(center=(WIDTH / 2, 80))
press_space_font = pygame.font.Font("font/BLOODY.TTF", 42)
press_space_surf = press_space_font.render("Press SPACE to Start", True, RED)
press_space_rect = press_space_surf.get_rect(center=(WIDTH / 2, 550))
score_font = pygame.font.Font("font/BLOODY.TTF", 32)
time_font = pygame.font.Font("font/BLOODY.TTF", 32)
exit_font = pygame.font.Font("font/BLOODY.TTF", 42)










