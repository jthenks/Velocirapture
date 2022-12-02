import pygame
import random
import time
import os

pygame.init()

# Game Screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Velocirapture")
clock = pygame.time.Clock()
og_background = pygame.image.load("./media/backgrounds/landscape1.jpg")
background = pygame.transform.scale(
    og_background, (screen_width, screen_height))
time_now = 0
intro_start = True
level1_start = True
level2_start = True
level3_start = True
level4_start = True
game_over_start = True
victory_start = True
fresh_start = False

# Sound
explosion_sound = pygame.mixer.Sound('./media/sounds/Death_sound.wav')
death_sound = pygame.mixer.Sound('./media/sounds/Death.mp3')
victory_sound = pygame.mixer.Sound('./media/sounds/Victory.mp3')

# Score Board
score_value = 0
textX = 10
textY = 10

# Level text
level = 1
levelX = 318
levelY = 10

# Lives
lives = 4
temp_lives = 4
lives_delay = 0
livesX = 630
livesY = 10

# Fonts
font = pygame.font.Font("./fonts/Dino.otf", 40)
font_b = pygame.font.Font("./fonts/Dino.otf", 42)
game_over_font = pygame.font.Font('./fonts/Carta_Magna.ttf', 90)
game_over_font_b = pygame.font.Font('./fonts/Carta_Magna.ttf', 93)
game_title_font = pygame.font.Font('./fonts/Dino.otf', 80)
game_title_font_b = pygame.font.Font('./fonts/Dino.otf', 82)
game_rules_font = pygame.font.Font('./fonts/Dino.otf', 24)
game_start_font = pygame.font.Font('./fonts/Dino.otf', 40)
game_over_text_font = pygame.font.Font('./fonts/Carta_Magna.ttf', 40)
game_start_font_b = pygame.font.Font('./fonts/Dino.otf', 42)
game_start_font_c = pygame.font.Font('./fonts/Carta_Magna.ttf', 41)
game_end_font = pygame.font.Font('./fonts/Dino.otf', 90)
game_end_font_b = pygame.font.Font('./fonts/Dino.otf', 92)
game_end_score = pygame.font.Font('./fonts/Dino.otf', 60)
game_end_score_b = pygame.font.Font('./fonts/Dino.otf', 62)
game_over_score = pygame.font.Font('./fonts/Carta_Magna.ttf', 60)
game_over_score_b = pygame.font.Font('./fonts/Carta_Magna.ttf', 62)
game_over_score_num = pygame.font.Font('./fonts/GutenbergTextura.ttf', 74)

# Player
player_path_left = "./media/player/PinkWalkLeft/"
player_path_right = "./media/player/PinkWalkRight/"
count = 0
colour = "Pink"
num_of_img = 6
animation = []
l_animation = []
r_animation = []
current_frame = 1
og_dino = pygame.image.load("./media/player/PinkWalkLeft/Pink1.png")
playerImg = pygame.transform.scale(og_dino, (60, 60))
playerX = 370
playerY = screen_height-55
playerX_change = 0
going_left = False
og_blood = pygame.image.load("./media/blood/1_10.png")
blood = pygame.transform.scale(og_blood, (60, 60))
death_spot_x = 0
death_spot_y = 0
display_player = True


# Meteor initialization
og_meteor_image = pygame.image.load('media/meteors/Ice.png')
meteor_image = pygame.transform.scale(og_meteor_image, (90, 90))
meteor_list = []
SPAWNMETEOR = pygame.USEREVENT
meteor_count = 0
keep_spawning = True


# how many ms spawn timer. Changes on each level
def timer(time):
    pygame.time.set_timer(SPAWNMETEOR, time)


# display things to screen (level, score, lives)
def display(string, display, x, y):
    display_a = font.render(str(string) + ": " +
                            str(display), True, (248, 240, 227))
    display_b = font_b.render(str(string) + ": " +
                              str(display), True, (200, 0, 0))
    screen.blit(display_b, (x - 3, y + 2))
    screen.blit(display_a, (x, y))


