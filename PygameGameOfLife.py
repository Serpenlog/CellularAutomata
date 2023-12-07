import pygame
from GameOfLife import GameOfLife
from Patterns import patterns
from InputBox import InputBox

class PygameGameOfLife(GameOfLife):
    def __init__(self, rows, cols, cell_size=10, pattern=None):
        super().__init__(rows, cols)
        self.cell_size = cell_size
        self.width = cols * cell_size
        self.height = rows * cell_size
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Game of Life')
        self.running = False

        if pattern:
            self.set_pattern(pattern)  # Initialize the pattern

    def show_menu(self):
        # Define menu properties
        font = pygame.font.Font(None, 36)
        title = font.render("Game of Life", True, (0, 0, 0))
        buttons = [("Select Pattern", self.show_pattern_selection),
                   ("Edit Rules", self.show_rule_editor)]  # Placeholder for rule editor
        button_height = 40
        menu_width = 200
        menu_height = button_height * len(buttons) + 60  # Extra space for title

        # Calculate menu position
        menu_x = (self.width - menu_width) // 2
        menu_y = (self.height - menu_height) // 2

        # Event loop for the menu
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    return None
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if menu_x <= x <= menu_x + menu_width:
                        index = (y - menu_y - 60) // button_height
                        if 0 <= index < len(buttons):
                            return buttons[index][1]()  # Call the associated function

            self.screen.fill((255, 255, 255))  # White background

            # Draw title
            self.screen.blit(title, (menu_x, menu_y))

            # Draw buttons
            for i, (label, _) in enumerate(buttons):
                text = font.render(label, True, (0, 0, 0))
                self.screen.blit(text, (menu_x, menu_y + 60 + i * button_height))

            pygame.display.flip()

    def show_pattern_selection(self):
        # Define properties for the pattern selection
        font = pygame.font.Font(None, 36)
        pattern_names = list(patterns.keys())
        button_height = 40
        menu_width = 200
        scroll_y = 0


        # Calculate menu position
        menu_x = (self.width - menu_width) // 2
        menu_y = 50

        # Event loop for the pattern selection
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    return None
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse click
                        x, y = event.pos
                        if menu_x <= x <= menu_x + menu_width:
                            index = (y - menu_y + scroll_y) // button_height
                            if 0 <= index < len(pattern_names):
                                return pattern_names[index]
                    elif event.button == 4:  # Scroll up
                        scroll_y = max(scroll_y - button_height, 0)
                    elif event.button == 5:  # Scroll down
                        max_scroll = max(0, len(pattern_names) * button_height - self.height)
                        scroll_y = min(scroll_y + button_height, max_scroll)

            self.screen.fill((255, 255, 255))  # White background

            # Draw pattern names
            for i, pattern in enumerate(pattern_names):
                text = font.render(pattern, True, (0, 0, 0))
                self.screen.blit(text, (menu_x, menu_y + i * button_height - scroll_y))

            pygame.display.flip()

    def show_rule_editor(self):
        font = pygame.font.Font(None, 36)
        input_box1 = InputBox(100, 100, 140, 32, font)  # For survival rules
        input_box2 = InputBox(100, 200, 140, 32, font)  # For birth rules
        done = False
        survival_rules = None
        birth_rules = None

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return  # Exit without saving if the window is closed

                # Handle input for each box
                input1 = input_box1.handle_event(event)
                input2 = input_box2.handle_event(event)
                if input1 is not None:
                    survival_rules = input1
                if input2 is not None:
                    birth_rules = input2

            # Check if both inputs have been entered
            if survival_rules is not None and birth_rules is not None:
                # Convert inputs to sets of integers and set rules
                try:
                    self.set_rules({int(x.strip()) for x in survival_rules.split(',')},
                                   {int(x.strip()) for x in birth_rules.split(',')})
                except ValueError:
                    # Handle invalid input
                    print("Invalid input. Please enter numbers separated by commas.")
                    survival_rules = None
                    birth_rules = None
                    continue

                return  # Return to main menu after setting rules

            self.screen.fill((255, 255, 255))  # White background
            input_box1.draw(self.screen)
            input_box2.draw(self.screen)
            pygame.display.flip()

    def run(self):
        """ Main loop for the game. """
        pattern = self.show_menu()
        if pattern:
            self.set_pattern(pattern)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.running = not self.running  # Toggle simulation running state
                    elif event.key == pygame.K_RIGHT:
                        self.update()  # Advance one generation
                    elif event.key == pygame.K_LEFT:
                        self.revert()  # Revert to previous generation

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    row, col = y // self.cell_size, x // self.cell_size
                    self.grid[row][col] = 1 if self.grid[row][col] == 0 else 0  # Toggle cell state

            if self.running:
                self.update()  # Update the grid if the simulation is running

            self.screen.fill((255, 255, 255))  # White background
            self.draw_grid()
            pygame.display.flip()
            pygame.time.delay(100)

    def draw_grid(self):
        """ Draw the grid on the screen. """
        for row in range(self.rows):
            for col in range(self.cols):
                color = (0, 0, 0) if self.grid[row][col] == 1 else (
                255, 255, 255)  # Black for live cells, white for dead
                rect = (col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, (200, 200, 200), rect, 1)  # Cell borders

# Initialize Pygame
pygame.init()

# Create a game instance and run it
game = PygameGameOfLife(50, 50)  # 50x50 grid with default cell size
game.run()

# Quit Pygame when done
pygame.quit()
