import os

from aocd import get_data
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    session_id = os.getenv("SESSION_ID")
    data = get_data(day=3, year=2022, session=session_id)
    data = data.split("\n")

    # Instanciate mappings between item letter and associated priority
    letter2prority = {
        **{chr(i): p + 1 for p, i in enumerate(range(ord("a"), ord("z") + 1))},
        **{chr(i): p + 27 for p, i in enumerate(range(ord("A"), ord("Z") + 1))},
    }

    # Part 1: Find the common items between the 2 compartments for each rucksack.
    # What is the sum of the priorities of those items?
    priority_sum = 0
    for rucksack in data:
        n = len(rucksack)
        first_compartiment_items = set(rucksack[: n // 2])
        second_compartiment_items = set(rucksack[n // 2 :])

        # Filter items present in both compartments
        duplicated_items = first_compartiment_items.intersection(
            second_compartiment_items
        )

        # Sum of priorities
        for item in duplicated_items:
            priority_sum += letter2prority.get(item, 0)

    print(priority_sum)

    # Part 2: Find the unique item that corresponds to the badges of each three-Elf group.
    # What is the sum of the priorities of those item?
    priority_sum = 0
    for group_id in range(len(data) // 3):
        first_rucksack = set(data[group_id * 3])
        second_rucksack = set(data[group_id * 3 + 1])
        third_rucksack = set(data[group_id * 3 + 2])

        duplicated_item = first_rucksack.intersection(second_rucksack).intersection(
            third_rucksack
        )
        assert (
            len(duplicated_item) == 1
        ), "There is more than 1 common item within the group"

        priority_sum += letter2prority[list(duplicated_item)[0]]
    print(priority_sum)