# load animations
def load_paths(player_path):
    global l_animation
    global r_animation

    if player_path == player_path_left:
        for i in range(num_of_img):
            l_animation.append(pygame.image.load(
                os.path.join(player_path, colour + str(i + 1) + ".png")).convert_alpha())
    elif player_path == player_path_right:
        for i in range(num_of_img):
            r_animation.append(pygame.image.load(
                os.path.join(player_path, colour + str(i + 1) + ".png")).convert_alpha())


# initially load player animation
load_paths(player_path_left)
load_paths(player_path_right)


# blit player
def player(x, y):
    global going_left
    global playerImg
    global playerX_change
    global animation
    global l_animation
    global r_animation

    if going_left:
        animation = l_animation[:]
    else:
        animation = r_animation[:]

    dino = update_dino()
    playerImg = pygame.transform.scale(dino, (60, 60))

    screen.blit(playerImg, (x, y))


# takes appropriate dino image from frame
def update_dino():
    global current_frame
    global og_dino
    global animation

    current_frame += 0.075
    if current_frame >= 6:
        current_frame = 1
    og_dino = animation[int(current_frame)]
    return og_dino


def create_meteor():

    random_meteor_pos = random.randint(-250, 460)
    new_meteor = meteor_image.get_rect(midtop=(random_meteor_pos, -150))

    return new_meteor


def move_meteors(meteors, speed):
    global meteor_movement
    global screen_height

    for meteorite in meteors:
        meteor_movement = speed

        meteorite.centerx += 2
        meteorite.centery += meteor_movement

    return meteors


def draw_meteors(meteors):
    for meteorite in meteors:
        screen.blit(meteor_image, meteorite)


def check_collision(meteors):
    global playerImg
    global playerX
    global playerY
    global lives
    global time_now
    global temp_lives
    global playerX_change
    global lives_delay
    global blood
    global death_spot_x
    global meteor_list

    for meteorite in meteors:
        dino_pos = pygame.Rect(playerX + 20, playerY + 12, 20, 20)

        if dino_pos.colliderect(meteorite):
            explosion_sound.play()
            death_sound.play(0, 2000)
            meteor_list = []
            time_now = time.time()
            lives_delay = time_now + 1
            temp_lives -= 1
            death_spot_x = playerX + 10
            new_life()

    return lives_delay


# runs when player dies. Changes dino
def new_life():
    global playerImg
    global going_left
    global fresh_start
    global lives
    global colour
    global player_path_left
    global player_path_right
    global animation
    global l_animation
    global r_animation

    animation = []
    l_animation = []
    r_animation = []

    going_left = False
    if fresh_start == True:
        lives = 4
        colour = "Pink"
        player_path_left = "./media/player/PinkWalkLeft/"
        player_path_right = "./media/player/PinkWalkRight/"
        fresh_start = False
    if lives == 3:
        colour = "Blue"
        player_path_left = "./media/player/BlueWalkLeft/"
        player_path_right = "./media/player/BlueWalkRight/"
    if lives == 2:
        colour = "Grey"
        player_path_left = "./media/player/GreyWalkLeft/"
        player_path_right = "./media/player/GreyWalkRight/"
    if lives == 1:
        colour = "Green"
        player_path_left = "./media/player/GreenWalkLeft/"
        player_path_right = "./media/player/GreenWalkRight/"
    load_paths(player_path_left)
    load_paths(player_path_right)


def new_game():
    global og_dino
    global playerImg
    global playerX
    global playerY
    global playerX_change
    global going_left
    global score_value
    global lives
    global level1_start
    global level2_start
    global level3_start
    global level4_start
    global game_over_start
    global victory_start
    global intro_start
    global fresh_start
    global meteor_image
    global keep_spawning

    score_value = 0
    lives = 4
    playerX = 370
    playerY = screen_height-55
    playerX_change = 0
    going_left = False
    level1_start = True
    level2_start = True
    level3_start = True
    level4_start = True
    intro_start = True
    game_over_start = True
    victory_start = True
    fresh_start = True
    og_meteor_image = pygame.image.load('media/meteors/Ice.png')
    meteor_image = pygame.transform.scale(og_meteor_image, (90, 90))
    keep_spawning = True
    new_life()


