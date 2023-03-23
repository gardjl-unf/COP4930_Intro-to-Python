class Player:
    def __init__(self, strings):
        self.strings = strings
        self.player_name = str()
        self.mark = str()
        self.wins = 0
        self.losses = 0
        self.draws = 0
        self.mark = str()
        self.moves = []
        self.winner = False

    def reset(self):
        self.moves = []
        self.mark = str()
        self.winner = False

    def load_player(self, player_name, player_data):
        self.name = player_name
        self.wins = player_data[0]
        self.losses = player_data[1]
        self.draws = player_data[2]
        if self.wins + self.losses + self.draws != 0:
            print(self.strings["_RETURNING_STR"].format(self.name))

    def load_moves(self, moves):
        self.moves = moves

    def print_moves(self):
        if self.moves is not None:
            print(self.strings["_MOVES_STR"].format(self.name), end='')
            for move in self.moves:
                if move != self.moves[-1]:
                    print(self.strings["_MOVES_LIST_STR"].format(move), end='')
                else:
                    print(move, end='\n')
            print()

    def new_player(self, player_name):
        print(self.strings["_FIRST_TIME_STR"])
        player_data = [0, 0, 0]
        self.load_player(player_name, player_data)

    def make_CPU(self):
        self.name = self.strings["_COMPUTER_NAME"]

    def __str__(self):
         return self.strings["_RECORD_STR"].format(self.wins, self.losses, self.draws)