import os

from aocd import get_data
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    session_id = os.getenv("SESSION_ID")
    data = get_data(day=2, year=2022, session=session_id)
    data = [d.split(" ") for d in data.split("\n")]

    shape2score = {"rock": 1, "papper": 2, "scissors": 3}
    opponent_encoding = {"A": "rock", "B": "papper", "C": "scissors"}

    # Part 1: What is the Rock Paper Scissors score following the strategy guide?
    my_encoding = {"X": "rock", "Y": "papper", "Z": "scissors"}
    total_score = 0

    for game in data:
        opponent_shape = opponent_encoding[game[0]]
        my_shape = my_encoding[game[1]]

        # Case 1: Lose
        lose_condition = (
            (my_shape == "rock" and opponent_shape == "papper")
            or (my_shape == "papper" and opponent_shape == "scissors")
            or (my_shape == "scissors" and opponent_shape == "rock")
        )
        if lose_condition:
            total_score += 0 + shape2score[my_shape]

        # Case 2: Draw
        elif opponent_shape == my_shape:
            total_score += 3 + shape2score[my_shape]

        # Case 3: Win
        else:
            total_score += 6 + shape2score[my_shape]

    print(total_score)

    # Part 2: What is the Rock Paper Scissors score following the new strategy?
    my_encoding = {"X": "lose", "Y": "draw", "Z": "win"}
    goal2score = {"lose": 0, "draw": 3, "win": 6}
    total_score = 0

    for game in data:
        opponent_shape = opponent_encoding[game[0]]
        my_goal = my_encoding[game[1]]

        rock_condition = (
            (opponent_shape == "rock" and my_goal == "draw")
            or (opponent_shape == "papper" and my_goal == "lose")
            or (opponent_shape == "scissors" and my_goal == "win")
        )
        papper_condition = (
            (opponent_shape == "papper" and my_goal == "draw")
            or (opponent_shape == "scissors" and my_goal == "lose")
            or (opponent_shape == "rock" and my_goal == "win")
        )

        if rock_condition:
            total_score += goal2score[my_goal] + shape2score["rock"]
        elif papper_condition:
            total_score += goal2score[my_goal] + shape2score["papper"]
        else:
            total_score += goal2score[my_goal] + shape2score["scissors"]

    print(total_score)
