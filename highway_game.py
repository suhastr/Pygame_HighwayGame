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
CAR_SPEED = 15
MAX_CAR_SPEED = 30
# Set the colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


# Define font
font = pygame.font.Font(None, 30)



# Create the window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
surface = pygame.Surface((WINDOW_WIDTH,WINDOW_HEIGHT))

# Load the car image
car_image = pygame.image.load("media/bugatti.png").convert_alpha()
car_image = pygame.transform.scale(car_image, (CAR_WIDTH, CAR_HEIGHT))

# Load the road image
road_image = pygame.image.load("media/road.PNG").convert()
road_image = pygame.transform.scale(road_image, (ROAD_WIDTH, ROAD_HEIGHT))


# Load the booster image and create a booster sprite
booster_image = pygame.image.load("media/fuel.jpg").convert_alpha()
booster_image = pygame.transform.scale(booster_image, (20,20))
class Booster(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = booster_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(ROAD_X, ROAD_WIDTH - self.rect.width)
        self.rect.y = random.randint(-500, -50)

    def update(self):
        self.rect.y += 3
        if self.rect.y > ROAD_HEIGHT:
            self.kill()

# create a car sprite
class Car(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = car_image
            self.rect = self.image.get_rect()
            


# Create a sprite group for the boosters
booster_group = pygame.sprite.Group()

# Create a sprite group for the car
car_group = pygame.sprite.Group()


# initialize the fuel
fuel_capacity = 100
mileage = 5
destination_distance = 520


# Create the clock
clock = pygame.time.Clock()
screen = pygame.display.get_surface()
# Main game loop
running = True

# booster count
boost_count = 0
obj = Car()

#define flags
boosterFlag = True
gameFinished = False
fuelEmpty = False
remaining_fuel = 0



while running:
    # show car speed
    surface.fill(BLACK)
    speed_text = font.render("CAR SPEED", True, WHITE)
    surface.blit(speed_text, (10, 10))
    speed_text = font.render(str(CAR_SPEED),True,RED)
    surface.blit(speed_text,(18,30))


    # fuel consumption 
    distance_travelled = int(CAR_SPEED) * (pygame.time.get_ticks() // 1000)
    fuel_consumed = distance_travelled/mileage


    if fuel_consumed<fuel_capacity and gameFinished==False:
        remaining_fuel = fuel_capacity-fuel_consumed
        fuel_text = font.render("Fuel:"+ str(remaining_fuel), True, WHITE)
        surface.blit(fuel_text, (20, 50))
        # Move the road
        ROAD_Y += CAR_SPEED
    elif fuel_consumed>fuel_capacity:
        fuel_text = font.render("Fuel:"+ str(0), True, WHITE)
        surface.blit(fuel_text, (20, 50))
        fuelEmpty=True
        # stop the road
        ROAD_Y = 0 
        boosterFlag = False
    elif gameFinished:
        fuel_text = font.render("Fuel:"+ str(remaining_fuel), True, WHITE)
        surface.blit(fuel_text, (20, 50))
    if distance_travelled>destination_distance:
        boosterFlag = False
        gameFinished = True
        ROAD_Y = 0
    else:
        # distance travelled
        distace_text = font.render("Distance : "+str(destination_distance-distance_travelled),True,RED)
        surface.blit(distace_text,(10,70))

    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                CAR_X -= 50
            elif event.key == pygame.K_RIGHT:
                CAR_X += 50
            elif event.key == pygame.K_UP:
                if CAR_SPEED<30:
                    CAR_SPEED+=5
            elif event.key == pygame.K_DOWN:
                if CAR_SPEED>15:
                    CAR_SPEED-=5
                

    

    # Reset the position of the road when it reaches the bottom of the window
    if ROAD_Y >= 20:
        ROAD_Y = -615



    obj.rect.x = CAR_X
    obj.rect.y = CAR_Y
    car_group.add(obj)
    car_group.update()


    # Draw the background and check against flags
    if gameFinished:
        surface.blit(road_image, (ROAD_X, ROAD_Y))
        car_group.draw(surface)
        font_text = pygame.font.SysFont("Arial", 36)
        level_text = font_text.render("RACE COMPLETED", True, GREEN)
        surface.blit(level_text, (WINDOW_WIDTH//2-level_text.get_width()//2,WINDOW_HEIGHT//2-level_text.get_width()//2))
    elif fuelEmpty:
        surface.blit(road_image, (ROAD_X, ROAD_Y))
        car_group.draw(surface)
        font_text = pygame.font.SysFont("Arial", 36)
        level_text = font_text.render("FUEL EMPTY", True, RED)
        surface.blit(level_text, (WINDOW_WIDTH//2-level_text.get_width()//2,WINDOW_HEIGHT//2-level_text.get_width()//2))

    else:
        surface.blit(road_image, (ROAD_X, ROAD_Y))

        car_group.draw(surface)


    

    if boosterFlag:
        # Spawn a new booster at random intervals
        if random.randint(0, 60) == 0:
            booster = Booster()
            booster_group.add(booster)

        # Update the booster sprites
        booster_group.update()
        booster_group.draw(surface)

        boosterList = booster_group.sprites()
        car_rect = car_group.sprites()

        # Detect the collision
        if boosterList!=[]:
            for i in boosterList:
                if pygame.Rect.colliderect(obj.rect,i.rect):
                    fuel_capacity+=1
                    i.kill()

    screen.blit(surface, (0, 0))

    # Update the display

    pygame.display.update()

    # Set the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()