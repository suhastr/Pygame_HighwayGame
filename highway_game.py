import pygame
import random

# Initialize Pygame
pygame.init()

# Set the window dimensions
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Set the car dimensions
CAR_WIDTH = 100
CAR_HEIGHT = 150

# Set the road dimensions
ROAD_WIDTH = 500
ROAD_HEIGHT = 1200

# Set the road position
ROAD_X = (WINDOW_WIDTH - ROAD_WIDTH) // 2
ROAD_Y = -600

# Set the car position
CAR_X = (WINDOW_WIDTH - CAR_WIDTH) // 2
CAR_Y = WINDOW_HEIGHT - CAR_HEIGHT - 50

# Set the car speed
CAR_SPEED = 10

# Set the colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# # Define font
font = pygame.font.Font(None, 36)

# Create the window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Load the car image
car_image = pygame.image.load("media/bugatti.png").convert_alpha()
car_image = pygame.transform.scale(car_image, (CAR_WIDTH, CAR_HEIGHT))

# Load the road image
road_image = pygame.image.load("media/road.PNG").convert()
road_image = pygame.transform.scale(road_image, (ROAD_WIDTH, ROAD_HEIGHT))

# Create the clock
clock = pygame.time.Clock()

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                CAR_X -= 50
            elif event.key == pygame.K_RIGHT:
                CAR_X += 50

    # Move the road
    ROAD_Y += CAR_SPEED

    # Reset the position of the road when it reaches the bottom of the window
    if ROAD_Y >= 20:
        ROAD_Y = -615

    # Draw the background
    window.blit(road_image, (ROAD_X, ROAD_Y))

    # Draw the car
    window.blit(car_image, (CAR_X, CAR_Y))


    # Update the display
    pygame.display.update()

    # Set the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()