class GameState():

    def __init__(self):
        self.state = 'intro'

    def intro(self):
        global running
        global game_start_font
        global intro_start

        if intro_start == True:
            pygame.mixer.music.stop()
            pygame.mixer.music.load("./media/sounds/opening.mp3")
            pygame.mixer.music.play(-1)
            intro_start = False

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.state = 'level_1'

        # Screen Attributes
        background = pygame.image.load("./media/backgrounds/titlepage.jpg")
        background = pygame.transform.scale(
            background, (screen_width, screen_height))
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        # start screen text
        title = game_title_font.render("Velocirapture", True, (248, 240, 227))
        title_b = game_title_font_b.render(
            "Velocirapture", True, (0, 200, 0))
        instructions = game_rules_font.render(
            "Use the left and right arrow keys", True, (248, 240, 227))
        instructions2 = game_rules_font.render(
            "to avoid extinction", True, (248, 240, 227))
        start = game_start_font.render(
            "START", True, (248, 240, 227))
        start_b = game_start_font_b.render(
            "START", True, (0, 200, 0))
        screen.blit(title_b, (92, 82))
        screen.blit(title, (100, 80))
        screen.blit(instructions, (180, 500))
        screen.blit(instructions2, (270, 530))
        screen.blit(start_b, (318, 300))
        screen.blit(start, (320, 300))

        # pygame.display.update()

    def level_1(self):
        global running
        global playerX_change
        global playerX
        global playerImg
        global going_left
        global background
        global screen
        global meteor_image
        global meteor_list
        global score_value
        global victory_sound
        global lives
        global temp_lives
        global fresh_start
        global blood
        global num_of_img
        global animation
        global display_player
        global level1_start

        # Screen Attributes
        # og_background = pygame.image.load(
        # "./media/backgrounds/landscape1.jpg")
        background = pygame.transform.scale(og_background, (800, 600))
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        # music
        if level1_start == True:
            timer(1200)
            pygame.mixer.music.stop()
            pygame.mixer.music.load("./media/sounds/AtDoomsGate.mp3")
            pygame.mixer.music.play(-1)
            level1_start = False

        # Game Events
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -7
                    if going_left == False:
                        playerImg = pygame.transform.flip(
                            playerImg, True, False)
                        going_left = True

                if event.key == pygame.K_RIGHT:
                    playerX_change = 7
                    if going_left:
                        playerImg = pygame.transform.flip(
                            playerImg, True, False)
                        going_left = False

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0
            if keep_spawning == True:
                if event.type == SPAWNMETEOR:
                    meteor_list.append(create_meteor())
                    score_value += 1
            else:
                if event.type == SPAWNMETEOR:
                    score_value += 1

        # meteor movement
        meteor_list = move_meteors(meteor_list, 3)  # 3 is speed
        draw_meteors(meteor_list)
        if fresh_start:
            meteor_list.clear()

        # collision check
        delay = check_collision(meteor_list)
        if time.time() < delay and temp_lives < lives:
            screen.blit(blood, (death_spot_x, playerY))
            display_player = False

        if time.time() > delay and temp_lives < lives:
            lives -= 1
            temp_lives = lives
            new_life()
            display_player = True

        # player movement
        playerX += playerX_change
        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736
        if playerImg == pygame.transform.scale(blood, (60, 60)):
            playerX_change = 0

        # display to screen
        if display_player == True:
            player(playerX, playerY)
        display("Score", score_value, textX, textY)
        display("Lives", lives, livesX, livesY)
        display("Level", level, levelX, levelY)

        # victory sound
        if score_value == 20:
            victory_sound.play()

    def level_2(self):
        global running
        global playerX_change
        global playerX
        global playerImg
        global going_left
        global background
        global screen
        global meteor_image
        global meteor_list
        global score_value
        global victory_sound
        global lives
        global temp_lives
        global fresh_start
        global blood
        global num_of_img
        global animation
        global display_player
        global level2_start
        global keep_spawning

        # Screen Attributes
        og_background = pygame.image.load("./media/backgrounds/landscape2.jpg")
        background = pygame.transform.scale(og_background, (800, 600))
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        # music and level 2 start items
        if level2_start == True:
            timer(550)
            meteor_list = []
            pygame.mixer.music.stop()
            pygame.mixer.music.load("./media/sounds/TransistorFist.mp3")
            pygame.mixer.music.play(-1)
            level2_start = False

        # Game Events
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -7
                    if going_left == False:
                        playerImg = pygame.transform.flip(
                            playerImg, True, False)
                        going_left = True

                if event.key == pygame.K_RIGHT:
                    playerX_change = 7
                    if going_left:
                        playerImg = pygame.transform.flip(
                            playerImg, True, False)
                        going_left = False

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0

            if keep_spawning == True:
                if event.type == SPAWNMETEOR:
                    meteor_list.append(create_meteor())
                    score_value += 1
            else:
                if event.type == SPAWNMETEOR:
                    score_value += 1

        # meteor movement
        og_meteor_image = pygame.image.load('media/meteors/Lava.png')
        meteor_image = pygame.transform.scale(og_meteor_image, (120, 120))
        meteor_list = move_meteors(meteor_list, 4)  # 4 is speed
        draw_meteors(meteor_list)
        if fresh_start:
            meteor_list.clear()

        # collision check
        delay = check_collision(meteor_list)
        if time.time() < delay and temp_lives < lives:
            screen.blit(blood, (death_spot_x, playerY))
            display_player = False

        if time.time() > delay and temp_lives < lives:
            lives -= 1
            temp_lives = lives
            new_life()
            display_player = True

        # player movement
        playerX += playerX_change
        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736
        if playerImg == pygame.transform.scale(blood, (60, 60)):
            playerX_change = 0

        # display to screen
        if display_player == True:
            player(playerX, playerY)
        display("Score", score_value, textX, textY)
        display("Lives", lives, livesX, livesY)
        display("Level", level, levelX, levelY)

        # victory sound
        if score_value == 80:
            victory_sound.play()

    def level_3(self):
        global running
        global playerX_change
        global playerX
        global playerImg
        global going_left
        global background
        global screen
        global meteor_image
        global meteor_list
        global score_value
        global victory_sound
        global lives
        global temp_lives
        global fresh_start
        global blood
        global num_of_img
        global animation
        global display_player
        global level3_start
        global keep_spawning

        # Screen Attributes
        og_background = pygame.image.load("./media/backgrounds/landscape3.jpg")
        background = pygame.transform.scale(og_background, (800, 600))
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        # music and level 2 start items
        if level3_start == True:
            timer(500)
            meteor_list = []
            pygame.mixer.music.stop()
            pygame.mixer.music.load("./media/sounds/Damnation.mp3")
            pygame.mixer.music.play(-1)
            level3_start = False

        # Game Events
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -7
                    if going_left == False:
                        playerImg = pygame.transform.flip(
                            playerImg, True, False)
                        going_left = True

                if event.key == pygame.K_RIGHT:
                    playerX_change = 7
                    if going_left:
                        playerImg = pygame.transform.flip(
                            playerImg, True, False)
                        going_left = False

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0

            if keep_spawning == True:
                if event.type == SPAWNMETEOR:
                    meteor_list.append(create_meteor())
                    score_value += 1
            else:
                if event.type == SPAWNMETEOR:
                    score_value += 1

        # meteor movement
        og_meteor_image = pygame.image.load('media/meteors/Gas.png')
        meteor_image = pygame.transform.scale(og_meteor_image, (130, 130))
        meteor_list = move_meteors(meteor_list, 4)
        draw_meteors(meteor_list)
        if fresh_start:
            meteor_list.clear()

        # collision check
        delay = check_collision(meteor_list)
        if time.time() < delay and temp_lives < lives:
            screen.blit(blood, (death_spot_x, playerY))
            display_player = False

        if time.time() > delay and temp_lives < lives:
            lives -= 1
            temp_lives = lives
            new_life()
            display_player = True

        # player movement
        playerX += playerX_change
        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736
        if playerImg == pygame.transform.scale(blood, (60, 60)):
            playerX_change = 0

        # display to screen
        if display_player == True:
            player(playerX, playerY)
        display("Score", score_value, textX, textY)
        display("Lives", lives, livesX, livesY)
        display("Level", level, levelX, levelY)

        # victory sound
        if score_value == 180:
            victory_sound.play()

    def level_4(self):
        global running
        global playerX_change
        global playerX
        global playerImg
        global going_left
        global background
        global screen
        global meteor_image
        global meteor_list
        global score_value
        global victory_sound
        global lives
        global temp_lives
        global fresh_start
        global blood
        global num_of_img
        global animation
        global display_player
        global level4_start

        # Screen Attributes
        og_background = pygame.image.load("./media/backgrounds/landscape4.jpg")
        background = pygame.transform.scale(og_background, (800, 600))
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        # music and level 2 start items
        if level4_start == True:
            timer(170)
            meteor_list = []
            pygame.mixer.music.stop()
            pygame.mixer.music.load("./media/sounds/Rip&Tear.mp3")
            pygame.mixer.music.play(-1)
            level4_start = False

        # Game Events
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -7
                    if going_left == False:
                        playerImg = pygame.transform.flip(
                            playerImg, True, False)
                        going_left = True

                if event.key == pygame.K_RIGHT:
                    playerX_change = 7
                    if going_left:
                        playerImg = pygame.transform.flip(
                            playerImg, True, False)
                        going_left = False

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0

            if keep_spawning == True:
                if event.type == SPAWNMETEOR:
                    meteor_list.append(create_meteor())
                    score_value += 1
            else:
                if event.type == SPAWNMETEOR:
                    score_value += 1

        # meteor movement
        og_meteor_image = pygame.image.load('media/meteors/Sun.png')
        meteor_image = pygame.transform.scale(og_meteor_image, (70, 70))
        meteor_list = move_meteors(meteor_list, 5)
        draw_meteors(meteor_list)
        if fresh_start:
            meteor_list.clear()

        # collision check
        delay = check_collision(meteor_list)
        if time.time() < delay and temp_lives < lives:
            screen.blit(blood, (death_spot_x, playerY))
            display_player = False

        if time.time() > delay and temp_lives < lives:
            lives -= 1
            temp_lives = lives
            new_life()
            display_player = True

        # player movement
        playerX += playerX_change
        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736
        if playerImg == pygame.transform.scale(blood, (60, 60)):
            playerX_change = 0

        # display to screen
        if display_player == True:
            player(playerX, playerY)
        display("Score", score_value, textX, textY)
        display("Lives", lives, livesX, livesY)
        display("Level", level, levelX, levelY)

        # victory sound
        if score_value == 400:
            victory_sound.play()

    def game_over(self):

        global running
        global game_start_font
        global game_over_start
        global lives
        global temp_lives

        if game_over_start == True:
            pygame.mixer.music.stop()
            pygame.mixer.music.load("./media/sounds/Death_song.mp3")
            pygame.mixer.music.play(-1)
            game_over_start = False

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                new_game()
                self.state = 'intro'
                lives = 4
                temp_lives = 4

        # Screen Attributes
        background = pygame.image.load("./media/backgrounds/lose1.jpg")
        background = pygame.transform.scale(
            background, (screen_width, screen_height))
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        # game over text
        lose = game_over_font.render("Game Over!", True, (255, 228, 225))
        lose_b = game_over_font_b.render(
            "Game Over!", True, (200, 0, 0))
        text = game_over_text_font.render(
            "Click to Restart", True, (200, 0, 0))
        score = game_over_score.render(
            "Score: ", True, (200, 0, 0))
        score_num = game_over_score_num.render(
            str(score_value), True, (200, 0, 0))
        screen.blit(lose_b, (146, 20))
        screen.blit(lose, (153, 20))
        screen.blit(text, (255, 520))
        screen.blit(score, (260, 440))
        screen.blit(score_num, (434, 445))

        # player images
        og_halo = pygame.image.load("./media/player/halo1.png")
        halo = pygame.transform.scale(og_halo, (30, 30))
        og_pink = pygame.image.load("./media/player/PinkDead.png")
        pink = pygame.transform.scale(og_pink, (60, 60))
        og_blue = pygame.image.load("./media/player/BlueDead.png")
        blue = pygame.transform.scale(og_blue, (60, 60))
        og_grey = pygame.image.load("./media/player/GreyDead.png")
        grey = pygame.transform.scale(og_grey, (60, 60))
        og_green = pygame.image.load("./media/player/GreenDead.png")
        green = pygame.transform.scale(og_green, (60, 60))
        screen.blit(halo, (280, 220))
        screen.blit(halo, (340, 220))
        screen.blit(halo, (400, 220))
        screen.blit(halo, (460, 220))
        screen.blit(pink, (265, 240))
        screen.blit(blue, (325, 240))
        screen.blit(grey, (380, 240))
        screen.blit(green, (445, 240))

        # pygame.display.update()

    def you_win(self):

        global running
        global game_start_font
        global victory_start
        global lives
        global temp_lives

        if victory_start == True:
            pygame.mixer.music.stop()
            pygame.mixer.music.load("./media/sounds/credits.mp3")
            pygame.mixer.music.play(-1)
            victory_start = False

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                new_game()
                self.state = 'intro'
                lives = 4
                temp_lives = 4

        # Screen Attributes
        background = pygame.image.load("./media/backgrounds/win.jpg")
        background = pygame.transform.scale(
            background, (screen_width, screen_height))
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        # start screen text
        win = game_end_font.render("You Win!", True, (248, 240, 227))
        win = game_end_font.render("You Win!", True, (255, 255, 255))
        win_b = game_end_font_b.render(
            "You Win!", True, (0, 200, 0))
        text = game_start_font.render(
            "Go forth and eat all the mammals.", True, (248, 240, 227))
        text2 = game_start_font.render(
            "You deserve it.", True, (248, 240, 227))
        score = game_end_score.render(
            "Score: " + str(score_value), True, (248, 240, 227))
        score_b = game_end_score_b.render(
            "Score: " + str(score_value), True, (0, 200, 0))
        screen.blit(win_b, (185, 80))
        screen.blit(win, (190, 80))
        screen.blit(text, (20, 490))
        screen.blit(text2, (250, 530))
        screen.blit(score_b, (230, 300))
        screen.blit(score, (234, 300))

        pygame.display.update()

    def state_manager(self):
        global score_value
        global background
        global og_background
        global level
        global lives
        global keep_spawning

        if lives <= 0:
            self.state = 'game_over'
            self.game_over()
        else:
            if self.state == 'intro':
                self.intro()
            if self.state == 'level_1':
                if score_value >= 16:
                    keep_spawning = False
                self.level_1()
            if score_value >= 20 and score_value < 80:
                keep_spawning = True
                level = 2
                self.state = 'level_2'
                if score_value >= 74:
                    keep_spawning = False
                self.level_2()
            if score_value >= 80 and score_value < 180:
                keep_spawning = True
                level = 3
                self.state = 'level_3'
                if score_value >= 173:
                    keep_spawning = False
                self.level_3()
            if score_value >= 180 and score_value < 400:
                keep_spawning = True
                level = 4
                self.state = 'level_4'
                if score_value >= 382:
                    keep_spawning = False
                self.level_4()
            if score_value >= 400:
                self.state = 'you_win'
                self.you_win()


game_state = GameState()

# Game Loop
running = True
while running:
    game_state.state_manager()
    pygame.display.update()
    clock.tick(60)
