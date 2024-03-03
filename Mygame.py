import pygame
from pygame.locals import *
import random

# Initialize pygame
pygame.init()

# Set screen dimensions
width = 500
height = 500
screen_size = (width, height)


# Set up the display
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("elf_barbarossa")

# Define colors
gray = (93,59,26)
green = (75,83,32)
red = (200, 4, 6)
white = (255,255,255)
gray2 = (55,35,15)
gray3=(75,56,38)

# Game settings
gameover = False
speed = 3
score = 0
booster=0.5
limit=100
score_for_speed = 0
coin_score=0
try:
    with open("Record.txt", "r") as input_file:    
        record_str = input_file.readline().strip() 
        if record_str:
            record = float(record_str)
        else:
            record = 0 
except FileNotFoundError:
    record = 0 
# Marker size
marker_width = 10
marker_height = 50

# Road
road = (100, 0, 300, height)
left_edge_markers = (95, 0, marker_width, height)
right_edge_markers = (395, 0, marker_width, height)

# X coordinates for tree
left_line_tree = 70
right_line_tree = 450
left_line_tree2 = 45
right_line_tree2 = 470
left_line_tree3 = 20
right_line_tree3 = 420
lines2 = [left_line_tree, right_line_tree, left_line_tree2, right_line_tree2, right_line_tree3, left_line_tree3]

# X coordinates
left_line = 150
center_line = 250
right_line = 350
lines = [left_line, center_line, right_line]

left_line2 = 115
center_line2 = 225
right_line2 = 360
left_line3 = 175
center_line3= 275
right_line3 = 335
lines3= [left_line2, center_line2, right_line2, left_line3, center_line3 , right_line3]

# For animation
line_mark_move_y = 0

