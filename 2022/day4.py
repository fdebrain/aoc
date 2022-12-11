import os

from aocd import get_data
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    session_id = os.getenv("SESSION_ID")
    data = get_data(day=4, year=2022, session=session_id)

    # From "a0-a1,b0-b1" to [[a0,a1], [b0,b1]] for each line of data
    data = [
        [interval.split("-") for interval in d.split(",")] for d in data.split("\n")
    ]
    data = [[[int(r[0]), int(r[1])] for r in d] for d in data]

    # Part 1: Count the number of pairs for which one range contains fully the other
    count = 0
    for pair in data:
        a, b = pair

        # Equivalent to (a0<b0 AND a1>b1) OR (a0>b0 AND a1<b1)
        if (a[0] - b[0]) * (a[1] - b[1]) <= 0:
            count += 1

    print(count)

    # Part 2: Count the number of pairs for which ranges overlap on at least 1 section
    count = 0
    for pair in data:
        a, b = pair

        # Equivalent to NOT (a0>b1 OR a1>b0)
        if a[1] >= b[0] and b[1] >= a[0]:
            count += 1

    print(count)
