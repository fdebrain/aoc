import os

from aocd import get_data
from dotenv import load_dotenv

load_dotenv()


if __name__ == "__main__":
    session_id = os.getenv("SESSION_ID")
    data = get_data(day=9, year=2022, session=session_id)
    data = data.split("\n")

    action2delta = {"R": (0, 1), "L": (0, -1), "U": (1, 0), "D": (-1, 0)}

    # Part 1: How many positions does the tail of the rope visit at least once?
    H = [0, 0]  # (row, col) = (y, x) in Euclidean space
    T = [0, 0]
    unique_tail_positions = [(0, 0)]
    for action in data:
        direction, steps = action.split(" ")

        for _ in range(int(steps)):
            # Move H
            H[0] += action2delta[direction][0]
            H[1] += action2delta[direction][1]

            # Compute deltas
            dx = H[1] - T[1]
            dy = H[0] - T[0]

            # Move T
            if abs(dx) > 1 and dy == 0:
                # Horizontal
                T[1] += dx // abs(dx)
            elif abs(dy) > 1 and dx == 0:
                # Vertical
                T[0] += dy // abs(dy)
            elif (abs(dy) > 1 and abs(dx) > 0) or (abs(dy) > 0 and abs(dx) > 1):
                # Diagonal
                T[0] += dy // abs(dy)
                T[1] += dx // abs(dx)
            else:
                # No movement
                continue

            # Keep track of tail visited positions
            T_pos = tuple(T)
            if T_pos not in unique_tail_positions:
                unique_tail_positions.append(T_pos)

    print(len(unique_tail_positions))

    # Part 2: How many positions does the tail of the rope visit at least once?
    knots = {i + 1: [0, 0] for i in range(10)}
    unique_tail_positions = [(0, 0)]

    for action in data:
        direction, steps = action.split(" ")

        for _ in range(int(steps)):
            for i, pos in knots.items():
                if i == 1:  # Move head
                    pos[0] += action2delta[direction][0]
                    pos[1] += action2delta[direction][1]
                else:  # Move body
                    # Compute deltas with previous knot
                    dx = knots[i - 1][1] - pos[1]
                    dy = knots[i - 1][0] - pos[0]

                    # Move knot
                    if abs(dx) > 1 and dy == 0:
                        # Horizontal
                        pos[1] += dx // abs(dx)
                    elif abs(dy) > 1 and dx == 0:
                        # Vertical
                        pos[0] += dy // abs(dy)
                    elif (abs(dy) > 1 and abs(dx) > 0) or (abs(dy) > 0 and abs(dx) > 1):
                        # Diagonal
                        pos[0] += dy // abs(dy)
                        pos[1] += dx // abs(dx)
                    else:
                        # No movement
                        continue

                # Keep track of tail visited positions
                if i == 10:
                    T_pos = tuple(pos)
                    if T_pos not in unique_tail_positions:
                        unique_tail_positions.append(T_pos)

    print(len(unique_tail_positions))
