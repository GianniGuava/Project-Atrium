import pygame
import random
import sys

# TO DO:
#   Cell sight implementation
#   Eating mechanism implementation
#   Respawn food

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 30
BG_COLOR = (0, 0, 0)  # Black background

class Cell:    
    # Cell constants
    speed:  int = 2                 # Speed in pixels/sec
    sight:  int = 20                # Sight range in pixels
    size:   int = 5                 # Radius in pixels
    color:  tuple = (255, 255, 255) # Color in RGB
    
    def __init__(self, x: int, y: int):
        self.x              = x             # x-Position on board
        self.y              = y             # y-position on board
        self.life:      int = (10 * FPS)    # Life span in seconds
        self.direction: int = random.randint(1,8)
        
    #Initialize on game board
    def draw(self, surface):
        pygame.draw.circle(surface, Cell.color, (self.x, self.y), Cell.size)
        
    def is_dead(self):
        return self.life <= 0
        
    def decay(self):
        self.life -= 1
    
    #def eat()          Eats a Food object and deletes it (Maybe calls deconstructor?)
    #adds 25 seconds to life span
 
    def boundary_check(self):
        if self.x == 0 & self.y == 0:   # Top Left
            self.direction = 5
        elif self.x == 800 & self.y == 0:   # Top right
            self.direction = 7
        elif self.x == 0 & self.y == 600:   # Bottom left
            self.direction = 3
        elif self.x == 800 & self.y == 600:   # Bottom right
            self.direction = 1
            
        elif self.x == 0:   # Left
            self.direction = random.randint(3,5)
        elif self.y == 0:   # Top
            self.direction = random.randint(5,7)
        elif self.x == 800: # Right
            self.direction = random.randint(7, 9)
            if self.direction == 9:
                self.direction = 1
        elif self.y == 600: # Bottom
            self.direction = random.randint(1,3)
            
    def move(self):         
        match self.direction:
            case 1: # Up Left
                self.x -= 1
                self.y -= 1
            case 2: # Up
                self.y -= 1
            case 3: # Up Right
                self.x += 1
                self.y -= 1
            case 4: # Right
                self.x += 1
            case 5: # Down Right
                self.x += 1
                self.y += 1
            case 6: # Down
                self.y += 1
            case 7: # Down Left
                self.x -= 1
                self.y += 1
            case 8: # Left
                self.x -= 1        
    
    def __del__(self):
        print("Cell Removed")

class Food:
    # Food constants
    size:   int = 8
    color:  tuple = (0, 255, 0)     # Color in RGB
    
    def __init__(self, x: int, y: int):
        self.x: int = x                 # x-Position on board
        self.y: int = y                 # y-position on board
    
    def draw(self, surface):
        pygame.draw.rect(surface, Food.color, (self.x, self.y, Food.size, Food.size))
        
    def __del__(self):
        print("Food Removed")
        
def main():
    # Initializing pygame board
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Test: Petri Dish")
    clock = pygame.time.Clock()
    
    pygame.font.init()
    font = pygame.font.SysFont('Arial', 24)
    tick_count = 0
    
    # Create initial cells and food
    # TO DO:
    #   Fix random spawning so that nothing spawns on top of each other
    cells = [Cell(random.randint((Cell.size), SCREEN_WIDTH - (Cell.size)), random.randint((Cell.size), SCREEN_HEIGHT - (Cell.size))) for _ in range(10)]
    food_items = [Food(random.randint((Food.size), SCREEN_WIDTH - (Food.size)), random.randint((Food.size), SCREEN_HEIGHT - (Food.size))) for _ in range(20)]

    running = True
    while running:
        clock.tick(FPS)
        tick_count += 1

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Draw background
        screen.fill(BG_COLOR)

        # Draw food
        for food in food_items:
            food.draw(screen)

        # Draw cells
        for cell in cells:
            cell.decay()
            cell.boundary_check()
            cell.move()
            cells = [cell for cell in cells if not cell.is_dead()]
            cell.draw(screen)

        # Timers
        tick_text = font.render(f'Ticks: {tick_count}', True, (255, 255, 255))
        screen.blit(tick_text, (10, 10))
        seconds_passed = tick_count/FPS
        seconds_text = font.render(f'Seconds: {seconds_passed}', True, (255, 255, 255))
        screen.blit(seconds_text, (10, 40))
        
        # Update display
        pygame.display.flip()

    pygame.quit()
    sys.exit()
    
if __name__ == "__main__":
    main()