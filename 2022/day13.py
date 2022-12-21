import ast
import os

from aocd import get_data
from dotenv import load_dotenv

load_dotenv()


def check_order(left, right, verbose=False):
    i = 0

    while i < len(left) and i < len(right):
        left_element = left[i]
        right_element = right[i]

        if isinstance(left_element, int) and isinstance(right_element, int):
            if left_element > right_element:
                order = -1
            elif left_element < right_element:
                order = 1
            else:
                order = 0
        elif isinstance(left_element, list) and isinstance(right_element, list):
            order = check_order(left_element, right_element, verbose=False)
        elif isinstance(left_element, int) and isinstance(right_element, list):
            order = check_order([left_element], right_element, verbose=False)
        elif isinstance(left_element, list) and isinstance(right_element, int):
            order = check_order(left_element, [right_element], verbose=False)
        else:
            print("Wrong type")

        # Debug purpose
        if verbose:
            print(left_element, right_element, end=" | ")
            if order == -1:
                print("Bad order detected")
            elif order == 1:
                print("Good order detected")
            else:
                print("Equal items detected. Continue comparison")

        # Stop comparison if elements are not equal
        if order == -1:
            return -1
        elif order == 1:
            return 1
        else:
            i += 1

    # End of array
    if len(left) > len(right):
        if verbose:
            print("Right side ran out of items")
        order = -1
    elif len(left) < len(right):
        if verbose:
            print("Left side ran out of items")
        order = 1
    else:
        order = 0

    return order


if __name__ == "__main__":
    session_id = os.getenv("SESSION_ID")
    data = get_data(day=13, year=2022, session=session_id)

    # Test case:
    # with open("tests/test_input_day13.txt", "r") as f:
    #     data = f.read()

    data = [tuple(pair.split("\n")) for pair in data.split("\n\n")]

    # Part 1: Determine which pairs of packets are already in the right order.
    # What is the sum of the indices of those pairs?
    ordered_pair_ids = []
    for i, pair in enumerate(data):
        left, right = [ast.literal_eval(p) for p in pair]  # Parse strings into lists

        print(i + 1, left, "| ", right)

        if check_order(left, right, verbose=False) >= 0:
            ordered_pair_ids.append(i + 1)  # Pairs index starts from 1
        print()

    print(sum(ordered_pair_ids))

    # Part 2: Organize all of the packets into the correct order.
    # What is the decoder key for the distress signal?
    def list_data_packets(data):
        prepared_data = []

        for pair in data:
            left, right = [ast.literal_eval(p) for p in pair]
            prepared_data.extend([left, right])
        return prepared_data

    divider_packets = [[[2]], [[6]]]
    packets = list_data_packets(data)
    packets.extend(divider_packets)

    # Bubble sort
    n = len(packets)
    for i in range(n):
        for j in range(n - i - 1):
            if check_order(packets[j], packets[j + 1], verbose=False) == -1:
                packets[j], packets[j + 1] = packets[j + 1], packets[j]

    # Display ordered packets
    # for p in packets:
    #     print(p)

    # Find divider packets and compute decoder key
    decoder_key = 1
    for i, p in enumerate(packets):
        if p in divider_packets:
            print("Found divider packet: ", i + 1)
            decoder_key *= i + 1

    print(decoder_key)
