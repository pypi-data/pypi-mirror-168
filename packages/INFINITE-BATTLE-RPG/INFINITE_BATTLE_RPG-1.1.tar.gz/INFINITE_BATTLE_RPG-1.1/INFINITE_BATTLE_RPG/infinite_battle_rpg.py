"""
This file contains code for the game "Infinite Battle RPG".
Author: PythonApkDev
"""


# Importing necessary libraries


import sys
import os
import uuid
import copy
import random

import mpmath
from mpmath import mp, mpf

mp.pretty = True


# Creating static function to be used in the game.


def clear():
    # type: () -> None
    if sys.platform.startswith('win'):
        os.system('cls')  # For Windows System
    else:
        os.system('clear')  # For Linux System


# Creating necessary classes to be used in the game.


class Player:
    """
    This class contains attributes of the player in this game.
    """

    def __init__(self, name):
        # type: (str) -> None
        self.player_id: str = str(uuid.uuid1())  # Generate random player ID
        self.name: str = name
        self.level: int = 1
        self.max_hp: mpf = mpf(random.randint(120, 150))
        self.curr_hp: mpf = self.max_hp
        self.attack_power: mpf = mpf(random.randint(30, 50))
        self.defense: mpf = mpf(random.randint(20, 30))

    def __str__(self):
        # type: () -> str
        res: str = ""  # initial value
        res += "Player ID: " + str(self.player_id) + "\n"
        res += "Level: " + str(self.level) + "\n"
        res += "Name: " + str(self.name) + "\n"
        res += "HP: " + str(self.curr_hp) + "/" + str(self.max_hp) + "\n"
        res += "Attack Power: " + str(self.attack_power) + "\n"
        res += "Defense: " + str(self.defense) + "\n"
        return res

    def is_alive(self):
        # type: () -> bool
        return self.curr_hp > 0

    def restore(self):
        # type: () -> None
        self.curr_hp = self.max_hp

    def level_up(self):
        # type: () -> None
        self.level += 1
        self.max_hp *= 2
        self.restore()
        self.attack_power *= 2
        self.defense *= 2

    def attack(self, other):
        # type: (Player) -> None
        raw_damage: mpf = self.attack_power - other.defense
        damage: mpf = mpf("0") if raw_damage < 0 else raw_damage
        other.curr_hp -= damage
        print(str(self.name) + " dealt " + str(damage) + " damage on " + str(other.name) + "!")

    def clone(self):
        # type: () -> Player
        return copy.deepcopy(self)


class CPU(Player):
    """
    This class contains attributes of the CPU in this game.
    """

    def __init__(self):
        # type: () -> None
        Player.__init__(self, "CPU")


# Creating main function used to run the game.


def main() -> int:
    """
    This main function is used to run the game.
    :return: an integer
    """

    print("Welcome to 'Infinite Battle RPG' by 'PythonApkDev'.")
    print("In this game, your mission is to survive as many rounds as possible.")

    name: str = input("Please enter your name: ")
    player: Player = Player(name)
    cpu: CPU = CPU()

    clear()
    print("Enter 'Y' for yes.")
    print("Enter anything else for no.")
    round_number: int = 1
    turn: int = 0
    continue_playing: str = input("Do you want to continue playing 'Infinite Battle RPG? ")
    while continue_playing == "Y":
        while player.is_alive() and cpu.is_alive():
            clear()
            print("#################### ROUND " + str(round_number) + " ####################")
            print("Player stats:\n" + str(player) + "\n")
            print("CPU stats:\n" + str(cpu) + "\n")
            turn += 1
            if turn % 2 == 1:
                print("It is your turn to attack.")
                attack: str = input("Enter anything to attack: ")
                player.attack(cpu)
            else:
                print("It is CPU's turn to attack")
                cpu.attack(player)

        if not player.is_alive():
            clear()
            print("GAME OVER!!!! " + str(player.name).upper() + " DIED!!!!")
            round_number = 1
            turn = 0
            player = Player(name)
            cpu = CPU()
        elif not cpu.is_alive():
            clear()
            print("YOU WON THE BATTLE IN ROUND " + str(round_number) + "!!!!")
            round_number += 1
            turn = 0
            player_level_ups: int = random.randint(1, 100)
            cpu_level_ups: int = random.randint(1, 100)
            for i in range(player_level_ups):
                player.level_up()

            for i in range(cpu_level_ups):
                cpu.level_up()

        print("Enter 'Y' for yes.")
        print("Enter anything else for no.")
        continue_playing = input("Do you want to continue playing 'Infinite Battle RPG? ")

    return 0


if __name__ == '__main__':
    main()
