import pygame
import random
# Initialize Pygame
pygame.init()
# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hydrogen Vehicle Challenge")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0) 

# Game settings
clock = pygame.time.Clock()
FPS = 60  # Frames per second
GAME_DURATION = 300  # Game duration in seconds
INITIAL_FUEL = 100  # Initial fuel level for the player

# Load assets (images)
road_background = pygame.image.load("road_background.jpg")  # Load the road background image
road_background = pygame.transform.scale(road_background, (WIDTH, HEIGHT))  # Scale the background to fit the screen
vehicle_img = pygame.image.load("car.png")  # Load the player car image
vehicle_img = pygame.transform.scale(vehicle_img, (65, 100))  # Scale the player car

# Load the image for vehicles collected
vehicle_collected_img = pygame.image.load("vehicle_collected.png")  # Load the collectible vehicle image
vehicle_collected_img = pygame.transform.scale(vehicle_collected_img, (50, 50))  # Scale the collectible vehicle

# Load the fuel pump image
fuel_pump_img = pygame.image.load("fuel_station.png")  # Load the fuel pump image
fuel_pump_img = pygame.transform.scale(fuel_pump_img, (50, 50))  # Scale the fuel pump

# Load the start screen background image
start_background = pygame.image.load("start_background.jpg")  # Make sure the image is in the right path
start_background = pygame.transform.scale(start_background, (WIDTH, HEIGHT))  # Scale to screen size

# Start screen variables
font = pygame.font.Font(None, 48)
start_button_width = 200
start_button_height = 60
start_button_rect = pygame.Rect(WIDTH // 2 - start_button_width // 2, HEIGHT // 2 - start_button_height // 2, start_button_width, start_button_height)  # Start button dimensions
start_button_color = (0, 255, 0)

# Define road boundaries
ROAD_LEFT_BOUNDARY = 165  # Left side boundary of the road
ROAD_RIGHT_BOUNDARY = WIDTH - 165  # Right side boundary of the road

# Player class
# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = vehicle_img
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 40)  # Position at the bottom of the screen
        self.speed = 7  # Movement speed of the player
        self.vehicles_collected = 0  # Track vehicles collected by the player
        self.vehicles = 10  # Number of vehicles unlocked by the player
        self.vehicle_threshold = 10  # Threshold for unlocking a new vehicle
        self.new_vehicle_message = ""  # Message displayed when unlocking a new vehicle
        self.fuel = INITIAL_FUEL  # Initial fuel level
        self.speed_up_time = None  # Time when speed is increased
        self.speed_up_duration = 60  # Speed up duration in seconds (1 minute)

    def update(self, keys):
        # Increase speed for 1 minute when 5000 vehicles are collected
        if self.vehicles_collected >= 5000 and not self.speed_up_time:
            self.speed_up_time = pygame.time.get_ticks()  # Store the current time when 5000 vehicles are collected
            self.speed = 14  # Double the speed (or set to any value you want)

        # Check if one minute has passed since the speed up
        if self.speed_up_time and pygame.time.get_ticks() - self.speed_up_time >= self.speed_up_duration * 1000:
            self.speed = 7  # Reset to normal speed
            self.speed_up_time = None  # Clear the speed up time

        # Move left and right within road boundaries
        if keys[pygame.K_LEFT] and self.rect.left > ROAD_LEFT_BOUNDARY:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < ROAD_RIGHT_BOUNDARY:
            self.rect.x += self.speed

        # Decrease fuel as the game progresses
        self.fuel -= 0.1
        if self.fuel < 0:  # Ensure fuel does not go negative
            self.fuel = 0

    def check_new_vehicle(self):
        if self.vehicles_collected >= self.vehicle_threshold * self.vehicles:
            self.vehicles += 1  # Unlock a new vehicle
            self.new_vehicle_message = f"Vehicles: {self.vehicles}"  # Update message
            print(f"New vehicle unlocked! Total vehicles: {self.vehicles}")  # Debugging message

