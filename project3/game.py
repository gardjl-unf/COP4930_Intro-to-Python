from random import randint
from json import load, dump
from player import Player
from board import Board

_MARK_INVERT = { "O" :"X", "X" : "O"}
_MOVE_STRINGS = ["1st","2nd","3rd","4th","5th","6th","7th","8th","9th"]

class Game:
    def __init__(self, strings):
        self.strings = strings
        self.player = Player(self.strings)
        self.computer = Player(self.strings)
        self.board = Board(self.strings)
        self.current_player = str()
        self.computer.makeCPU()
        self.file = self.strings["_FILE_PATH"] + self.strings["_FILE_NAME"]
        self.loaded = False
        self.quit = False

    def reset(self):
        self.player = Player(self.strings)
        self.computer = Player(self.strings)
        self.board = Board(self.strings)
        self.current_player = str()
        self.computer.makeCPU()
        self.loaded = False
        self.quit = False

    def loadGame(self, player_name):
        with open(self.file) as file_object:
            print(self.strings["_LOADING_STR"])
            game_data = load(file_object)
            if player_name not in game_data:
                self.player = self.player.newPlayer(player_name)
            else:
                player_data = game_data[player_name]
                self.strings["_RETURNING_STR"].format(player_name)
                self.loadGameState(player_name, player_data)
                self.loaded = True
                print(self.player)

    def loadGameState(self, player_name, player_data):
        self.player.loadPlayer(player_name, player_data)
        self.loadMark(player_data[3])
        self.loadCurrentPlayer(player_data[4])
        self.player.loadMoves(player_data[5])
        if len(self.player.moves) > 0:
            self.board.updateBoard(self.player)
            self.player.printMoves()
        self.computer.loadMoves(player_data[6])
        if len(self.computer.moves) > 0:
            self.board.updateBoard(self.computer)
            self.computer.printMoves()

    def loadCurrentPlayer(self, current_data):
        self.current_player = current_data

    def loadMark(self, mark_data):
        self.player.mark = mark_data
        self.computer.mark = _MARK_INVERT[self.player.mark]
        print(self.strings["_CURRENT_MARK_STR"].format(self.player.name, self.player.mark))

    def saveGame(self):
        with open(self.file) as file_object:
            game_data = load(file_object)
        game_data[self.player.name] = [self.player.wins, self.player.losses, self.player.draws, self.player.mark, \
                                       self.current_player, self.player.moves, self.computer.moves, self.board.board]
        with open(self.file, 'w') as file_object:
            dump(game_data, file_object, indent = 3)
        print(self.strings["_SAVE_STR"])

    def play(self):
        self.player.player_name = input(self.strings["_NAME_PROMPT_STR"])
        self.loadGame(self.player.player_name)
        if not self.loaded:   
            self.player.mark = input(self.strings["_CHOOSE_MARK_STR"])
            self.computer.mark = _MARK_INVERT[self.player.mark]
            self.coinFlip()
        self.playRounds()

    def coinFlip(self):
        input(self.strings["_COIN_TOSS_STR"])
        coin = randint(0, 1)
        if coin == 0:
            print(self.strings["_TOSS_RESULT_STR"].format(self.player.player_name))
            self.current_player = self.player.player_name
        else:
            print(self.strings["_TOSS_RESULT_STR"].format(self.computer.player_name))
            self.current_player = self.computer.player_name

    def playRounds(self):
        while not self.quit:
            print(self.board)
            if self.current_player == self.player.player_name:
                self.playerTurn() 
            else:
                self.computerTurn()
            if self.player.winner or self.computer.winner:
                if self.current_player == self.computer.name:
                    self.player.losses += 1
                self.quit = True
                break
            elif self.board.moves == 9:
                self.player.draws += 1
                print(self.strings["_DRAW_STR"])
                self.quit = True
                break

    def playerTurn(self):
        move = input(self.strings["_ENTER_MOVE_STR"].format(self.player.name, _MOVE_STRINGS[len(self.player.moves)]))
        if move == self.strings["_QUIT_STR"]:
                self.quit = True
                return
        move = move.split(',')
        move = [int(move[0]), int(move[1])]
        while not self.board.makeMove(self.player, move) == None:
            move = input(self.strings["_ENTER_MOVE_STR"].format(self.player.name, _MOVE_STRINGS[len(self.player.moves)]))
            if move == self.strings["_QUIT_STR"]:
                self.quit = True
                return
            move = move.split(',')
            move = [int(move[0]), int(move[1])]
        print(self.board)
        self.current_player = self.computer.name

    def computerTurn(self):
        move = self.board.getMove()
        self.board.makeMove(self.computer, move)
        print(self.board)
        self.current_player = self.player.name