import os

from aocd import get_data
from dotenv import load_dotenv

load_dotenv()


if __name__ == "__main__":
    session_id = os.getenv("SESSION_ID")
    data = get_data(day=6, year=2022, session=session_id)

    # Part 1: Position of the first start-of-message marker (after 4 unique characters)
    for i in range(4, len(data)):
        substring = data[i - 4 : i]

        # Detect marker - Count letter occurences
        count_dict = {}
        for letter in substring:
            count_dict[letter] = count_dict.get(letter, 0) + 1

        if set(list(count_dict.values())) == {1}:
            print(i)
            break

    # Part 2: Position of the first start-of-message marker (after 14 unique characters)
    for i in range(14, len(data)):
        substring = data[i - 14 : i]

        # Detect marker - Count letter occurences
        count_dict = {}
        for letter in substring:
            count_dict[letter] = count_dict.get(letter, 0) + 1

        if set(list(count_dict.values())) == {1}:
            print(i)
            break
