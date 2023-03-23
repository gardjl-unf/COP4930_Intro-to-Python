from game import Game
from json import load

_VARIABLES_FILE = "strings.json"

with open(_VARIABLES_FILE, 'r+') as file_object:
    strings = load(file_object)

print(strings["_WELCOME_STR"])
game = Game(strings)
while not game.quit:
    game.play()
game.save_game()
print(strings["_GOODBYE_STR"])
