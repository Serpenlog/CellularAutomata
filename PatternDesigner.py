import pygame

class PatternDesigner:
    def __init__(self, rows, cols, cell_size=10):
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]
        self.width = cols * cell_size
        self.height = rows * cell_size
        self.screen = pygame.display.set_mode((self.width, self.height))

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.output_pattern()
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    row, col = y // self.cell_size, x // self.cell_size
                    self.grid[row][col] = 1 if self.grid[row][col] == 0 else 0

            self.screen.fill((255, 255, 255))  # White background
            self.draw_grid()
            pygame.display.flip()

    def draw_grid(self):
        for row in range(self.rows):
            for col in range(self.cols):
                color = (0, 0, 0) if self.grid[row][col] == 1 else (255, 255, 255)
                rect = (col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, (200, 200, 200), rect, 1)

    def output_pattern(self):
        active_cells = [(row, col) for row in range(self.rows) for col in range(self.cols) if self.grid[row][col] == 1]
        print("Pattern Coordinates:", active_cells)

# Initialize Pygame
pygame.init()

# Create a Pattern Designer instance and run it
designer = PatternDesigner(50, 50)  # Adjust grid size as needed
designer.run()

# Quit Pygame when done
pygame.quit()
