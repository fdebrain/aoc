import os

from aocd import get_data
from dotenv import load_dotenv

load_dotenv()


if __name__ == "__main__":
    session_id = os.getenv("SESSION_ID")
    data = get_data(day=8, year=2022, session=session_id)
    data = data.split("\n")
    data = [[int(cell) for cell in line] for line in data]

    # Part 1: How many trees are visible from outside the grid?
    visibility_grid = [[False for _ in line] for line in data]

    # Visible from left to right
    for row in range(len(data)):
        top_tree = -1
        for col in range(len(data[0])):
            tree = data[row][col]
            if tree > top_tree:
                visibility_grid[row][col] = True
                top_tree = tree

    # Visible from right to left
    for row in range(len(data)):
        top_tree = -1
        for col in range(len(data[0]))[::-1]:
            tree = data[row][col]
            if tree > top_tree:
                visibility_grid[row][col] = True
                top_tree = tree

    # Visible from top to bottom
    for col in range(len(data[0])):
        top_tree = -1
        for row in range(len(data)):
            tree = data[row][col]
            if tree > top_tree:
                visibility_grid[row][col] = True
                top_tree = tree

    # Visible from bottom to top
    for col in range(len(data[0])):
        top_tree = -1
        for row in range(len(data))[::-1]:
            tree = data[row][col]
            if tree > top_tree:
                visibility_grid[row][col] = True
                top_tree = tree

    print(sum(sum(line) for line in visibility_grid))

    # Part 2: What is the highest scenic score possible for any tree?
    def compute_scenic_score(data, current_row, current_col):
        current_tree = data[current_row][current_col]
        visibilities = {"left": 0, "right": 0, "top": 0, "bottom": 0}

        # Visibility on the top
        for row in range(0, current_row)[::-1]:
            tree = data[row][current_col]
            visibilities["top"] += 1
            if tree >= current_tree:  # Blocking tree
                break

        # Visibility on the bottom
        for row in range(current_row + 1, len(data)):
            tree = data[row][current_col]
            visibilities["bottom"] += 1
            if tree >= current_tree:
                break

        # Visibility on the left
        for col in range(0, current_col)[::-1]:
            tree = data[current_row][col]
            visibilities["left"] += 1
            if tree >= current_tree:
                break

        # Visibility on the right
        for col in range(current_col + 1, len(data[0])):
            visibilities["right"] += 1
            tree = data[current_row][col]
            if tree >= current_tree:
                break

        return (
            visibilities["left"]
            * visibilities["right"]
            * visibilities["top"]
            * visibilities["bottom"]
        )

    top_scenic_score = 0
    for row in range(len(data)):
        for col in range(len(data[0])):
            score = compute_scenic_score(data, row, col)
            if score > top_scenic_score:
                top_scenic_score = score

    print(top_scenic_score)
