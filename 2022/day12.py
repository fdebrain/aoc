import os

from aocd import get_data
from dotenv import load_dotenv

load_dotenv()


def decode_elevation(char):
    if char == "S":
        return ord("a")
    elif char == "E":
        return ord("z")
    else:
        return ord(char)


def initialize_positions(data):
    start, end = None, None

    for row in range(len(data)):
        for col in range(len(data[0])):
            elevation = data[row][col]
            if elevation == "S":
                start = [row, col]
            elif elevation == "E":
                end = [row, col]

            if start and end:
                return start, end


def evaluate_neighbors(data, current):
    row, col = current
    current_elevation = decode_elevation(data[row][col])
    filtered_neighbors = []

    # Left
    if col > 0:
        neighbor_elevation = decode_elevation(data[row][col - 1])
        if neighbor_elevation <= current_elevation + 1:
            filtered_neighbors.append([row, col - 1])

    # Top
    if row > 0:
        neighbor_elevation = decode_elevation(data[row - 1][col])
        if neighbor_elevation <= current_elevation + 1:

            filtered_neighbors.append([row - 1, col])

    # Right
    if col < len(data[0]) - 1:
        neighbor_elevation = decode_elevation(data[row][col + 1])
        if neighbor_elevation <= current_elevation + 1:
            filtered_neighbors.append([row, col + 1])

    # Bottom
    if row < len(data) - 1:
        neighbor_elevation = decode_elevation(data[row + 1][col])
        if neighbor_elevation <= current_elevation + 1:
            filtered_neighbors.append([row + 1, col])

    return filtered_neighbors


def evaluate_neighbors_backward(data, current):
    row, col = current
    current_elevation = decode_elevation(data[row][col])
    filtered_neighbors = []

    # Left
    if col > 0:
        neighbor_elevation = decode_elevation(data[row][col - 1])
        if current_elevation <= neighbor_elevation + 1:
            filtered_neighbors.append([row, col - 1])

    # Top
    if row > 0:
        neighbor_elevation = decode_elevation(data[row - 1][col])
        if current_elevation <= neighbor_elevation + 1:
            filtered_neighbors.append([row - 1, col])

    # Right
    if col < len(data[0]) - 1:
        neighbor_elevation = decode_elevation(data[row][col + 1])
        if current_elevation <= neighbor_elevation + 1:
            filtered_neighbors.append([row, col + 1])

    # Bottom
    if row < len(data) - 1:
        neighbor_elevation = decode_elevation(data[row + 1][col])
        if current_elevation <= neighbor_elevation + 1:
            filtered_neighbors.append([row + 1, col])

    return filtered_neighbors


def bfs(data, start, end):
    visited = []
    current = None
    depth = 0
    to_visit = [(start, depth)]

    while current != end:
        # Retrieve position and depth of current position
        current, depth = to_visit.pop(0)

        # Add to list of visited positions
        visited.append(current)

        # Evaluate feasibility to reach each neighbor squares
        filtered_neighbors = evaluate_neighbors(data, current)

        # Add to list of next nodes to visit (with corresponding depth)
        to_visit.extend(
            (neighbor, depth + 1)
            for neighbor in filtered_neighbors
            if neighbor not in visited and (neighbor, depth + 1) not in to_visit
        )

    return depth


def bfs_backward(data, start):
    visited = []
    current = None
    depth = 0
    to_visit = [(start, depth)]
    current_elevation = None

    while current_elevation != "a":
        # Retrieve position and depth of current position
        current, depth = to_visit.pop(0)
        current_elevation = data[current[0]][current[1]]

        # Add to list of visited positions
        visited.append(current)

        # Evaluate feasibility to reach each neighbor squares
        filtered_neighbors = evaluate_neighbors_backward(data, current)

        # Add to list of next nodes to visit (with corresponding depth)
        to_visit.extend(
            (neighbor, depth + 1)
            for neighbor in filtered_neighbors
            if neighbor not in visited and (neighbor, depth + 1) not in to_visit
        )

    return depth


if __name__ == "__main__":
    session_id = os.getenv("SESSION_ID")
    data = get_data(day=12, year=2022, session=session_id)
    data = data.split("\n")

    # Test case: Should return 31 | 29
    # data = [
    #     "Sabqponm",
    #     "abcryxxl",
    #     "accszExk",
    #     "acctuvwj",
    #     "abdefghi",
    # ]

    start, end = initialize_positions(data)

    # Part 1: What is the shortest path length from the start to the the end destination?
    print(bfs(data, start, end))

    # Part 2: What is the fewest steps required to move starting from any square with elevation a to the end destination?
    print(bfs_backward(data, end))