# Define sprite classes
class Vagon(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        image_scale = 60 / image.get_rect().width
        new_width = 60
        new_height = image.get_rect().height * image_scale
        self.image = pygame.transform.scale(image, (int(new_width), int(new_height)))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

class Player(Vagon):
    def __init__(self, image, x, y):
        image = pygame.image.load(image)
        super().__init__(image, x, y)

# Define Tree class
class Tree(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        image_scale = 70 / image.get_rect().width
        new_width = image.get_rect().width * image_scale
        new_height = image.get_rect().height * image_scale
        self.image = pygame.transform.scale(image, (int(new_width), int(new_height)))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
# Define coin class
class Coin(pygame.sprite.Sprite):
    def __init__(self, images, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = [pygame.transform.scale(image, (40, 45)) for image in images]
        self.image_index = 0
        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.animation_speed = 5
        self.animation_counter = 0


    def update(self):
        # Update animation
        self.animation_counter += 1
        if self.animation_counter >= self.animation_speed:
            self.animation_counter = 0
            self.image_index = (self.image_index + 1) % len(self.images)
            self.image = self.images[self.image_index]

        # Update the coin's position
        self.rect.y += speed * 0.7 

        # Wrap around the screen if the coin goes off the edges
        if self.rect.top > height:
            self.rect.bottom = 0



# Player spawn point
player_x = 250
player_y = 400

# Player settings
player_group = pygame.sprite.Group()
player = Player('images/player1.com.png', player_x, player_y)
player_group.add(player)
frame = 0

# Load vagon images
image_filenames = ['monster1_1.png', 'monster2_1.png', 'monster3_1.png']
vagon_images = []
for image_filename in image_filenames:
    image = pygame.image.load('images/' + image_filename )
    vagon_images.append(image)


# Load tree images
image_trees = ['agash1.png','agash2.png','agash3.png', 'agash4.png','agash5.png','agash6.png', 'tas1.png', 'tas2.png']
tree_images = []
for image_tree in image_trees:
    image = pygame.image.load('images/' + image_tree)
    tree_images.append(image)

# Create sprite groups
vagon_group = pygame.sprite.Group()
tree_group = pygame.sprite.Group()

# Load coin animation images
coin_images = []
for i in range(1):
    image = pygame.image.load(f'images/diamond.gif')
    coin_images.append(image)

# Create sprite group for coins
coin_group = pygame.sprite.Group()

kamushka_images = []
for i in range(1,3):
    image = pygame.image.load(f'images/lav1.png')
    kamushka_images.append(image)

# Create sprite group for coins
kamushka_group = pygame.sprite.Group()



# Load crash image
crash = pygame.image.load('images/player3.png')
crash_rect = crash.get_rect()

# Load background music
pygame.mixer.init()
background_music = pygame.mixer.Sound('images/13 Thunderbrew.mp3')
background_music.play(-1)  # Loop

# Load crash sound effect
crash_sound = pygame.mixer.Sound('images/death.wav')

# Load money get effect
money_get=pygame.mixer.Sound('images\money2.wav')

# Game loop
clock = pygame.time.Clock()
fps = 120
running = True
paused = False
while running:
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
    
        if event.type == KEYDOWN:
            if event.key == K_LEFT and player.rect.center[0] > left_line:
                player.rect.x -= 100
            elif event.key == K_RIGHT and player.rect.center[0] < right_line:
                player.rect.x += 100
            elif event.key == K_DOWN:
                paused = not paused
            elif event.key == K_UP:
                paused= not paused

            for vagon in vagon_group:
                if pygame.sprite.collide_rect(player, vagon):
                    gameover = True
    if paused:
        pygame.draw.rect(screen, white, (75, 45, 350, 110))
        pygame.draw.rect(screen, green, (80, 50, 340, 100))
        triangle_center_x = 250
        triangle_center_y = 250
        triangle_side_length = 60
        triangle_points = [
            (triangle_center_x - triangle_side_length // 2, triangle_center_y - triangle_side_length // 2),
            (triangle_center_x - triangle_side_length // 2, triangle_center_y + triangle_side_length // 2), 
            (triangle_center_x + triangle_side_length // 2, triangle_center_y)]
        pygame.draw.polygon(screen, white, triangle_points)

        font = pygame.font.Font(pygame.font.get_default_font(), 16)
        text = font.render('Pause: to continue press up or down key', True, white)
        text1=font.render('Your score: '+str(round(score)),True, white)
        text2=font.render('Your coins: '+str(round(coin_score)),True, white)
        text3=font.render('Record: '+str(round(record)),True, white)
        text_rect = text.get_rect()
        text_rect1 = text1.get_rect()
        text_rect2=text2.get_rect()
        text_rect3=text3.get_rect()
        text_rect.center = (width / 2, 70)
        text_rect1.center = (width / 2, 110)
        text_rect2.center=(width/2,130)
        text_rect3.center=(width/2,90)
        screen.blit(text, text_rect)
        screen.blit(text1, text_rect1)
        screen.blit(text2, text_rect2)
        screen.blit(text3, text_rect3)
        pygame.display.update()
        continue

    frame += 1
    if frame >= 30:
        frame = 0
    if frame < 15:
        image = pygame.image.load('images/player1.com.png')
    else:
        image = pygame.image.load('images/player2.com.png')

    image_scale = 45 / image.get_rect().width
    new_width = image.get_rect().width * image_scale
    new_height = image.get_rect().height * image_scale
    image = pygame.transform.scale(image, (int(new_width), int(new_height)))
    player.image = image

    screen.fill(green)  # Grass
    pygame.draw.rect(screen, gray, road)  # Road
    pygame.draw.rect(screen, gray2, left_edge_markers)  # Left edge markers
    pygame.draw.rect(screen, gray2, right_edge_markers)  # Right edge markers

    line_mark_move_y += speed * 0.7
    score+=booster
    if score>record:
        with open("Record.txt", "w") as output_file:
            record=score
            output_file.write(str(record))
    if score>limit:
        booster+=0.5
        limit=limit*10
    if line_mark_move_y >= marker_height * 2:
        line_mark_move_y = 0
    for y in range(marker_height * -2, height, marker_height * 2):
        pygame.draw.rect(screen, gray, (left_line + 45, y + line_mark_move_y, marker_width, marker_height))
        pygame.draw.rect(screen, gray, (center_line + 45, y + line_mark_move_y, marker_width, marker_height))

    player_group.draw(screen)

    if len(vagon_group) < 2:
        add_vagon = True
        for vagon in vagon_group:
            if vagon.rect.top < vagon.rect.height * 1.5:
                add_vagon = False
        if add_vagon:
            line = random.choice(lines)
            image = random.choice(vagon_images)
            vagon = Vagon(image, line, height / -2)
            vagon_group.add(vagon)

    for vagon in vagon_group:
        vagon.rect.y += speed

        if vagon.rect.top >= height:
            vagon.kill()
            score_for_speed += 1
            if score_for_speed > 0 and score_for_speed < 400 and score_for_speed % 5 == 0:
                speed += 0.5

    vagon_group.draw(screen)
    # Generate kamushka during the game loop
    if len(kamushka_group) < 5:
        add_coin = True
        for coin in kamushka_group:
            if coin.rect.top < coin.rect.height * 1.5:
                add_coin = False
        if add_coin:
            line = random.choice(lines3)
            coin = Coin(kamushka_images, line, -10)
            kamushka_group.add(coin)
    # Move and update coins
    kamushka_group.update()
    kamushka_group.draw(screen)
    # Add trees
    frame +=0.109
    if frame >=30:
        line = random.choice(lines2)
        image = random.choice(tree_images)
        tree = Tree(image, line, -50)
        tree_group.add(tree)
        frame=0


    # Move trees
    for tree in tree_group:
        tree.rect.y += speed * 0.7

    # Draw trees
    tree_group.draw(screen)
    # Generate coins during the game loop
    if len(coin_group) < 5: 
        add_coin = True
        for coin in coin_group:
            if coin.rect.top < coin.rect.height * 1.5:
                add_coin = False
        if add_coin:
            line = random.choice(lines)  
            coin = Coin(coin_images, line, -50)
            coin_group.add(coin)
    # Move and update coins
    coin_group.update()
    coin_group.draw(screen)

    # Check for collisions between player and coins
    if pygame.sprite.spritecollide(player, coin_group, True):
        coin_score += 1
        money_get.play()
    # Update the coin display
    def draw_rounded_rect(surface, rect, color, radius):
        pygame.draw.circle(surface, color, (rect.left + radius, rect.top + radius), radius)
        pygame.draw.circle(surface, color, (rect.right - radius, rect.top + radius), radius)
        pygame.draw.circle(surface, color, (rect.left + radius, rect.bottom - radius), radius)
        pygame.draw.circle(surface, color, (rect.right - radius, rect.bottom - radius), radius)
        pygame.draw.rect(surface, color, pygame.Rect(rect.left + radius, rect.top, rect.width - radius * 2, rect.height))
        pygame.draw.rect(surface, color, pygame.Rect(rect.left, rect.top + radius, rect.width, rect.height - radius * 2))

    surf = pygame.Surface((90, 25), pygame.SRCALPHA)
    draw_rounded_rect(surf, surf.get_rect(), gray3, 10) 
    surf.set_alpha(200)
    screen.blit(surf, (407, 5))
    screen.blit(surf, (407, 35))
    screen.blit(surf, (407, 65))
    font = pygame.font.Font(pygame.font.get_default_font(), 14)
    text = font.render('Coin: ' + str(round(coin_score)), True, white)
    text_rect = text.get_rect()
    text_rect.center = (453, 47)
    screen.blit(text, text_rect)

    font = pygame.font.Font(pygame.font.get_default_font(), 14)
    text = font.render(str(round(score)), True, white)
    text_rect = text.get_rect()
    text_rect.center = (453, 17)
    screen.blit(text, text_rect)

    font = pygame.font.Font(pygame.font.get_default_font(), 14)
    text = font.render( str(round(record)), True, white)
    text_rect = text.get_rect()
    text_rect.center = (453, 77)
    screen.blit(text, text_rect)

    if pygame.sprite.spritecollide(player, vagon_group, True):
        gameover = True
        crash_rect.center = [player.rect.center[0], player.rect.top]
        crash_sound.play()

    if gameover:
        screen.blit(crash, crash_rect)
        pygame.draw.rect(screen, red, (0, 50, width, 100))

        font = pygame.font.Font(pygame.font.get_default_font(), 16)
        text = font.render('Game Over. Play again? Press Y or N', True, white)
        text1=font.render('Your score: '+str(round(score)),True, white)
        text2=font.render('Your coins: '+str(round(coin_score)),True, white)
        text3=font.render('Record: '+str(round(record)),True, white)
        text_rect = text.get_rect()
        text_rect1 = text1.get_rect()
        text_rect2=text2.get_rect()
        text_rect3=text3.get_rect()
        text_rect.center = (width / 2, 70)
        text_rect1.center = (width / 2, 110)
        text_rect2.center=(width/2,130)
        text_rect3.center=(width/2,90)
        screen.blit(text, text_rect)
        screen.blit(text1, text_rect1)
        screen.blit(text2, text_rect2)
        screen.blit(text3, text_rect3)

    pygame.display.update()

    while gameover:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == QUIT:
                gameover = False
                running = False
            if event.type == KEYDOWN:
                if event.key == K_y:
                    gameover = False
                    speed = 2
                    score = 0
                    coin_score=0
                    vagon_group.empty()
                    player.rect.center = [player_x, player_y]
                elif event.key == K_n:
                    gameover = False
                    running = False

pygame.quit()