import os

from aocd import get_data
from dotenv import load_dotenv

load_dotenv()


def initialize_structure(starting):
    """Return a dictionary of lists containing the crates in each stack."""
    structure = {int(d.strip()): [] for d in starting[-1].split(" ") if d.strip()}
    for line in starting[:-1]:
        line = extract_stack_row(line, len(structure))
        # Populate stacks with items (top of stack = end of list)
        for i in range(len(structure)):
            if item := line[i]:
                structure[i + 1].insert(0, item)
    return structure


def decode_instruction(x):
    """Return a tuple of integers (n, start, end) for a given input string.

    Input should be in the form of `Move {n} from {start} to {end}`.
    """
    x = x.split(" ")
    return (int(x[1]), int(x[3]), int(x[-1]))


def extract_stack_row(row, n_stacks):
    """Return a list of length `n_stacks` containing up to 1 item per stack.

    Input should be in the form of a string such as `    [V] [G]             [H]        `.
    Each stack position is a substring of length 3 and separated from other positions by a single space.
    """
    return [
        row[4 * i : 4 * (i + 1)].replace("[", "").replace("]", "").strip()
        for i in range(n_stacks)
    ]


if __name__ == "__main__":
    session_id = os.getenv("SESSION_ID")
    data = get_data(day=5, year=2022, session=session_id)
    data = data.split("\n")

    # Split starting structure from instructions
    is_starting = True
    starting = []
    instructions = []
    for d in data:
        if d == "":
            is_starting = False
            continue

        if is_starting:
            starting.append(d)
        else:
            instructions.append(d)

    # Show initial structure
    for line in starting:
        print(line)

    # Part 1: What crate ends up on the top of each stack?
    structure = initialize_structure(starting)
    for instruction in instructions:
        n, start, end = decode_instruction(instruction)

        # Rearrange stacks
        block_to_move = structure[start][-n:]
        structure[end].extend(block_to_move[::-1])  # Inverse order of crates (1-by-1)
        del structure[start][-n:]

        # print(instruction)
        # print(structure)

    top = "".join([structure[stack + 1][-1] for stack in range(len(structure))])
    print(top)

    # Part 2: What crate ends up on the top of each stack with the new procedure?
    structure = initialize_structure(starting)
    for instruction in instructions:
        n, start, end = decode_instruction(instruction)

        # Rearrange stacks
        block_to_move = structure[start][-n:]
        structure[end].extend(block_to_move)  # Keep same order of crates
        del structure[start][-n:]

    top = "".join([structure[stack + 1][-1] for stack in range(len(structure))])
    print(top)
