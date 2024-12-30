```python
import pygame
import sys
import random
import math

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
NUM_COAL = 5
COAL_SIZE = 50
MIN_COAL_SPEED = 2
MAX_COAL_SPEED = 5
BIG_COAL_SIZE = 100
BIG_COAL_SPEED_FACTOR = 0.5
SNOWFLAKE_DRIFT = 1
BASE_SPEED_CHANGE = 2
POWERUP_DURATION = 10000
POWERUP_CHANCE = 0.15
ITEM_FALL_SPEED = 3
SLEIGH_LIVES = 3
SHIELD_DURATION = 5000
FREEZE_DURATION = 7000
MAGNET_DURATION = 7000
TIME_FOR_BIG_COAL = 20
WARNING_DURATION = 3000
BLIZZARD_DURATION = 15000
METEOR_SHOWER_DURATION = 15000
METEOR_SPEED_BOOST = 3
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GOLD = (255, 215, 0)
CYAN = (0, 255, 255)
GRAY = (128, 128, 128)
PINK = (255, 20, 147)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("David's Sleigh Dash")

background_image = pygame.image.load("background.png").convert()
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
coal_img = pygame.image.load("coal.png").convert_alpha()
coal_img = pygame.transform.scale(coal_img, (COAL_SIZE, COAL_SIZE))
snowflake_img = pygame.image.load("snowflake.png").convert_alpha()
snowflake_img = pygame.transform.scale(snowflake_img, (COAL_SIZE, COAL_SIZE))
big_coal_img = pygame.transform.scale(coal_img, (BIG_COAL_SIZE, BIG_COAL_SIZE))
sleigh_image = pygame.image.load("sleigh.png").convert_alpha()
sleigh_width = 110
sleigh_height = 180
sleigh_image = pygame.transform.scale(sleigh_image, (sleigh_width, sleigh_height))
end_screen_image = pygame.image.load("davidEndScreen.png").convert_alpha()
font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()

def get_sleigh_hitbox(sleigh_rect):
    hitbox_padding_x = 20
    hitbox_padding_y = 30
    return pygame.Rect(
        sleigh_rect.x + hitbox_padding_x,
        sleigh_rect.y + hitbox_padding_y,
        sleigh_rect.width - 2 * hitbox_padding_x,
        sleigh_rect.height - 2 * hitbox_padding_y
    )

def create_normal_coal():
    x_pos = random.randint(0, SCREEN_WIDTH - COAL_SIZE)
    y_pos = -COAL_SIZE
    return {
        "type": "coal",
        "rect": pygame.Rect(x_pos, y_pos, COAL_SIZE, COAL_SIZE),
        "x_speed": 0,
        "y_speed": random.randint(MIN_COAL_SPEED, MAX_COAL_SPEED)
    }

def create_big_coal():
    x_pos = random.randint(0, SCREEN_WIDTH - BIG_COAL_SIZE)
    y_pos = -BIG_COAL_SIZE
    speed = int(random.randint(MIN_COAL_SPEED, MAX_COAL_SPEED) * BIG_COAL_SPEED_FACTOR)
    return {
        "type": "big_coal",
        "rect": pygame.Rect(x_pos, y_pos, BIG_COAL_SIZE, BIG_COAL_SIZE),
        "x_speed": 0,
        "y_speed": speed
    }

def create_snowflake():
    x_pos = random.randint(0, SCREEN_WIDTH - COAL_SIZE)
    y_pos = -COAL_SIZE
    y_speed = random.randint(MIN_COAL_SPEED, MAX_COAL_SPEED)
    x_speed = random.choice([-SNOWFLAKE_DRIFT, SNOWFLAKE_DRIFT])
    return {
        "type": "snowflake",
        "rect": pygame.Rect(x_pos, y_pos, COAL_SIZE, COAL_SIZE),
        "x_speed": x_speed,
        "y_speed": y_speed
    }

def create_coal_set(num_coal):
    return [create_normal_coal() for _ in range(num_coal)]

def create_item():
    power_types = ["speed_up", "speed_down", "shield", "freeze", "magnet", "health", "event_trigger"]
    power_type = random.choice(power_types)
    if power_type == "speed_up":
        color = RED
    elif power_type == "speed_down":
        color = BLUE
    elif power_type == "shield":
        color = GOLD
    elif power_type == "freeze":
        color = CYAN
    elif power_type == "magnet":
        color = GRAY
    elif power_type == "health":
        color = PINK
    else:
        color = GREEN
    item_width = 30
    item_height = 30
    x_pos = random.randint(0, SCREEN_WIDTH - item_width)
    y_pos = -item_height
    rect = pygame.Rect(x_pos, y_pos, item_width, item_height)
    return (rect, power_type, color)

def draw_sleigh(surface, sleigh_rect):
    surface.blit(sleigh_image, (sleigh_rect.x, sleigh_rect.y))

def draw_obstacle(surface, obstacle):
    rect = obstacle["rect"]
    obs_type = obstacle["type"]
    if obs_type == "coal":
        surface.blit(coal_img, (rect.x, rect.y))
    elif obs_type == "big_coal":
        surface.blit(big_coal_img, (rect.x, rect.y))
    else:
        surface.blit(snowflake_img, (rect.x, rect.y))

def draw_item(surface, item_tuple):
    rect, power_type, color = item_tuple
    pygame.draw.rect(surface, color, rect)

def display_message_centered(surface, msg, color, font_obj):
    surf = font_obj.render(msg, True, color)
    x = (SCREEN_WIDTH - surf.get_width()) // 2
    y = (SCREEN_HEIGHT - surf.get_height()) // 3
    surface.blit(surf, (x, y))

def apply_blizzard_overlay(surface):
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 100))
    surface.blit(overlay, (0, 0))

def colliding_obstacle(sleigh_rect, obstacles):
    sleigh_hitbox = get_sleigh_hitbox(sleigh_rect)
    for obs in obstacles:
        if sleigh_hitbox.colliderect(obs["rect"]):
            return obs
    return None

def check_collision_sleigh_items(sleigh_rect, items):
    sleigh_hitbox = get_sleigh_hitbox(sleigh_rect)
    for i, (rect, power_type, color) in enumerate(items):
        if sleigh_hitbox.colliderect(rect):
            return i
    return -1

def apply_magnet(sleigh_rect, items):
    MAGNET_RADIUS = 200
    MAGNET_PULL_SPEED = 3
    center = (sleigh_rect.centerx, sleigh_rect.centery)
    updated = []
    for rect, ptype, color in items:
        dist = math.dist(center, (rect.centerx, rect.centery))
        if dist < MAGNET_RADIUS:
            dx = center[0] - rect.centerx
            dy = center[1] - rect.centery
            angle = math.atan2(dy, dx)
            rect.x += int(MAGNET_PULL_SPEED * math.cos(angle))
            rect.y += int(MAGNET_PULL_SPEED * math.sin(angle))
        updated.append((rect, ptype, color))
    return updated

def run_game():
    original_speeds_dict = {}
    life_lost_message = ""
    life_lost_message_timer = 0
    message_display_duration = 2000
    sleigh_rect = pygame.Rect(
        (SCREEN_WIDTH // 2) - (sleigh_width // 2),
        SCREEN_HEIGHT - sleigh_height - 10,
        sleigh_width,
        sleigh_height
    )
    sleigh_lives = SLEIGH_LIVES
    obstacles = create_coal_set(NUM_COAL)
    items = []
    start_time = pygame.time.get_ticks()
    last_life_lost_time = start_time
    big_coal_unlocked = False
    warning_active = False
    warning_message = ""
    warning_start = 0
    active_event = None
    event_start = 0
    event_warning = False
    event_warning_start = 0
    freeze_active = False
    freeze_end_time = 0
    shield_active = False
    shield_end_time = 0
    magnet_active = False
    magnet_end_time = 0
    power_up_active = None
    power_up_end_time = 0
    original_speeds_list = []
    power_message = ""
    power_message_color = WHITE
    power_message_start = 0
    power_message_duration = 2000
    blizzard_snowflakes = []
    running = True
    while running:
        clock.tick(FPS)
        current_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and sleigh_rect.left > 0:
            sleigh_rect.x -= 5
        if keys[pygame.K_RIGHT] and sleigh_rect.right < SCREEN_WIDTH:
            sleigh_rect.x += 5
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()
        if random.random() < (POWERUP_CHANCE / FPS):
            items.append(create_item())
        updated_obs = []
        for obs in obstacles:
            if not freeze_active:
                obs["rect"].x += obs["x_speed"]
                obs["rect"].y += obs["y_speed"]
            if obs["rect"].y > SCREEN_HEIGHT:
                if obs["type"] == "big_coal":
                    obs["rect"].y = -BIG_COAL_SIZE
                    obs["rect"].x = random.randint(0, SCREEN_WIDTH - BIG_COAL_SIZE)
                elif obs["type"] == "snowflake":
                    obs["rect"].y = -COAL_SIZE
                    obs["rect"].x = random.randint(0, SCREEN_WIDTH - COAL_SIZE)
                else:
                    obs["rect"].y = -COAL_SIZE
                    obs["rect"].x = random.randint(0, SCREEN_WIDTH - COAL_SIZE)
            if obs["type"] == "snowflake":
                if obs["rect"].x < 0 or obs["rect"].x > SCREEN_WIDTH - COAL_SIZE:
                    obs["x_speed"] *= -1
            updated_obs.append(obs)
        obstacles = updated_obs
        updated_items = []
        for rect, ptype, color in items:
            if not freeze_active:
                rect.y += ITEM_FALL_SPEED
            updated_items.append((rect, ptype, color))
        items = updated_items
        if magnet_active:
            items = apply_magnet(sleigh_rect, items)
        items = [(r, p, c) for (r, p, c) in items if r.y < SCREEN_HEIGHT]
        collided_obs = colliding_obstacle(sleigh_rect, obstacles)
        if collided_obs is not None:
            if not shield_active:
                sleigh_lives -= 1
                life_lost_message = f"You lost a life! Lives remaining: {sleigh_lives}"
                life_lost_message_timer = current_time
                last_life_lost_time = current_time
                obstacles.remove(collided_obs)
                if sleigh_lives <= 0:
                    running = False
        idx = check_collision_sleigh_items(sleigh_rect, items)
        if idx != -1:
            rect, ptype, color = items.pop(idx)
            if ptype == "freeze":
                freeze_active = True
                freeze_end_time = current_time + FREEZE_DURATION
                original_speeds_dict = {}
                for o in obstacles:
                    original_speeds_dict[id(o)] = o["y_speed"]
                    o["y_speed"] = 0
                power_message = "Freeze! Objects won't move for 7s."
                power_message_color = CYAN
            elif ptype == "speed_up":
                power_up_active = "speed_up"
                power_up_end_time = current_time + POWERUP_DURATION
                original_speeds_list = [o["y_speed"] for o in obstacles]
                for o in obstacles:
                    o["y_speed"] += BASE_SPEED_CHANGE
                power_message = "Speed Up! Obstacles move faster (10s)!"
                power_message_color = RED
            elif ptype == "speed_down":
                power_up_active = "speed_down"
                power_up_end_time = current_time + POWERUP_DURATION
                original_speeds_list = [o["y_speed"] for o in obstacles]
                for o in obstacles:
                    o["y_speed"] = max(1, o["y_speed"] - BASE_SPEED_CHANGE)
                power_message = "Speed Down! Obstacles slow down (10s)!"
                power_message_color = BLUE
            elif ptype == "shield":
                shield_active = True
                shield_end_time = current_time + SHIELD_DURATION
                power_message = "Shield Up! You're protected for 5s."
                power_message_color = GOLD
            elif ptype == "magnet":
                magnet_active = True
                magnet_end_time = current_time + MAGNET_DURATION
                power_message = "Magnet! Items are pulled to you (7s)."
                power_message_color = GRAY
            elif ptype == "health":
                if sleigh_lives < 3:
                    sleigh_lives += 1
                    power_message = "Health Restored! +1 life."
                else:
                    power_message = "You're already at full health!"
                power_message_color = PINK
            elif ptype == "event_trigger":
                event_warning = True
                event_warning_start = current_time
                power_message = "Special Event Incoming!"
                power_message_color = BLACK
            power_message_start = current_time
        if event_warning and current_time - event_warning_start > WARNING_DURATION:
            event_warning = False
            active_event = random.choice(["blizzard", "meteor"])
            event_start = current_time
            if active_event == "blizzard":
                blizzard_snowflakes = []
                for _ in range(3):
                    new_flake = create_snowflake()
                    obstacles.append(new_flake)
                    blizzard_snowflakes.append(new_flake)
                power_message = "Blizzard Strikes! Snowflakes are falling (15s)!"
                power_message_color = CYAN
                power_message_start = current_time
            elif active_event == "meteor":
                for o in obstacles:
                    o["y_speed"] += METEOR_SPEED_BOOST
                power_message = "Meteor Shower! Obstacles speeding up (15s)!"
                power_message_color = RED
                power_message_start = current_time
        if active_event == "blizzard" and current_time - event_start > BLIZZARD_DURATION:
            for flake in blizzard_snowflakes:
                if flake in obstacles:
                    obstacles.remove(flake)
            blizzard_snowflakes.clear()
            active_event = None
        if active_event == "meteor" and current_time - event_start > METEOR_SHOWER_DURATION:
            for o in obstacles:
                o["y_speed"] -= METEOR_SPEED_BOOST
            active_event = None
        if freeze_active and current_time > freeze_end_time:
            freeze_active = False
            for o in obstacles:
                obs_id = id(o)
                if obs_id in original_speeds_dict:
                    o["y_speed"] = original_speeds_dict[obs_id]
        if shield_active and current_time > shield_end_time:
            shield_active = False
        if magnet_active and current_time > magnet_end_time:
            magnet_active = False
        if power_up_active in ["speed_up", "speed_down"] and current_time > power_up_end_time:
            for i, o in enumerate(obstacles):
                if i < len(original_speeds_list):
                    o["y_speed"] = original_speeds_list[i]
            power_up_active = None
        screen.blit(background_image, (0, 0))
        if active_event == "blizzard":
            apply_blizzard_overlay(screen)
        for obs in obstacles:
            draw_obstacle(screen, obs)
        for it in items:
            draw_item(screen, it)
        elapsed_time = (current_time - start_time) // 1000
        score_surf = font.render(f"Time: {elapsed_time}s", True, WHITE)
        lives_surf = font.render(f"Lives: {sleigh_lives}", True, WHITE)
        screen.blit(score_surf, (10, 10))
        screen.blit(lives_surf, (10, 50))
        draw_sleigh(screen, sleigh_rect)
        if freeze_active:
            frz_rem = max(0, (freeze_end_time - current_time) // 1000)
            frz_surf = font.render(f"Freeze: {frz_rem}s", True, CYAN)
            screen.blit(frz_surf, (SCREEN_WIDTH - 150, 10))
        if shield_active:
            shield_surf = font.render("Shield: Active", True, GOLD)
            screen.blit(shield_surf, (10, 90))
        if magnet_active:
            mag_rem = max(0, (magnet_end_time - current_time) // 1000)
            mag_surf = font.render(f"Magnet: {mag_rem}s", True, GRAY)
            screen.blit(mag_surf, (SCREEN_WIDTH - 150, 50))
        now = current_time
        if now - power_message_start < power_message_duration:
            msg_surf = font.render(power_message, True, power_message_color)
            x = (SCREEN_WIDTH - msg_surf.get_width()) // 2
            y = SCREEN_HEIGHT // 3
            screen.blit(msg_surf, (x, y))
        if current_time - life_lost_message_timer < message_display_duration:
            msg_surf = font.render(life_lost_message, True, RED)
            msg_x = (SCREEN_WIDTH - msg_surf.get_width()) // 2
            msg_y = SCREEN_HEIGHT // 2
            screen.blit(msg_surf, (msg_x, msg_y))
        pygame.display.flip()
    return elapsed_time

def show_game_over(score):
    go_font = pygame.font.SysFont(None, 60)
    cont_font = pygame.font.SysFont(None, 36)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_r:
                    return True
        screen.blit(background_image, (0, 0))
        game_over_surf = go_font.render("Game Over!", True, RED)
        score_surf = cont_font.render(f"You survived: {score} seconds", True, WHITE)
        info_surf = cont_font.render("Press 'R' to Restart or 'ESC' to Quit", True, WHITE)
        game_over_x = (SCREEN_WIDTH // 2) - (game_over_surf.get_width() // 2)
        game_over_y = (SCREEN_HEIGHT // 2) - 100
        score_x = (SCREEN_WIDTH // 2) - (score_surf.get_width() // 2)
        score_y = (SCREEN_HEIGHT // 2) - 20
        info_x = (SCREEN_WIDTH // 2) - (info_surf.get_width() // 2)
        info_y = (SCREEN_HEIGHT // 2) + 40
        screen.blit(game_over_surf, (game_over_x, game_over_y))
        screen.blit(score_surf, (score_x, score_y))
        screen.blit(info_surf, (info_x, info_y))
        man_x = score_x - end_screen_image.get_width() + 450
        man_y = score_y - 30
        screen.blit(end_screen_image, (man_x, man_y))
        pygame.display.flip()

def main():
    while True:
        final_score = run_game()
        restart = show_game_over(final_score)
        if not restart:
            break
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
```
