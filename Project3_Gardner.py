import json, random

# Game Strings
# This is not the modern way to do this, but I'm going to pretend that this game
#  needs to be localized and it makes sense to have all the strings in one place.

_WELCOME_STR = 'Welcome to Tic Tac Toe!'
_NAME_PROMPT_STR = 'Enter player name: '
_LOADING_STR = 'Loading...'
_COMPUTER_NAME = 'Computer'
_FIRST_TIME_STR = 'Seems you are a first time player.'
_RETURNING_STR = 'Welcome back, {}!\n'
_RECORD_STR = 'Your record so far is: W{}-L{}-D{}'
_CHOOSE_MARK_STR = 'Enter the mark (‘X’ or ‘O’) you want to play: '
_BOARD_ODD_STR = '|-----------|'
_BOARD_EVEN_STR = '| | | |'
_VERTICAL_STR = '|'
_MARK_STR = '{}|'
_COIN_TOSS_STR = "To start game, enter ‘H’ for Heads or ‘T’ for Tails for a coin toss: "
_TOSS_RESULT_STR = 'Coin toss goes to {}.'
_BEGIN_STR = 'Let the game begin!'
_MOVE_STR = '{} made their {} move at {},{}'
_SANITY_FAIL_STR = 'Bad coordinates! They must be less than 3 and separated by a comma!'
_DUPLICATE_FAIL_STR = 'Bad move! Cell ({0},{1}) was already used!'
_ENTER_MOVE_STR = 'Enter {}’s {} move (Enter ‘q’ to quit game):'
_WIN_STR = '{} strike for {}!'
_DIAG_STR = 'Diagonal'
_COL_STR = 'Column'
_ROW_STR = 'Row'
_MOVE_STRINGS = '1st','2nd','3rd','4th','5th','6th','7th','8th','9th'
_GOODBYE_STR = 'Have a good day!'
_RESULT_STR = '{} {} the game!'
_DRAW_STR = 'Game ended in a draw!'
_SAVE_STR = 'Game saved. Come back and resume game any time!'
_RESUME_STR = 'Let’s resume the unfinished game!'
_CURRENT_MARK_STR = '{} plays ‘{}’.'
_YOUR_MOVES_STR = 'Your moves: '
_COMPUTER_MOVES_STR = 'Computer\'s moves: '
_MOVES_LIST_STR = '{}, '
_MARK_NUM_LET = {0,'O', 1,'X'}
_MARK_LET_NUM = {'O':0, 'X':1}
_MARK_INVERT = {'O':'X', 'X':'O'}

#_FILE_PATH='/content/drive/MyDrive/Colab Notebooks/CIS4930/Projects/Project3/'
_FILE_PATH = ''
_FILE_NAME = 'game_log.json'

