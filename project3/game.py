from random import randint
from json import load, dump
from os.path import getsize, isfile
from player import Player
from board import Board

_MARK_INVERT = { "O" :"X", "X" : "O"}
_MOVE_STRINGS = [ "1st", "2nd", "3rd", "4th", "5th" ]
_MARKS = [ "X", "O" ]
_HEADS_OR_TAILS = [ "H", "T" ]

class Game:
    def __init__(self, strings):
        self.strings = strings
        self.player = Player(self.strings)
        self.computer = Player(self.strings)
        self.board = Board(self.strings)
        self.current_player = str()
        self.file = self.strings["_FILE_PATH"] + self.strings["_FILE_NAME"]
        self.msg = str()
        self.loaded = False
        self.quit = False
        self.computer.make_CPU()

    def reset(self):
        self.player.reset()
        self.computer.reset()
        self.board.reset()

    def load_game(self, player_name):
        print(self.strings["_LOADING_STR"])
        if isfile(self.file) and getsize(self.file) > 0:
            with open(self.file) as file_object:
                game_data = load(file_object)
                if player_name not in game_data:
                    self.player.new_player(player_name)
                else:
                    player_data = game_data[player_name]
                    self.player.load_player(player_name, player_data)
                    self.current_player = self.player.name
                    print(self.player)
                    self.strings["_RETURNING_STR"].format(player_name)
                    self.load_game_state(player_data)
                    self.loaded = True       
        else:
            f = open(self.file, "a")
            f.close()
            self.player.new_player(player_name)

    def load_game_state(self, player_data):
        self.load_mark(player_data[3])
        self.player.load_moves(player_data[4])
        if len(self.player.moves) > 0:
            self.board.updateBoard(self.player)
            self.player.print_moves()
        self.computer.load_moves(player_data[5])
        if len(self.computer.moves) > 0:
            self.board.updateBoard(self.computer)
            self.computer.print_moves()
        if len(self.player.moves) + len(self.computer.moves) == 0:
            self.get_mark()
            self.coin_flip()
        else:
            print(self.strings["_RESUME_STR"])

    def binary_entry(self, prompt, valid_entries):
        entry = input(prompt)
        while entry not in valid_entries:
            print(self.strings["_INVALID_ENTRY_STR"].format(valid_entries[0], valid_entries[1]))
            entry = input(prompt)
        return entry

    def get_mark(self):
        self.set_mark(self.binary_entry(self.strings["_CHOOSE_MARK_STR"], _MARKS))
        print()

    def get_name(self):
        self.player.player_name = input(self.strings["_NAME_PROMPT_STR"])

    def load_mark(self, mark_data):
        if mark_data != '' and mark_data != None:
            self.set_mark(mark_data)
            print(self.strings["_CURRENT_MARK_STR"].format(self.player.name, self.player.mark))

    def set_mark(self, mark):
        self.player.mark = mark
        self.computer.mark = _MARK_INVERT[self.player.mark]

    def save_game(self):
        if getsize(self.file) > 0:
            with open(self.file) as file_object:
                game_data = load(file_object)
        else:
            game_data = dict()
        if self.board.moves == 9 or self.player.winner or self.computer.winner:
            print(self.player)
            self.reset()
        else:
            print(self.strings["_SAVE_STR"])
        game_data[self.player.name] = [self.player.wins, self.player.losses, self.player.draws, self.player.mark, \
                                       self.player.moves, self.computer.moves]
        with open(self.file, 'w') as file_object:
            dump(game_data, file_object, indent = 3)

    def play(self):
        self.get_name()
        self.load_game(self.player.player_name)
        if not self.loaded:   
            self.get_mark()
            self.coin_flip()
        self.play_rounds()

    def coin_flip(self):
        self.binary_entry(self.strings["_COIN_TOSS_STR"], _HEADS_OR_TAILS)
        coin = randint(0, 1)
        if coin == 0:
            print(self.strings["_TOSS_RESULT_STR"].format(self.player.player_name))
            self.current_player = self.player.player_name
        else:
            print(self.strings["_TOSS_RESULT_STR"].format(self.strings("_COMPUTER_NAME_STR_STR")))
            self.current_player = self.computer.player_name

    def play_rounds(self):
        while not self.quit:
            if self.player.winner or self.computer.winner:
                if self.current_player == self.player.name:
                    self.player.losses += 1
                self.quit = True
                break
            elif self.board.moves == 9:
                self.player.draws += 1
                print(self.board)
                print(self.strings["_DRAW_STR"])
                self.quit = True
                break
            if self.current_player == self.player.player_name:
                self.player_turn() 
            else:
                self.computer_turn()
            
    def player_turn(self):
        len(self.player.moves)
        print(self.board)
        move = input(self.strings["_ENTER_MOVE_STR"].format(self.player.name, _MOVE_STRINGS[len(self.player.moves)]))
        if move == self.strings["_QUIT_STR"]:
                self.quit = True
                return
        move = move.split(',')
        move = [int(move[0]), int(move[1])]
        while not self.board.make_move(self.player, move) == None:
            move = input(self.strings["_ENTER_MOVE_STR"].format(self.player.name, _MOVE_STRINGS[len(self.player.moves)]))
            if move == self.strings["_QUIT_STR"]:
                self.quit = True
                return
            move = move.split(',')
            move = [int(move[0]), int(move[1])]
        self.current_player = self.computer.name

    def computer_turn(self):
        move = self.board.getMove()
        self.board.make_move(self.computer, move)
        self.current_player = self.player.name