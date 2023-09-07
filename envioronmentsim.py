import pygame
import random

# Constants
WIDTH = 800
HEIGHT = 600
CELL_SIZE = 10
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE
FPS = 30

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Parameters
NUM_HERBIVORES = 20
NUM_PREDATORS = 5
NUM_HUMANS = 5
VEGETATION_GROWTH_RATE = 0.05  # Slower growth
MAX_VEGETATION_AGE = 200  # Vegetation lives longer
MAX_HUNGER = 100
REPRODUCTION_THRESHOLD = 60  # A bit higher threshold

class Environment:
    def __init__(self):
        self.grid = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.vegetation = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

    def add_agent(self, agent, x, y):
        self.grid[y][x] = agent

    def remove_agent(self, x, y):
        self.grid[y][x] = None

    def add_vegetation(self, x, y):
        self.vegetation[y][x] = 0

    def remove_vegetation(self, x, y):
        self.vegetation[y][x] = -1

    def grow_vegetation(self):
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.grid[y][x] is None and self.vegetation[y][x] >= 0:
                    self.vegetation[y][x] += VEGETATION_GROWTH_RATE
                    if self.vegetation[y][x] > MAX_VEGETATION_AGE:
                        self.grow_berries(x, y)
    def grow_berries(self, x, y):
        self.vegetation[y][x] = 0  # Reset the vegetation age
        # Add berries to the cell

class Agent:
    def __init__(self, environment, x, y, color):
        self.environment = environment
        self.x = x
        self.y = y
        self.color = color
        self.direction = (0, 0)  # Agent's movement direction

    def move(self):
        # Implement more realistic movement logic
        dx, dy = self.direction
        self.x += dx
        self.y += dy

        # Wrap around the grid
        self.x %= GRID_WIDTH
        self.y %= GRID_HEIGHT

        # Add some randomness to movement
        self.direction = (dx + random.choice([-1, 0, 1]), dy + random.choice([-1, 0, 1]))

    def reproduce(self):
        if self.hunger < REPRODUCTION_THRESHOLD:
            # Find all neighboring cells that are empty
            neighbors = [(dx, dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1] if self.environment.grid[(self.y+dy)%GRID_HEIGHT][(self.x+dx)%GRID_WIDTH] is None]
            if neighbors:
                # Choose a random empty neighbor and place the offspring there
                dx, dy = random.choice(neighbors)
                offspring = self.__class__(self.environment, (self.x+dx)%GRID_WIDTH, (self.y+dy)%GRID_HEIGHT)
                self.environment.add_agent(offspring, offspring.x, offspring.y)

class Herbivore(Agent):
    def __init__(self, environment, x, y):
        super().__init__(environment, x, y, GREEN)
        self.hunger = 0
        self.reproduction_age = random.randint(20, 40)

    def move(self):
        # Find all neighboring cells with vegetation
        neighbors = [(dx, dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1] if self.environment.vegetation[(self.y+dy)%GRID_HEIGHT][(self.x+dx)%GRID_WIDTH] > 0]
        if neighbors:
            # Choose a random neighbor with vegetation and move towards it
            self.direction = random.choice(neighbors)
        super().move()  # Call the parent move method

    def eat(self):
        # Implement herbivore-vegetation interaction
        if self.environment.vegetation[self.y][self.x] > 0:
            self.environment.remove_vegetation(self.x, self.y)
            self.hunger -= 10  # Herbivores get full by eating vegetation

    def reproduce(self):
        super().reproduce()  # Call the parent reproduce method
        pass

class Predator(Agent):
    def __init__(self, environment, x, y):
        super().__init__(environment, x, y, RED)
        self.hunger = 0
        self.reproduction_age = random.randint(30, 50)

    def move(self):
        # Find all neighboring cells with herbivores
        neighbors = [(dx, dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1] if isinstance(self.environment.grid[(self.y+dy)%GRID_HEIGHT][(self.x+dx)%GRID_WIDTH], Herbivore)]
        if neighbors:
            # Choose a random neighbor with a herbivore and move towards it
            self.direction = random.choice(neighbors)
        super().move()  # Call the parent move method

    def hunt(self):
        # Eat the herbivore if there is one in the current cell
        if isinstance(self.environment.grid[self.y][self.x], Herbivore):
            self.environment.remove_agent(self.x, self.y)
            self.hunger -= 10  # Predators get full by eating herbivores

    def reproduce(self):
        super().reproduce()  # Call the parent reproduce method
        pass

class Human(Agent):
    def __init__(self, environment, x, y):
        super().__init__(environment, x, y, BLUE)
        self.hunger = 0
        self.reproduction_age = random.randint(25, 35)

    def move(self):
        super().move()  # Call the parent move method
        # Implement human-specific movement logic here
        pass

    def hunt(self, grid):
        # Implement human-specific hunting logic here
        pass

    def eat(self):
        # Implement human-specific eating logic here
        pass

    def reproduce(self):
        # Implement human reproduction logic here
        pass

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ecosystem Simulation")
clock = pygame.time.Clock()

# Create an environment
env = Environment()

# Add agents to the environment
for _ in range(NUM_HERBIVORES):
    x = random.randint(0, GRID_WIDTH - 1)
    y = random.randint(0, GRID_HEIGHT - 1)
    herbivore = Herbivore(env, x, y)
    env.add_agent(herbivore, x, y)

for _ in range(NUM_PREDATORS):
    x = random.randint(0, GRID_WIDTH - 1)
    y = random.randint(0, GRID_HEIGHT - 1)
    predator = Predator(env, x, y)
    env.add_agent(predator, x, y)

for _ in range(NUM_HUMANS):
    x = random.randint(0, GRID_WIDTH - 1)
    y = random.randint(0, GRID_HEIGHT - 1)
    human = Human(env, x, y)
    env.add_agent(human, x, y)

# Simulation loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update agent behaviors
    for row in env.grid:
        for agent in row:
            if isinstance(agent, Herbivore):
                agent.move()
                agent.eat()
                agent.reproduce()
            elif isinstance(agent, Predator):
                agent.move()
                agent.hunt(env.grid)
                agent.reproduce()
            elif isinstance(agent, Human):
                agent.move()
                agent.hunt(env.grid)
                agent.eat()
                agent.reproduce()

    # Update the state of trees and vegetation
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if env.vegetation[y][x] == -1:
                env.grow_vegetation()
            elif random.random() < 0.1:
                env.add_vegetation(x, y)

    # Clear the screen
    screen.fill(WHITE)

    # Draw agents and vegetation
    for row in env.grid:
        for agent in row:
            if agent:
                pygame.draw.rect(screen, agent.color, (agent.x * CELL_SIZE, agent.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if env.vegetation[y][x] >= 0:
                color = (0, int(env.vegetation[y][x] * 2.55), 0)  # Gradual color change for vegetation
                pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Update the display
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()