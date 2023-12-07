from Patterns import patterns
class GameOfLife:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]
        self.history = []
        self.survival_rules = [2, 3]
        self.birth_rules = [3]

    def set_cell(self, row, col, state):
        """ Set the state of a cell. """
        self.grid[row][col] = state

    def count_neighbors(self, row, col):
        """ Count the number of live neighbors around a given cell. """
        neighbors = [(row-1, col-1), (row-1, col), (row-1, col+1),
                     (row, col-1),                 (row, col+1),
                     (row+1, col-1), (row+1, col), (row+1, col+1)]
        count = 0
        for r, c in neighbors:
            if 0 <= r < self.rows and 0 <= c < self.cols:
                count += self.grid[r][c]
        return count

    def update(self):
        """ Update the grid based on the Game of Life rules. """
        self.history.append([row[:] for row in self.grid])  # Save a copy of the grid
        if len(self.history) > 100:
            self.history.pop(0)

        new_grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

        for row in range(self.rows):
            for col in range(self.cols):
                live_neighbors = self.count_neighbors(row, col)
                # Rule: Any live cell with fewer than two live neighbors dies
                if self.grid[row][col] == 1 and live_neighbors in self.survival_rules:
                    new_grid[row][col] = 1
                # Rule: Any dead cell with exactly three live neighbors becomes a live cell
                elif self.grid[row][col] == 0 and live_neighbors in self.birth_rules:
                    new_grid[row][col] = 1
                # Else, the cell remains or becomes dead

        self.grid = new_grid

    def display(self):
        """ Display the grid in a text format. """
        for row in self.grid:
            print(' '.join(str(cell) for cell in row))
        print()

    def set_pattern(self, pattern_name):
        """ Set a predefined pattern on the grid. """
        if pattern_name in patterns:
            pattern = patterns[pattern_name]

            # Find the center of the grid
            center_row = self.rows // 2
            center_col = self.cols // 2

            # Find the pattern's size to adjust its position
            max_row = max([cell[0] for cell in pattern])
            max_col = max([cell[1] for cell in pattern])
            start_row = center_row - max_row // 2
            start_col = center_col - max_col // 2

            # Set cells based on adjusted coordinates
            for row, col in pattern:
                self.set_cell(start_row + row, start_col + col, 1)

    def revert(self):
        """ Revert the grid to the previous state. """
        if self.history:
            self.grid = self.history.pop()

    def set_rules(self, survival_rules, birth_rules):
        """ Set the survival and birth rules. """
        self.survival_rules = survival_rules
        self.birth_rules = birth_rules
