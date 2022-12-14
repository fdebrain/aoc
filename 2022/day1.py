import os

from aocd import get_data
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    session_id = os.getenv("SESSION_ID")
    data = get_data(day=1, year=2022, session=session_id)
    data = data.split("\n")

    # Part 1: Find the Elf carrying the most Calories. How much is he/she carrying?
    sum_max = 0
    sum_buffer = 0

    for val in data:
        # Detect new Elf -> reset buffer
        if not val:
            sum_buffer = 0
            continue

        # Update buffer
        sum_buffer += int(val)

        # Update max
        if sum_buffer > sum_max:
            sum_max = sum_buffer

    print(sum_max)

    # Part 2: Find the 3 Elves carrying the most Calories. How much do they carry in total?
    sum_max = [0, 0, 0]
    sum_buffer = 0

    for val in data:
        # Detect new Elf -> reset buffer
        if not val:
            sum_buffer = 0
            continue

        # Update buffer
        sum_buffer += int(val)

        # Locate lowest max
        lowest_max_idx = 0
        for i, val in enumerate(sum_max):
            if val < sum_max[lowest_max_idx]:
                lowest_max_idx = i

        # Update max
        if sum_buffer > sum_max[lowest_max_idx]:
            sum_max[lowest_max_idx] = sum_buffer

    print(sum(sum_max))
