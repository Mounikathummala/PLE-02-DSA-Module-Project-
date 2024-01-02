import tkinter as tk
import random

class MazeGenerator:
    def __init__(self, size):
        self.rows, self.cols = size, size
        self._LabWidth = 600
        self._cell_width = self._LabWidth // size
        self._root = tk.Tk()
        self._canvas = tk.Canvas(self._root, width=self._LabWidth, height=self._LabWidth)
        self._canvas.pack()

    def maze_generation(self, size):
        self.rows, self.cols = size, size
        self._cell_width = self._LabWidth // size
        maze = [[1] * self.cols for _ in range(self.rows)]
        stack = [(0, 0)]
        visited = set(stack)

        while stack:
            x, y = stack[-1]
            maze[x][y] = 0  # Mark the path
            neighbors = [(x + dx, y + dy) for dx, dy in [(0, 2), (2, 0), (0, -2), (-2, 0)]]
            unvisited_neighbors = [(nx, ny) for nx, ny in neighbors if 0 <= nx < self.rows and 0 <= ny < self.cols and (nx, ny) not in visited]

            if unvisited_neighbors:
                nx, ny = random.choice(unvisited_neighbors)
                wall_x, wall_y = (x + nx) // 2, (y + ny) // 2
                maze[wall_x][wall_y] = 0  # Mark the wall between cells
                stack.append((nx, ny))
                visited.add((nx, ny))
            else:
                stack.pop()

        return maze

    def maze_printing(self, maze):
        for i in range(self.rows):
            for j in range(self.cols):
                x = j * self._cell_width
                y = i * self._cell_width

                # Display walls in black, non-wall cells in white with black borders
                fill_color = 'black' if maze[i][j] == 1 else 'white'
                border_color = 'black'

                self._canvas.create_rectangle(
                    y, x,
                    y + self._cell_width, x + self._cell_width,
                    fill=fill_color, outline=border_color
                )

    def get_canvas(self):
        return self._canvas

    def destroy(self):
        self._root.destroy()


class MazeSolver:
    def __init__(self, canvas, maze):
        self.maze = maze
        self.rows = len(maze)
        self.cols = len(maze[0])
        self._LabWidth = 60
        self.cell_width = self._LabWidth
        # Adjust the cell size here
        self.canvas_width = self.cols * self.cell_width
        self.canvas_height = self.rows * self.cell_width
        self.win = tk.Tk()  # Use Tk() instead of Toplevel()
        self.win.geometry(f"{self.canvas_width}x{self.canvas_height}")
        self.canvas = tk.Canvas(self.win, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()
        self.path = []

    def path_finding(self, start, end):
        visited = [[False] * self.cols for _ in range(self.rows)]
        self.path = []
        self._dfs(start[0], start[1], end[0], end[1], visited)

    def maze_printing(self):
        for i in range(self.rows):
            for j in range(self.cols):
                x = j * self.cell_width
                y = i * self.cell_width
                fill_color = 'black' if self.maze[i][j] == 1 else 'white'
                border_color = 'black'
                self.canvas.create_rectangle(
                    y, x,
                    y + self.cell_width, x + self.cell_width,
                    fill=fill_color, outline=border_color
                )

    def _dfs(self, x, y, end_x, end_y, visited):
        if x < 0 or x >= self.rows or y < 0 or y >= self.cols or visited[x][y] or self.maze[x][y] == 1:
            return False

        visited[x][y] = True
        self.path.append((x, y))

        if x == end_x and y == end_y:
            return True

        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up

        for dx, dy in directions:
            if self._dfs(x + dx, y + dy, end_x, end_y, visited):
                return True

        self.path.pop()
        return False

    def path_printing(self, delay=300):
        for point in self.path:
            x = point[1] * self.cell_width
            y = point[0] * self.cell_width

            fill_color = 'red' if self.maze[point[0]][point[1]] == 0 else 'black'
            border_color = 'red' if self.maze[point[0]][point[1]] == 0 else 'black'

            self.canvas.create_rectangle(
                y, x,
                y + self.cell_width, x + self.cell_width,
                fill=fill_color, outline=border_color
            )

            self.canvas.update()
            self.win.after(delay)

        self.win.update()
        self.win.protocol("WM_DELETE_WINDOW", self.close_window)  # Bind close event

    def close_window(self):
        self.win.destroy()


def main():
    size = int(input("Enter the size of the maze (odd number): "))
    if size % 2 == 0:
        print("Please enter an odd number for maze size.")
        return

    maze_generator = MazeGenerator(size)
    canvas = maze_generator.get_canvas()

    maze = maze_generator.maze_generation(size)
    maze_generator.maze_printing(maze)
    canvas.update()

    while True:
        print("Options:")
        print("1. Regenerate the maze")
        print("2. Display the path")
        print("3. Exit")
        option = input("Enter your choice: ")

        if option == '1':
            # Close the existing Tkinter window in the generator
            

            # Ask for a new size and create a new maze
            size = int(input("Enter the size of the maze (odd number): "))
            if size % 2 == 0:
                print("Please enter an odd number for maze size.")
                continue
            
            maze_generator.destroy()
            maze_generator = MazeGenerator(size)
            canvas = maze_generator.get_canvas()
            maze = maze_generator.maze_generation(size)
            maze_generator.maze_printing(maze)
            canvas.update()
        elif option == '2':
            # Maze solving and path display
            # Inside the MazeGenerator class
            maze_solver = MazeSolver(canvas, maze)
            maze_solver.maze_printing()
            start_position = (0, 0)
            end_position = (size - 1, size - 1)
            maze_solver.path_finding(start_position, end_position)
            
            maze_solver.path_printing()
            canvas.update()
        elif option == '3':
            exit(0)

    canvas.mainloop()


if __name__ == "__main__":
    main()
