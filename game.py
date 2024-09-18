import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Element Escape: Iron vs Arsenic")

# Colors
WHITE = (255, 255, 255)
GRAY = (169, 169, 169)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Player properties
player_size = 30  # Player is now smaller
player_x = WIDTH // 2 - player_size // 2
player_y = HEIGHT - player_size
player_speed = 5
rusted_slowdown = False
rusted_timer = 0

# Arsenic (enemy) properties
enemy_size = 30
enemy_speed = 4
enemy_list = []

# Iron particles (collectible) properties
iron_size = 20
iron_list = []

# Water droplets (to cause rust)
water_size = 30
water_list = []

# Game variables
score = 0
rusted = False
game_over = False
clock = pygame.time.Clock()
font = pygame.font.Font(None, 30)

# Track whether the fact has been displayed
fact_displayed = False

# Educational Prompts
prompts = [
    "Fact: Iron is the 4th most abundant element in Earth's crust.",
    "Fact: Arsenic was used as a poison in ancient times.",
    "Fact: Iron rusts when exposed to oxygen and water.",
    "Fact: Arsenic is used in semiconductors.",
    "Fact: Iron is essential for blood production.",
    "Fact: Iron is the most commonly used metal in the world, primarily in the form of steel.",
    "Fact: Iron is essential for the human body because it helps transport oxygen in the blood.",
    "Fact: The Earth’s core is mostly made of iron and nickel.",
    "Fact: Pure iron is relatively soft, but adding carbon makes it significantly stronger, forming steel.",
    "Fact: Iron deficiency is the most common nutritional disorder in the world.",
    "Fact: Iron can exist in many oxidation states, but +2 and +3 are the most common.",
    "Fact: Iron is magnetic, which is why it's used in many electronic devices.",
    "Fact: Iron was one of the first metals to be discovered and used by humans, dating back over 5,000 years."
    "Fact: Arsenic is a metalloid, meaning it has properties of both metals and non-metals.",
    "Fact: Arsenic is highly toxic and has been historically used as a poison.",
    "Fact: Despite its toxicity, arsenic is used in semiconductors, especially in gallium arsenide.",
    "Fact: Arsenic is found naturally in many minerals, usually in combination with sulfur and metals.",
    "Fact: Arsenic poisoning was historically used in criminal activities because it’s tasteless and odorless.",
    "Fact: In small doses, arsenic has been used in medicine to treat illnesses like syphilis and psoriasis.",
    "Fact: Inorganic arsenic compounds are the most toxic, compared to organic arsenic compounds found in seafood.",
    "Fact: Arsenic is used in pesticides and wood preservatives, though its use is highly regulated."
]

