import os

from aocd import get_data
from dotenv import load_dotenv

load_dotenv()


def update_worry_level(item: int, operation_type: str, operation_val: str):
    value = item if operation_val == "old" else int(operation_val)

    if operation_type == "+":
        return item + value
    elif operation_type == "*":
        return item * value
    else:
        raise ValueError("Wrong operation type")


def compute_receiver(worry_level, divisible_by, monkey_true, monkey_false):
    is_divisible = (worry_level % divisible_by) == 0
    return [monkey_false, monkey_true][is_divisible]


def initialize_monkey_info(data, part_id: int):
    info = {}
    for line in data:
        if "Monkey" in line:
            monkey_id = int(line.replace(":", "").split(" ")[-1])
            info[monkey_id] = {"inspected_items": 0 if part_id == 1 else []}
        elif "Starting items" in line:
            cleaned_line = line.replace("Starting items:", "").split(", ")
            info[monkey_id]["items"] = [int(item) for item in cleaned_line]
        elif "Operation" in line:
            info[monkey_id]["operation"] = line.split(" ")[-2:]
        elif "Test" in line:
            info[monkey_id]["divisible_by"] = int(line.split(" ")[-1])
        elif "If true" in line:
            info[monkey_id]["true"] = int(line.split(" ")[-1])
        elif "If false" in line:
            info[monkey_id]["false"] = int(line.split(" ")[-1])
        else:
            continue
    return info


if __name__ == "__main__":
    session_id = os.getenv("SESSION_ID")
    data = get_data(day=11, year=2022, session=session_id)
    data = data.split("\n")

    # Part 1: What is the level of monkey business after 20 rounds?
    all_monkey_info = initialize_monkey_info(data, part_id=1)
    for _ in range(20):
        # Monkeys taking turn
        for monkey_id in range(len(all_monkey_info)):
            monkey_info = all_monkey_info[monkey_id]

            while monkey_info["items"]:
                # Pick next item on the list and delete it
                item = monkey_info["items"].pop(0)

                # Update "inspected_items" counter of the monkey
                monkey_info["inspected_items"] += 1

                # Apply operation and divide by 3 (nearest lower integer)
                worry_level = update_worry_level(
                    item,
                    *monkey_info["operation"],
                )
                worry_level = int(worry_level / 3)

                # Determine to which monkey the item will be sent
                receiver_monkey = compute_receiver(
                    worry_level,
                    divisible_by=monkey_info["divisible_by"],
                    monkey_true=monkey_info["true"],
                    monkey_false=monkey_info["false"],
                )

                # Send item to receiver monkey
                all_monkey_info[receiver_monkey]["items"].append(worry_level)

        # for monkey_id in range(len(all_monkey_info)):
        #     print(monkey_id, all_monkey_info[monkey_id]["items"])

    # Sum inspected items for the most 2 active monkeys
    all_inspected_items = sorted(
        [monkey_info["inspected_items"] for monkey_info in all_monkey_info.values()]
    )
    print(all_inspected_items[-1] * all_inspected_items[-2])

    # Part 2:
    all_monkey_info = initialize_monkey_info(data, part_id=1)
    for round_id in range(10_000):
        # Monkeys taking turn
        for monkey_id in range(len(all_monkey_info)):
            monkey_info = all_monkey_info[monkey_id]

            while monkey_info["items"]:
                # Pick next item on the list and delete it
                item = monkey_info["items"].pop(0)

                # Update "inspected_items" counter of the monkey
                monkey_info["inspected_items"] += 1

                # Apply operation
                worry_level = update_worry_level(
                    item,
                    *monkey_info["operation"],
                )

                # Trick: worry level modulo product of all divisible_by
                divisibility_list = [
                    info["divisible_by"] for info in all_monkey_info.values()
                ]
                divisibility_product = 1
                for d in divisibility_list:
                    divisibility_product *= d
                worry_level = worry_level % divisibility_product

                # Determine to which monkey the item will be sent
                receiver_monkey = compute_receiver(
                    worry_level,
                    divisible_by=monkey_info["divisible_by"],
                    monkey_true=monkey_info["true"],
                    monkey_false=monkey_info["false"],
                )

                # Send item to receiver monkey
                all_monkey_info[receiver_monkey]["items"].append(worry_level)

        #     for monkey_id in range(len(all_monkey_info)):
        #         print(monkey_id, all_monkey_info[monkey_id]["items"])

    # Sum inspected items for the most 2 active monkeys
    all_inspected_items = sorted(
        [monkey_info["inspected_items"] for monkey_info in all_monkey_info.values()]
    )
    print(all_inspected_items[-1] * all_inspected_items[-2])
