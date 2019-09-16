import time

import numpy as np
from IPython.display import clear_output


class Connect4(object):
    def __init__(self):
        self.start_game()

    def start_game(self):
        p1_name = input("Player 1 Name: ")
        p2_name = input("Player 2 Name, or (Computer): ")
        self.players = [p1_name, p2_name]
        self.ai_player = p2_name.lower() == "computer"
        self.rounds = int(input("How many rounds? "))
        self.curr_round = 0
        self.round_score = [0, 0]

        while ((self.curr_round < self.rounds)
               and
               (abs(self.round_score[0] - self.round_score[1])) <= (self.rounds - self.curr_round)):
            clear_output()
            print("Round Score:")
            print(f"{self.players[0]}: {self.round_score[0]}")
            print(f"{self.players[1]}: {self.round_score[1]}")
            print()
            input("Press Enter to start new round:")
            self.start_round()

        clear_output()
        print("Final Round Score:")
        print(f"{self.players[0]}: {self.round_score[0]}")
        print(f"{self.players[1]}: {self.round_score[1]}")
        print()

        if self.round_score[0] > self.round_score[1]:
            print(f"{self.players[0]} wins!")
        elif self.round_score[0] > self.round_score[1]:
            print(f"{self.players[1]} wins!")
        else:
            print("It's a tie!")

        new = input("New game? (y/n) ")
        if new.lower() == 'y':
            self.start_game()
        else:
            print("Thanks for playing!")

    def start_round(self):
        clear_output()
        self.curr_round += 1
        self.bitboards = [0, 0]
        self.display_mask = [
            [7*j + i for j in range(7)] for i in range(6, -1, -1)]
        self.heights = [7*j for j in range(7)]
        self.max_heights = [7*j + 6 for j in range(7)]
        self.move_counter = 0
        self.finished = False

        self.display_board()
        while not self.finished:
            self.curr_player = (self.curr_round + self.move_counter + 1) % 2
            self.valid_actions = [i for i, height in enumerate(self.heights)
                                  if height not in self.max_heights]
            time.sleep(0.1)
            self.make_move(self.ask_move())
            win = self.check_win(self.bitboards[self.curr_player])
            self.finished = win or (self.heights == self.max_heights)
            self.move_counter += 1
            self.display_board()
            if not self.finished:
                time.sleep(0.5)
        if not win:
            print()
            print(f"Round {self.curr_round} is a tie!")
            print()
        else:
            print()
            self.round_score[self.curr_player] += 1
            print(
                f"{self.players[self.curr_player]} wins round {self.curr_round}!")
            print()
        input("Enter to continue:")

    def make_move(self, col):
        move = pow(2, self.heights[col])
        self.bitboards[self.curr_player] += move
        self.heights[col] += 1

    def display_board(self):
        clear_output()
        print(f"X: {self.players[0]}, O: {self.players[1]}")
        print()
        board_arr = ""
        for i in self.display_mask[1:]:
            board_arr += '| '
            for j in i:
                if (pow(2, j) & self.bitboards[0]):
                    board_arr += "X "
                elif (pow(2, j) & self.bitboards[1]):
                    board_arr += "O "
                else:
                    board_arr += ". "
            board_arr += '|\n'
        board_arr += "| - - - - - - - |\n"
        board_arr += "| 0 1 2 3 4 5 6 |"
        print(board_arr)

    def ask_move(self):
        player = self.players[self.curr_player]
        col = input(
            f"{player}'s move, choose column from {self.valid_actions}: ")

        while (not col.isdigit()) or (int(col) not in self.valid_actions):
            col = input(f"Invalid, choose column from {self.valid_actions}: ")
        return int(col)

    def check_win(self, curr_board):
        directions = [1, 7, 6, 8]
        for direction in directions:
            bb = curr_board & (curr_board >> direction)
            if bb & (bb >> direction * 2):
                return True
        return False
