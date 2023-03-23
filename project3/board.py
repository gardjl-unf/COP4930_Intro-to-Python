from random import randint
from player import Player

_MOVE_STRINGS = ["1st","2nd","3rd","4th","5th","6th","7th","8th","9th"]

class Board:
    def __init__(self, strings):
        self.strings = strings
        self.board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
        self.moves = 0
    
    def isValidMove(self, move):
        if move[0] < 3 and move[1] < 3:
            if self.board[move[0]][move[1]] == ' ':
                return None
            else:
                return self.strings["_DUPLICATE_FAIL_STR"].format(move[0], move[1])
        else:
            return self.strings["_SANITY_FAIL_STR"]
    
    def makeMove(self, player, move):
        result = self.isValidMove(move)
        if result is None:
            self.board[move[0]][move[1]] = player.mark
            self.moves += 1
            player.moves.append(move)
            print(self.strings["_MOVE_STR"].format(player.name, _MOVE_STRINGS[len(player.moves)], move[0], move[1]))
            winning = self.isWinningMove(player)
            if winning is not None:
                print(winning)
        else:
            print(result)
        return result
    
    def getMove(self):
        move = [randint(0, 2), randint(0, 2)]
        while not self.isValidMove(move) == None:
            move = [randint(0, 2), randint(0, 2)]
        return move

    def isWinningMove(self, player):
        move = player.moves[-1]
        for i in range(3):
            if self.board[move[0]][i] != player.mark:
                break
            if i == 2:
                player.winner = True
                player.wins += 1
                print(self.strings["_WIN_STR"].format(self.strings["_ROW_STR"], player.mark))
                return self.strings["_RESULT_STR"].format(player.name)      
        for i in range(3):
            if self.board[i][move[1]] != player.mark:
                break
            if i == 2:
                player.winner = True
                player.wins += 1
                print(self.strings["_WIN_STR"].format(self.strings["_COL_STR"], player.mark))
                return self.strings["_RESULT_STR"].format(player.name)
        if move[0] == move[1]:
            for i in range(3):
                if self.board[i][i] != player.mark:
                    break
                if i == 2:
                    player.winner = True
                    player.wins += 1
                    print(self.strings["_WIN_STR"].format(self.strings["_DIAG_STR"], player.mark))
                    return self.strings["_RESULT_STR"].format(player.name)
        if move[0] + move[1] == 2:
            for i in range(3):
                if self.board[i][2-i] != player.mark:
                    break
                if i == 2:
                    player.winner = True
                    player.wins += 1
                    print(self.strings["_WIN_STR"].format(self.strings["_DIAG_STR"], player.mark))
                    return self.strings["_RESULT_STR"].format(player.name)
    
    def updateBoard(self, player):
        if len(player.moves) > 0:
            for move in player.moves:
                self.board[move[0]][move[1]] = player.mark
                self.moves += 1

    def __str__(self):
        board_str = '\n'
        for i in range(7):
            if i % 2 == 2 or i % 2 == 0:
                board_str += self.strings["_BOARD_EVEN_STR"] + '\n'
            else:
                board_str += self.strings["_BOARD_ODD_STR"].format(self.board[i//2][0], self.board[i//2][1], self.board[i//2][2]) + '\n'
        return board_str
