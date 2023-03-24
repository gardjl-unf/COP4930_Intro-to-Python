from random import randint

_MOVE_STRINGS = ["1st","2nd","3rd","4th","5th","6th","7th","8th","9th"]

class Board:
    def __init__(self, strings):
        self.strings = strings
        self.board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
        self.moves = 0

    def reset(self):
        self.board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
        self.moves = 0
    
    def is_valid_move(self, move):
        if move[0] < 3 and move[1] < 3:
            if self.board[move[0]][move[1]] == ' ':
                return None
            else:
                return self.strings["_DUPLICATE_FAIL_STR"].format(move[0], move[1])
        else:
            return self.strings["_SANITY_FAIL_STR"]
    
    def make_move(self, player, move):
        result = self.is_valid_move(move)
        if result is None:
            self.board[move[0]][move[1]] = player.mark
            self.moves += 1
            player.moves.append(move)
            print(self.strings["_MOVE_STR"].format(player.name, _MOVE_STRINGS[len(player.moves) - 1], move[0], move[1]))
            winning = self.check_win(player)
            if winning is not None:
                print(winning)
        else:
            print(result)
        return result
    
    def getMove(self):
        move = [randint(0, 2), randint(0, 2)]
        while not self.is_valid_move(move) == None:
            move = [randint(0, 2), randint(0, 2)]
        return move

    def check_win(self, player):
        result = self.check_row(player)
        if result is None:
            result = self.check_column(player)
        if result is None:
            result = self.check_diagonal(player)
        return result

    def check_row(self, player):
        move = player.moves[-1]
        for i in range(3):
            if self.board[move[0]][i] != player.mark:
                break
            if i == 2:
                return self.set_win(player, self.strings["_ROW_STR"])

    def check_column(self, player):
        move = player.moves[-1]
        for i in range(3):
            if self.board[i][move[1]] != player.mark:
                break
            if i == 2:
                return self.set_win(player, self.strings["_COL_STR"])

    def check_diagonal(self, player):
        move = player.moves[-1]
        if move[0] == move[1]:
            for i in range(3):
                if self.board[i][i] != player.mark:
                    break
                if i == 2:
                    return self.set_win(player, self.strings["_DIAG_STR"])
        if move[0] + move[1] == 2:
            for i in range(3):
                if self.board[i][2 - i] != player.mark:
                    break
                if i == 2:
                    return self.set_win(player, self.strings["_DIAG_STR"])
        return None
        
    def set_win(self, player, direction):
        print(self)
        player.winner = True
        player.wins += 1
        return self.strings["_WIN_STR"].format(direction, player.mark) + '\n' + \
               self.strings["_RESULT_STR"].format(player.name)
    
    def updateBoard(self, player):
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
