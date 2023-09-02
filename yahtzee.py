"""
This module contains functions for playing the game of Yahtzee. The game can be played interactively with multiple players.
The module includes functions for rolling dice, validating and processing user input, determining the kind of roll based on the given dice list,
and displaying the statistics of the Yahtzee game results. The main_interactive_multiplayer function allows multiple players to play Yahtzee interactively.
"""
from typing import List, Tuple
from random import randint
import logging

logging.basicConfig(filename='yahtzee_game.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def roll_dice() -> List[int]:
    """
    Simulates rolling 5 dice and returns the result as a list of integers.

    Returns:
    List[int]: A list of 5 integers representing the result of rolling 5 dice.
    """
    return [randint(1, 6) for _ in range(5)]

def validate_and_process_input(input_str: str) -> Tuple[bool, List[int]]:
    """
    Validates and processes the user input for the Yahtzee game.

    Args:
        input_str (str): The user input string.

    Returns:
        Tuple[bool, List[int]]: A tuple containing a boolean value indicating whether the input is valid,
        and a list of processed indices if the input is valid, otherwise an empty list.
    """
    input_str = input_str.replace(",", "").replace(" ", "")
    is_valid = all(char.isdigit() and 1 <= int(char) <= 5 for char in input_str)
    processed_indices = [int(char) - 1 for char in input_str] if is_valid else []
    return is_valid, processed_indices

def game_statistics(game_results: List[Tuple[bool, ...]]) -> None:
    """
    Prints the statistics of the Yahtzee game results.

    Parameters:
    game_results (List[Tuple[bool, ...]]): A list of tuples representing the results of each game played. Each tuple contains boolean values indicating whether a certain roll type was achieved or not.

    Returns:
    None
    """
    counters = {"yahtzee": 0, "full_house": 0, "low_straight": 0, "high_straight": 0, "four_of_a_kind": 0, "three_of_a_kind": 0}
    for result in game_results:
        for i, roll_type in enumerate(counters.keys()):
            counters[roll_type] += result[i]
    total_games = len(game_results)
    print(f"In {total_games} games, you rolled:")
    for roll_type, count in counters.items():
        percentage = (count / total_games) * 100
        print(f"{roll_type.replace('_', ' ').title()}: {count} ({percentage:.2f}%)")

def determine_roll_kind(dice_list: List[int]) -> Tuple[bool, ...]:
    """
    Determines the kind of roll based on the given dice list.

    Args:
        dice_list (List[int]): A list of integers representing the values of the dice.

    Returns:
        Tuple[bool, ...]: A tuple of boolean values representing the kind of roll.
        The tuple contains the following values in order:
        - yahtzee (bool): True if the roll is a yahtzee (all dice have the same value), False otherwise.
        - full_house (bool): True if the roll is a full house (three dice have the same value and the other two have the same value), False otherwise.
        - low_straight (bool): True if the roll is a low straight (the dice values form a sequence of four consecutive numbers), False otherwise.
        - high_straight (bool): True if the roll is a high straight (the dice values form a sequence of five consecutive numbers), False otherwise.
        - four_of_a_kind (bool): True if the roll is a four of a kind (four dice have the same value), False otherwise.
        - three_of_a_kind (bool): True if the roll is a three of a kind (three dice have the same value), False otherwise.
    """
    counts = [dice_list.count(i) for i in dice_list]
    unique_sorted_dice = sorted(set(dice_list))
    yahtzee = 5 in counts
    full_house = 3 in counts and 2 in counts
    low_straight = len(unique_sorted_dice) >= 4 and max(unique_sorted_dice[:4]) - min(unique_sorted_dice[:4]) == 3
    high_straight = len(unique_sorted_dice) == 5 and max(unique_sorted_dice) - min(unique_sorted_dice) == 4
    four_of_a_kind = 4 in counts
    three_of_a_kind = 3 in counts
    return yahtzee, full_house, low_straight, high_straight, four_of_a_kind, three_of_a_kind

def main_interactive_multiplayer():
    """
    This function allows multiple players to play Yahtzee interactively. It prompts the user to enter the number of players,
    and then loops through each player's turn until the game is over. During each turn, the player rolls five dice and has the
    option to replace any number of them. The function then determines the type of roll (e.g. three of a kind, full house, etc.)
    and records the result for that player. At the end of the game, the function displays the statistics for each player.
    """
    print("Welcome to Yahtzee!")
    print("=" * 80)
    num_players = int(input("Enter the number of players: "))
    player_results = {f"Player {i+1}": [] for i in range(num_players)}
    
    while True:
        for player, results in player_results.items():
            print(f"\n{'-' * 80}\n")
            print(f"{player}'s Turn\n")
            first_roll = roll_dice()
            print(f"You rolled: {first_roll}\n")
            first_instruction = input("Do you want to replace any dice? (y/n): ").strip().lower()
            while first_instruction not in ('y', 'n'):
                print("Incorrect input. Please enter 'y' for yes or 'n' for no.")
                first_instruction = input("Do you want to replace any dice? (y/n): ").strip().lower()
            
            if first_instruction == 'y':
                is_valid, indices_to_replace = validate_and_process_input(input("Type the values of each die you want to replace (1-5), separate with a comma: "))
                while not is_valid:
                    print("Incorrect input. Please enter values between 1 and 5, separated by commas.")
                    is_valid, indices_to_replace = validate_and_process_input(input("Type the values of each die you want to replace (1-5), separate with a comma: "))
                
                for i in indices_to_replace:
                    first_roll[i] = randint(1, 6)
                print(f"New roll: {first_roll}\n")
            
            game_result = determine_roll_kind(first_roll)
            results.append(game_result)
        
        new_game = input("Do you want to play another game? (y/n): ").strip().lower()
        if new_game != 'y':
            break

    for player, results in player_results.items():
        print(f"\nStatistics for {player}:")
        game_statistics(results)

if __name__ == "__main__":
    main_interactive_multiplayer()
