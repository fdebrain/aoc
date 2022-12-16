import os

from aocd import get_data
from dotenv import load_dotenv

load_dotenv()


if __name__ == "__main__":
    session_id = os.getenv("SESSION_ID")
    data = get_data(day=10, year=2022, session=session_id)
    data = data.split("\n")

    # Part 1: Find the signal strength during the 20th, 60th, 100th, 140th, 180th, and 220th cycles.
    # What is the sum of these six signal strengths?
    register = 1
    signal_strengths = {}
    idx = 0
    wait_cycles = 0
    to_increment = None

    for cycle in range(1, 221):
        instruction = data[idx]

        if cycle in [20, 60, 100, 140, 180, 220]:
            signal_strengths[cycle] = register * cycle

        if instruction == "noop":
            # Start new instruction in the next cycle
            idx += 1
        elif to_increment is None:
            # Start addx execution
            wait_cycles = 1
            to_increment = int(instruction.split(" ")[-1])
        elif to_increment and wait_cycles == 0:
            # Finish addx execution (increment register)
            register += to_increment
            to_increment = None
            idx += 1  # Start new instruction in the next cycle

        wait_cycles -= 1

    print(sum(signal_strengths.values()))

    # Part 2: What eight capital letters appear on your CRT?
    register = 1
    idx = 0
    wait_cycles = 0
    to_increment = None
    sprite_position = 0
    screen = []

    for cycle in range(1, 241):
        instruction = data[idx]

        if instruction == "noop":
            idx += 1
        elif to_increment is None:  # Start addx execution
            wait_cycles = 1
            to_increment = int(instruction.split(" ")[-1])
        elif to_increment and wait_cycles == 0:  # Finish addx execution
            register += to_increment
            to_increment = None
            idx += 1

        wait_cycles -= 1

        # Update screen
        if abs(cycle % 40 - register) > 1:
            screen.append(".")
        else:
            screen.append("#")

    # Show screen
    for i, pixel in enumerate(screen):
        if i % 40 == 0:
            print("\n", end="")
        print(pixel, end="")
    print()