def display_message(text):
    label = font.render(text, 1, WHITE)
    screen.blit(label, (WIDTH // 2 - label.get_width() // 2, HEIGHT // 2 - label.get_height() // 2))
    pygame.display.update()

def wrap_text(text, font, max_width):
    # Split text into words
    words = text.split(' ')
    lines = []
    current_line = ""

    for word in words:
        # Add the word to the current line
        test_line = current_line + word + " "
        # Check if the width of the test line is greater than the allowed width
        if font.size(test_line)[0] > max_width:
            # If it is, add the current line to lines and start a new one
            lines.append(current_line)
            current_line = word + " "
        else:
            current_line = test_line

    # Add the last line
    if current_line:
        lines.append(current_line)

    return lines

def pause_for_fact(text):
    screen.fill(BLACK)  # Clear the screen with a black background
    x_position = 50  # Starting x position for the text
    y_position = 100  # Starting y position for the text
    line_height = 40  # Spacing between lines, adjust based on font size
    max_width = WIDTH - 100  # Maximum width of the text, with padding on both sides

    # Split the text into wrapped lines
    wrapped_lines = wrap_text(text, font, max_width)
    
    # Render each wrapped line separately
    for i, line in enumerate(wrapped_lines):
        label = font.render(line, True, WHITE)
        screen.blit(label, (x_position, y_position + i * line_height))

    pygame.display.update()  # Update the display to show the text
    time.sleep(5)  # Pause for 3 seconds

# Functions to manage enemies, collectibles, and water
def drop_enemy(enemy_list):
    if len(enemy_list) < 10:
        enemy_x = random.randint(0, WIDTH - enemy_size)
        enemy_y = 0
        enemy_list.append([enemy_x, enemy_y])

def update_enemy_positions(enemy_list):
    for enemy in enemy_list:
        enemy[1] += enemy_speed
        if enemy[1] > HEIGHT:
            enemy_list.remove(enemy)

def draw_enemies(enemy_list):
    for enemy in enemy_list:
        pygame.draw.rect(screen, RED, (enemy[0], enemy[1], enemy_size, enemy_size))

def drop_iron(iron_list):
    if len(iron_list) < 5:
        iron_x = random.randint(0, WIDTH - iron_size)
        iron_y = 0
        iron_list.append([iron_x, iron_y])

def update_iron_positions(iron_list):
    for iron in iron_list:
        iron[1] += enemy_speed // 2
        if iron[1] > HEIGHT:
            iron_list.remove(iron)

def draw_iron(iron_list):
    for iron in iron_list:
        pygame.draw.rect(screen, GREEN, (iron[0], iron[1], iron_size, iron_size))

def drop_water(water_list):
    if len(water_list) < 3:
        water_x = random.randint(0, WIDTH - water_size)
        water_y = 0
        water_list.append([water_x, water_y])

def update_water_positions(water_list):
    for water in water_list:
        water[1] += enemy_speed // 2
        if water[1] > HEIGHT:
            water_list.remove(water)

def draw_water(water_list):
    for water in water_list:
        pygame.draw.rect(screen, BLUE, (water[0], water[1], water_size, water_size))

def detect_collision(player_x, player_y, object_x, object_y, object_size):
    if (player_x < object_x < player_x + player_size or player_x < object_x + object_size < player_x + player_size) and \
       (player_y < object_y < player_y + player_size or player_y < object_y + object_size < player_y + player_size):
        return True
    return False

def check_collisions(player_x, player_y, enemy_list, iron_list, water_list, score, rusted):
    for enemy in enemy_list:
        if detect_collision(player_x, player_y, enemy[0], enemy[1], enemy_size):
            return True, score, rusted

    for iron in iron_list:
        if detect_collision(player_x, player_y, iron[0], iron[1], iron_size):
            iron_list.remove(iron)
            score += 1

    for water in water_list:
        if detect_collision(player_x, player_y, water[0], water[1], water_size):
            rusted = True

    return False, score, rusted

# Game Loop
while not game_over:
    screen.fill(BLACK)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
        player_x += player_speed

    # Apply rust effect (slow down player for 3 seconds)
    if rusted_slowdown:
        player_speed = 3
        rusted_timer -= 1
        if rusted_timer <= 0:
            rusted_slowdown = False
            player_speed = 5

    # Drop enemies, iron, and water droplets
    drop_enemy(enemy_list)
    update_enemy_positions(enemy_list)
    draw_enemies(enemy_list)

    drop_iron(iron_list)
    update_iron_positions(iron_list)
    draw_iron(iron_list)

    drop_water(water_list)
    update_water_positions(water_list)
    draw_water(water_list)

    # Check for collisions
    collision, score, rusted = check_collisions(player_x, player_y, enemy_list, iron_list, water_list, score, rusted)
    if collision:
        display_message("Game Over!")
        pygame.display.update()
        pygame.time.wait(2000)
        game_over = True

    # If player touches water, slow down temporarily
    if rusted:
        rusted_slowdown = True
        rusted_timer = 45  # Slow down for 3 seconds (90 frames at 30 FPS)
        rusted = False

    # Draw the player (Iron)
    if rusted_slowdown:
        pygame.draw.rect(screen, (128, 128, 128), (player_x, player_y, player_size, player_size))  # Rusted color
    else:
        pygame.draw.rect(screen, GRAY, (player_x, player_y, player_size, player_size))

    # Display the score
    score_label = font.render(f"Score: {score}", 1, WHITE)
    screen.blit(score_label, (10, 10))

    # Display a fact after reaching a multiple of 5 points, only once
    if score > 0 and score % 5 == 0 and not fact_displayed:
        pause_for_fact(random.choice(prompts))
        fact_displayed = True
    if score % 5 != 0:
        fact_displayed = False

    pygame.display.update()

    # Frame rate
    clock.tick(30)

# Quit Pygame
pygame.quit()
