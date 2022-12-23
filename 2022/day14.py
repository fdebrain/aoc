import os

from aocd import get_data
from dotenv import load_dotenv

load_dotenv()


def preprocess_data(data):
    return [
        [
            [int(coord) for coord in point.split(",")]  # List of (x,y) coordinates
            for point in line.split(" -> ")  # List of lines in each path
        ]
        for line in data.split("\n")  # List of rock paths
    ]


def determine_boundaries(data, part_id):
    min_x, min_y = 500, 0
    max_x, max_y = 500, 0

    for path in data:
        x_list, y_list = list(zip(*path))

        if min(x_list) < min_x:
            min_x = min(x_list)

        if min(y_list) < min_y:
            min_y = min(y_list)

        if max(x_list) > max_x:
            max_x = max(x_list)

        if max(y_list) > max_y:
            max_y = max(y_list)

    # Source should be included
    min_x = min(500, min_x)
    max_x = max(500, max_x)

    if part_id == 2:
        min_x = min_x - max_y
        max_x = max_x + max_y
        max_y = max_y + 2

    return min_x, min_y, max_x, max_y


def fill_col(matrix, x, min_y, max_y, offset_x):
    for y in range(min_y, max_y + 1):
        matrix[y][abs(x - offset_x)] = "#"


def fill_row(matrix, y, min_x, max_x, offset_x):
    for x in range(min_x, max_x + 1):
        matrix[y][abs(x - offset_x)] = "#"


def initialize_drawing(data, min_x, min_y, max_x, max_y):
    width = max_x - min_x + 1
    height = max_y - min_y + 1
    draw_matrix = [["." for _ in range(width)] for _ in range(height)]
    offset_x = min_x

    # Rock paths as '#'
    for path in data:
        for i, start_point in enumerate(path[:-1]):
            end_point = path[i + 1]

            if start_point[0] == end_point[0]:  # Vertical rock
                x = start_point[0]
                min_y = min(start_point[1], end_point[1])
                max_y = max(start_point[1], end_point[1])
                fill_col(draw_matrix, x, min_y, max_y, offset_x)

            else:  # Horizontal rock
                y = start_point[1]
                min_x = min(start_point[0], end_point[0])
                max_x = max(start_point[0], end_point[0])
                fill_row(draw_matrix, y, min_x, max_x, offset_x)

    # Source as '+'
    draw_matrix[0][abs(500 - offset_x)] = "+"
    return draw_matrix


def show_state(draw_matrix):
    for line in draw_matrix:
        print(line)
    print()


def generate_sand_unit(matrix, offset_x):
    current_position = [0, abs(500 - offset_x)]  # Source position (0, 500)
    next_position = compute_next_sand_position(draw_matrix, current_position)
    matrix[next_position[0]][next_position[1]] = "o"
    return next_position


def is_inside(matrix, pos):
    return (
        pos[0] >= 0 and pos[1] >= 0 and pos[0] < len(matrix) and pos[1] < len(matrix[0])
    )


def compute_next_sand_position(matrix, current_position, part_id=1):
    y, x = current_position  # Position within matrix coordinate system [row, col]

    if is_inside(matrix, [y + 1, x]) and matrix[y + 1][x] == ".":
        # Down
        return [y + 1, x]
    elif is_inside(matrix, [y + 1, x - 1]) and matrix[y + 1][x - 1] == ".":
        # Diagonal left
        return [y + 1, x - 1]
    elif is_inside(matrix, [y + 1, x + 1]) and matrix[y + 1][x + 1] == ".":
        # Diagonal right
        return [y + 1, x + 1]
    elif (
        not is_inside(matrix, [y + 1, x - 1])
        or not is_inside(matrix, [y + 1, x + 1])
        or not is_inside(matrix, [y + 1, x])
    ) and part_id == 1:
        # Into the abyss
        return "out"
    else:
        # Stay still
        return [y, x]


def update_state(matrix, current_position, next_position):
    old_y, old_x = current_position
    new_y, new_x = next_position
    matrix[old_y][old_x] = "."
    matrix[new_y][new_x] = "o"


if __name__ == "__main__":
    session_id = os.getenv("SESSION_ID")
    data = get_data(day=14, year=2022, session=session_id)

    # Test case:
    # with open("tests/test_input_day14.txt", "r") as f:
    #     data = f.read()

    # Initialization
    data = preprocess_data(data)
    min_x, min_y, max_x, max_y = determine_boundaries(data, part_id=1)

    # Part 1: How many units of sand come to rest before sand starts flowing into the abyss below?
    draw_matrix = initialize_drawing(data, min_x, min_y, max_x, max_y)
    # show_state(draw_matrix)
    steps = 0
    is_out = False

    while not is_out:
        current_position = generate_sand_unit(draw_matrix, offset_x=min_x)
        next_position = []
        # show_state(draw_matrix)

        while True:
            next_position = compute_next_sand_position(draw_matrix, current_position)
            if next_position == current_position:  # Detect rest position
                steps += 1
                break
            elif next_position == "out":  # Detect outside
                is_out = True
                break

            update_state(draw_matrix, current_position, next_position)
            # show_state(draw_matrix)

            current_position = next_position

    print(steps)

    # Part 2: How many units of sand come to rest?
    min_x, min_y, max_x, max_y = determine_boundaries(data, part_id=2)
    draw_matrix = initialize_drawing(data, min_x, min_y, max_x, max_y)
    fill_row(draw_matrix, max_y, min_x, max_x, offset_x=min_x)  # Floor
    steps = 0
    is_out = False

    # show_state(draw_matrix)

    while not is_out:
        current_position = generate_sand_unit(draw_matrix, offset_x=min_x)
        next_position = []

        while True:
            next_position = compute_next_sand_position(
                draw_matrix,
                current_position,
                part_id=2,
            )
            if next_position == [0, 500 - min_x]:  # Detect rest position at source
                is_out = True
                break
            elif next_position == current_position:  # Detect rest position
                steps += 1
                break

            update_state(draw_matrix, current_position, next_position)
            # show_state(draw_matrix)

            current_position = next_position

    print(steps + 1)
