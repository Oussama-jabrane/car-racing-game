# Importing Libraries
import pygame
from pygame.locals import *
import random
from termcolor import colored, cprint

# Initializing the game
pygame.init()

# Creating the window
WIDTH = 500
HEIGHT = 500
SCREEN_SIZE = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Oussama JABRANE's Car Game")

# Game Colors
GRAY = (100, 100, 100)
GREEN = (81, 222, 60)
RED = (200, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 232, 0)

# Default Game Settings
gameover = False
speed = 2
score = 0


class Vehicle(pygame.sprite.Sprite):
    # Constructor
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)

        # Scale The Image To Fit The Lane
        image_scale = 60 / image.get_rect().width
        new_width = image.get_rect().width * image_scale
        new_height = image.get_rect().height * image_scale
        self.image = pygame.transform.scale(image, (new_width, new_height))

        self.rect = self.image.get_rect()
        self.rect.center = [x, y]


class PlayerVehicle(Vehicle):
    def __init__(self, x, y):
        image = pygame.image.load('images/car.png')
        super().__init__(image, x, y)


# Markers Size
marker_width = 10
marker_height = 50

# Road And Edge Markers
road = (100, 0, 300, HEIGHT)
left_edge_marker = (95, 0, marker_width, HEIGHT)
right_edge_marker = (395, 0, marker_width, HEIGHT)

# X Coordinates Of Lanes
left_lane = 150
center_lane = 250
right_lane = 350
lanes = [left_lane, center_lane, right_lane]

# For Animating Movement Of The Lane Markers
lane_marker_move_y = 0


# Player's Starting Coordinates
player_x = 250
player_y = 400

# Create The Player's Car
player_group = pygame.sprite.Group()
player = PlayerVehicle(player_x, player_y)
player_group.add(player)

# Load The Other Vehicle Images
image_filenames = ['ambulance.png', 'taxi.png',
                   'truck.png', 'van.png', 'mini_truck.png', 'police.png']
vehicle_images = []
for image_filename in image_filenames:
    image = pygame.image.load('images/' + image_filename)
    vehicle_images.append(image)

# Sprite Group For Vehicles
vehicle_group = pygame.sprite.Group()

# Load the Crash Image
crash = pygame.image.load('images/crash.png')
crash_rect = crash.get_rect()

# Game Loop
clock = pygame.time.Clock()
FPS = 120
running = True

while running:

    # Running The Game With 120 FPS
    clock.tick(FPS)

    # Getting Different Event Types
    for event in pygame.event.get():
        if event.type == QUIT:
            # If The Player Quits, The Game Ends
            running = False

        # Move The Car With The Right/Left Arrow Keys
        if event.type == KEYDOWN:
            if event.key == K_LEFT and player.rect.center[0] > left_lane:
                player.rect.x -= 100
            elif event.key == K_RIGHT and player.rect.center[0] < right_lane:
                player.rect.x += 100

            # Check If There's A Side Collision While Changing Lanes
            for vehicle in vehicle_group:
                if pygame.sprite.collide_rect(player, vehicle):

                    gameover = True

                    # Place The Player's Car Next To The Hitten Car
                    # And Determine Where To Position The Crash Image
                    if event.key == K_LEFT:
                        player.rect.left = vehicle.rect.right
                        crash_rect.center = [
                            player.rect.left, (player.rect.center[1] + vehicle.rect.center[1]) / 2]
                    elif event.key == K_RIGHT:
                        player.rect.right = vehicle.rect.left
                        crash_rect.center = [
                            player.rect.right, (player.rect.center[1] + vehicle.rect.center[1]) / 2]

    # Draw The Grass
    screen.fill(GREEN)

    # Draw The Road
    pygame.draw.rect(screen, GRAY, road)

    # Draw The Edge Markers
    pygame.draw.rect(screen, YELLOW, left_edge_marker)
    pygame.draw.rect(screen, YELLOW, right_edge_marker)

    # Draw The Lane Markers
    lane_marker_move_y += speed * 2
    if lane_marker_move_y >= marker_height * 2:
        lane_marker_move_y = 0
    for y in range(marker_height * -2, HEIGHT, marker_height * 2):
        pygame.draw.rect(screen, WHITE, (left_lane + 45, y +
                         lane_marker_move_y, marker_width, marker_height))
        pygame.draw.rect(screen, WHITE, (center_lane + 45, y +
                         lane_marker_move_y, marker_width, marker_height))

    # Draw The Player's Car
    player_group.draw(screen)

    # Add Up To Two Vehicles At Once
    if len(vehicle_group) < 2:

        # Ensure That There Is Enough Space Between Vehicles
        add_vehicle = True
        for vehicle in vehicle_group:
            if vehicle.rect.top < vehicle.rect.height * 1.4:
                add_vehicle = False

        # If The Space Between Vehicles Is Available
        if add_vehicle:

            # Select A Random Lane
            lane = random.choice(lanes)

            # Select A Random Vehicle Image
            image = random.choice(vehicle_images)
            vehicle = Vehicle(image, lane, HEIGHT / -2)
            vehicle_group.add(vehicle)

    # Make The Vehicles Move
    for vehicle in vehicle_group:
        vehicle.rect.y += speed

        # Remove The Vehicle Once It Gets Off Screen
        if vehicle.rect.top >= HEIGHT:
            vehicle.kill()

            # Add To Score
            score += 1

            # Speed Up The Game After Passing 8 Vehicles
            if score > 0 and score % 8 == 0:
                speed += 1

    # Draw The Vehicles
    vehicle_group.draw(screen)

    # Display The Score
    font = pygame.font.Font(pygame.font.get_default_font(), 22)
    text = font.render('Score: ' + str(score), True, WHITE)
    text_rect = text.get_rect()
    text_rect.center = (50, 30)
    screen.blit(text, text_rect)

    # Check If The Collision Is A Head Collision
    if pygame.sprite.spritecollide(player, vehicle_group, True):
        gameover = True
        crash_rect.center = [player.rect.center[0], player.rect.top]

    if gameover:
        screen.blit(crash, crash_rect)
        pygame.draw.rect(screen, RED, (0, 50, WIDTH, 100))

        font = pygame.font.Font(pygame.font.get_default_font(), 16)
        text = font.render(
            'Game Over. Wanna Play Again? (Enter Y or N)', True, WHITE)
        text_rect = text.get_rect()
        text_rect.center = (WIDTH / 2, 100)
        screen.blit(text, text_rect)

    # Displaying The Updated Frame
    pygame.display.update()

    # Check If The Player Wants To Play Again
    while gameover:

        clock.tick()

        for event in pygame.event.get():
            if event.type == QUIT:
                gameover = False
                running = False

            # Get The User Input (Y or N)
            if event.type == KEYDOWN:
                if event.key == K_y:
                    # Reset The Game
                    gameover = False
                    speed = 2
                    score = 0
                    vehicle_group.empty()
                    player.rect.center = [player_x, player_y]
                elif event.key == K_n:
                    gameover = False
                    running = False


# When The Game is Over, The Window Closes

game_over = colored('*************** GAME OVER ***************', 'red')

print("\n")
print(game_over)
print("\n")

pygame.quit()