class Game:
    def __init__(self):
        self.player = Player()
        self.computer = Player()
        self.board = Board()
        self.current_player = str()
        self.computer_name = _COMPUTER_NAME
        self.file = _FILE_PATH + _FILE_NAME
        self.quit = False

    def loadGame(self, player_name):
        with open(self.file) as file_object:
            print(_LOADING_STR)
            game_data = json.load(file_object)
            if player_name not in game_data:
                self.newPlayer(player_name)
            else:
                player_data = {}
                player_data[player_name] = game_data[player_name]
                _RETURNING_STR.format(self.player.player_name)
                self.loadPlayer(player_name, player_data)
                print(self.player)

    def saveGame(self):
        with open(self.file, 'r+') as file_object:
            player_data = {}
            player_data[self.player.name] = self.player.name
            player_data[self.player.name]["Record"] = {}
            player_data[self.player.name]["Record"]["Win"] = self.player.wins
            player_data[self.player.name]["Record"]["Loss"] = self.player.losses
            player_data[self.player.name]["Record"]["Draw"] = self.player.draws
            player_data[self.player.name]["Unfinished"] = {}
            if not game.board.isFull():
                player_data[self.player.name]["Unfinished"]["Mark"] = self.player.mark
                player_data[self.player.name]["Unfinished"]["Board"] = self.board.board
                player_data[self.player.name]["Unfinished"]["CPUMoves"] = self.computer.moves
                player_data[self.player.name]["Unfinished"]["Moves"] = self.player.moves
            else:
                player_data[self.player.name]["Unfinished"]["Mark"] = None
                player_data[self.player.name]["Unfinished"]["Board"] = None
                player_data[self.player.name]["Unfinished"]["CPUMoves"] = None
                player_data[self.player.name]["Unfinished"]["Moves"] = None
            json.dump(player_data, file_object, indent = 3)
            print(_SAVE_STR)

    def loadBoard(self, player_data):
        self.board = player_data[self.player.name]["Unfinished"]["Board"]

    def loadPlayer(self, player_name, player_data):
        self.player.name = player_name
        self.wins = player_data[player_name]["Record"]["Win"]
        self.losses = player_data[player_name]["Record"]["Loss"]
        self.draws = player_data[player_name]["Record"]["Draw"]
        if self.wins + self.losses + self.draws != 0:
            print(_RETURNING_STR.format(self.player.name))
            print(_RECORD_STR.format(self.wins, self.losses, self.draws))
            self.player.firstGame = False
        self.mark = player_data[player_name]["Unfinished"]["Mark"]
        self.moves = player_data[player_name]["Unfinished"]["Moves"]
        self.cpu_moves = player_data[player_name]["Unfinished"]["CPUMoves"]
        if self.moves is not None:
            print(_CURRENT_MARK_STR.format(self.player.name, _MARK_NUM_LET[self.player.mark]))
            print(_YOUR_MOVES_STR, end='')
            for move in self.moves:
                if move != self.moves[-1]:
                    print(_MOVES_LIST_STR.format(move), end='')
                else:
                    print(move, end='')
        if self.cpu_moves is not None:
            print(_COMPUTER_MOVES_STR, end='')
            for move in self.cpu_moves:
                if move != self.cpu_moves[-1]:
                    print(_MOVES_LIST_STR.format(move), end='')
                else:
                    print(move, end='')
        if self.mark is not None:
            print(_RESUME_STR)
            self.loadBoard(player_data)
            self.board.printBoard()
            self.playGame()
        else:
            self.board = Board()

    def newPlayer(self, player_name):
        print(_FIRST_TIME_STR)
        self.player.firstGame = True
        player_data = {}
        player_data[player_name] = {}
        player_data[player_name]["Record"] = {}
        player_data[player_name]["Record"]["Win"] = 0
        player_data[player_name]["Record"]["Loss"] = 0
        player_data[player_name]["Record"]["Draw"] = 0
        player_data[player_name]["Unfinished"] = {}
        player_data[player_name]["Unfinished"]["Mark"] = None
        player_data[player_name]["Unfinished"]["Moves"] = None
        player_data[player_name]["Unfinished"]["CPUMoves"] = None
        player_data[player_name]["Unfinished"]["Board"] = None
        self.loadPlayer(player_name, player_data)

    def resetGame(self):
        self.board = Board()
        self.player.moves = []
        self.computer.moves = []
        self.player.mark = str()
        self.computer.mark = str()
        self.current_player = str()

    def play(self):
        self.resetGame()
        self.player.player_name = input(_NAME_PROMPT_STR)
        self.loadGame(self.player.player_name)
        self.player.mark = input(_MARK_STR)
        self.computer.mark = _MARK_INVERT[self.player.mark]
        self.current_player = self.player.player_name
        self.coinFlip()
        self.playRound()

    def coinFlip(self):
        print(_COIN_TOSS_STR)
        coin = random.randint(0, 1)
        if coin == 0:
            print(_TOSS_RESULT_STR.format(self.player.player_name))
            self.current_player = self.player.player_name
        else:
            print(_TOSS_RESULT_STR.format(self.computer.player_name))
            self.current_player = self.computer.player_name

    def playRound(self):
        while not self.board.isFull():
            if self.current_player == self.player.player_name:
                self.playerTurn()
                if self.board.isFull():
                    break
                self.computerTurn()
            else:
                self.computerTurn()
                if self.board.isFull():
                    break
                self.playerTurn()
        self.endRound()

    def playerTurn(self):
        #check win
        move = input(_ENTER_MOVE_STR.format(self.player.player_name, _MOVE_STRINGS[len(self.player.moves)]))
        move = move.split(',')
        move = [int(move[0]), int(move[1])]
        while not self.board.isValidMove(move):
            move = input(_ENTER_MOVE_STR.format(self.player.player_name, _MOVE_STRINGS[len(self.player.moves)]))
            move = move.split(',')
            move = [int(move[0]), int(move[1])]
        self.board.makeMove(move, self.player.mark)
        self.player.moves.append(move)
        print(self.board)

    def computerTurn(self):
        move = self.board.getMove()
        self.board.makeMove(move, self.computer.mark)
        self.computer.moves.append(move)
        print(self.board)

    def endRound(self):
        if self.board.isFull():
            print(_DRAW_STR)
            self.draws += 1
        elif self.player.wonRound():
            print(_WIN_STR.format(self.player.player_name))
            self.wins += 1
        else:
            print(_WIN_STR.format(self.computer.player_name))
            self.losses += 1
        self.saveGame()

class Player:
    def __init__(self):
        self.player_name = str()
        self.mark = str()
        self.wins = 0
        self.losses = 0
        self.draws = 0
        self.mark = str()
        self.moves = []
        self.firstGame = True

    def __str__(self):
         return _RECORD_STR.format(self.wins, self.losses, self.draws)

class Board:
    def __init__(self):
        self.board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
        self.moves = 0

    def isValidMove(self, move):
        if move[0] < 3 and move[1] < 3:
            if self.board[move[0]][move[1]] == ' ':
                return True
        return False
    
    def makeMove(self, move, mark):
        if self.isValidMove(move):
            self.board[move[0]][move[1]] = mark
            self.moves += 1
        return self.isWinningMove(move, mark)

    def isBoardFull(self):
        if self.moves == 9:
            return True
        return False
    
    def getMove(self):
        move = [random.randint(0, 2), random.randint(0, 2)]
        while not self.isValidMove(move):
            move = [random.randint(0, 2), random.randint(0, 2)]
        return move

    def isWinningMove(self, move, mark):
        if self.board[move[0]][0] == self.board[move[0]][1] == self.board[move[0]][2] == mark:
            return True, _ROW_STR
        if self.board[0][move[1]] == self.board[1][move[1]] == self.board[2][move[1]] == mark:
            return True, _COL_STR
        if move[0] == move[1] or move[0] + move[1] == 2:
            if self.board[0][0] == self.board[1][1] == self.board[2][2] == mark or \
               self.board[0][2] == self.board[1][1] == self.board[2][0] == mark:
                    return True, _DIAG_STR
        return False, None

    def __str__(self):
        for i in range(9):
            if i % 2 == 1 or i == 0:
                print(_BOARD_ODD_STR)
            else:
                print(_VERTICAL_STR, end='')
                for j in range(3):
                    print(_MARK_STR.format(self.board[i//2][j]), end='')
                print()

print(_WELCOME_STR)
game = Game()
while not game.quit:
    game.play()
game.saveGame()
print(_GOODBYE_STR)