# VehicleCollected class
class VehicleCollected(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = vehicle_collected_img  # Use the loaded vehicle image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(ROAD_LEFT_BOUNDARY, ROAD_RIGHT_BOUNDARY - self.rect.width)  # Random start position
        self.rect.y = random.randint(-100, -40)  # Start above the screen
        self.speed = random.randint(3, 6)  # Random speed for the vehicle

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:  # If the vehicle goes off the screen
            self.rect.x = random.randint(ROAD_LEFT_BOUNDARY, ROAD_RIGHT_BOUNDARY - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.speed = random.randint(3, 6)  # Reset with random speed

# FuelPump class
class FuelPump(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = fuel_pump_img  # Use the fuel pump image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(ROAD_LEFT_BOUNDARY, ROAD_RIGHT_BOUNDARY - self.rect.width)
        self.rect.y = random.randint(-200, -50)  # Start above the screen
        self.speed = random.randint(3, 5)  # Random speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.rect.x = random.randint(ROAD_LEFT_BOUNDARY, ROAD_RIGHT_BOUNDARY - self.rect.width)
            self.rect.y = random.randint(-200, -50)  # Reset above the screen

class PurpleObstacle(pygame.sprite.Sprite):
    """
    Represents purple obstacles (road barriers) that the player must avoid.
    """
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("../hydro_game/road_barrier.png")  # Load purple obstacle image
        self.image = pygame.transform.scale(self.image, (50, 50))  # Scale the obstacle
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(ROAD_LEFT_BOUNDARY, ROAD_RIGHT_BOUNDARY - self.rect.width)
        self.rect.y = random.randint(-150, -50)
        self.speed = random.randint(4, 8)  # Random speed

    def update(self):
        """
        Move the purple obstacle down and reset if it goes off the screen.
        """
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.rect.x = random.randint(ROAD_LEFT_BOUNDARY, ROAD_RIGHT_BOUNDARY - self.rect.width)
            self.rect.y = random.randint(-150, -50)
            self.speed = random.randint(4, 8)

# Sprite groups
all_sprites = pygame.sprite.Group()  # Group for all sprites
vehicles_collected = pygame.sprite.Group()  # Group for collectible vehicles
fuel_pumps = pygame.sprite.Group()  # Group for fuel pumps

player = Player()  # Create the player object
all_sprites.add(player)

# Add vehicles_collected to the game
for _ in range(5):
    vehicle_collected = VehicleCollected()
    all_sprites.add(vehicle_collected)
    vehicles_collected.add(vehicle_collected)

# Add fuel pumps
for _ in range(3):
    fuel_pump = FuelPump()
    all_sprites.add(fuel_pump)
    fuel_pumps.add(fuel_pump)

# Function to draw the start screen

def draw_start_screen():
    screen.blit(start_background, (0, 0))  # Draw the start background image

    start_text = font.render("Start Game", True, BLACK)

    # Draw the start button and center the text in it
    pygame.draw.rect(screen, start_button_color, start_button_rect)
    screen.blit(start_text, (start_button_rect.x + (start_button_width - start_text.get_width()) // 2, start_button_rect.y + (start_button_height - start_text.get_height()) // 2))

    pygame.display.flip()


# Game loop
def game_loop():
    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        # Update all sprites
        player.update(keys)
        vehicles_collected.update()
        fuel_pumps.update()

        # Check for collisions
        vehicle_collected_hit_list = pygame.sprite.spritecollide(player, vehicles_collected, True)
        for vehicle_collected in vehicle_collected_hit_list:
            player.vehicles_collected += 100
            player.check_new_vehicle()
            new_vehicle_collected = VehicleCollected()
            all_sprites.add(new_vehicle_collected)
            vehicles_collected.add(new_vehicle_collected)

        fuel_pump_hit_list = pygame.sprite.spritecollide(player, fuel_pumps, False)
        for fuel_pump in fuel_pump_hit_list:
            player.fuel = INITIAL_FUEL

        if player.fuel <= 0:
            print("Out of fuel! Game over.")
            running = False

        # Drawing
        screen.blit(road_background, (0, 0))
        all_sprites.draw(screen)

        # Draw fuel bar
        fuel_bar_width = 200
        fuel_percentage = (player.fuel / INITIAL_FUEL) * fuel_bar_width
        pygame.draw.rect(screen, GREEN, (WIDTH - fuel_bar_width - 10, 10, fuel_percentage, 20))
        pygame.draw.rect(screen, WHITE, (WIDTH - fuel_bar_width - 10, 10, fuel_bar_width, 20), 2)

        # Display collected vehicles and unlocked vehicles
        font = pygame.font.Font(None, 36)
        vehicles_collected_text = font.render(f"Vehicles Collected: {player.vehicles_collected}", True, BLACK)
        vehicles_text = font.render(f"Vehicles: {player.vehicles}", True, BLACK)
        screen.blit(vehicles_collected_text, (10, 10))
        screen.blit(vehicles_text, (10, 50))

        pygame.display.flip()

# Start screen logic
def start_screen():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    running = False
                    game_loop()  # Start the game loop

        draw_start_screen()

# Show the start screen
start_screen()

# Quit Pygame
pygame.quit()




