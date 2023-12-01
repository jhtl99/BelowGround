def bfs(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    queue = [(start, [start])]

    while queue:
        current, path = queue.pop(0)
        row, col = current

        if current == goal:
            return path

        if 0 <= row < rows and 0 <= col < cols and not visited[row][col] and grid[row][col] != 1:
            visited[row][col] = True

            # Define possible moves (up, down, left, right)
            moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]

            for move in moves:
                new_row, new_col = row + move[0], col + move[1]
                new_position = (new_row, new_col)

                if 0 <= new_row < rows and 0 <= new_col < cols and not visited[new_row][new_col] and grid[new_row][new_col] != 1:
                    queue.append((new_position, path + [new_position]))

    return None  # If no path is found


# Example usage:
grid = [
    [0, 0, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0]
]

start_position = (0, 0)
goal_position = (4, 4)

result = bfs(grid, start_position, goal_position)

if result:
    print(f"Path from {start_position} to {goal_position}: {result}")
else:
    print("No path found.")
