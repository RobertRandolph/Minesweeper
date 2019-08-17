# driver.py
# Author: Wolf
# Created: 08/16/2019
# Driver to run a minesweeper game

from board import Board

# List of commands that can be used by the player
# As well as detailed descriptiosn for each command
commands = """Commands:
    New: Resets the board using the same size and bomb count.
    C <size> <bombs>: Creates a new board with the given size and bomb count. Bomb count is optional.
    M: <x> <y>: Moves the cursor to the given coordinates. Cursor can be used for quick actions.
    R: <x> <y>: Reveals the tile at the given coordinates, or at the cursor.
    F: <x> <y>: Flags / De-Flags the tile at the given coorinates, or at the cursor.
    Exit: Closes the game.
    Help: Displays the current list of commands.
    Help <command>: Gives further details on the command."""

new = """Command: New
    Resets the board using the same size and bomb count.
    This is a new setup and the bombs will be in differant locations."""

c = """Command: C <size> <bombs>
    Creates a new board with the given size and bombs.
    A Board must have at least 9 non-bomb tiles.
    Size will change the dimensions of the board.
    Size dictates how many tiles are present on the board.
    Size must be greater then 3.
    Bombs dictates how many tiles on the board are bombs.
    Bombs must be greater then 0.
    Bomb count is optional.
    If no bomb count is given then 25% of board tiles will be converted to bombs."""

m = """Command: M <x> <y>
    Moves the cursor to the given coordinates.
    The cursor can be used for quick actions.
    Quick actions are best used by utilizing the numberpad on your keyboard.
    Quick actions take in a single number as input: 0-9
    Depending on the number a differant action will occur.
    0 will reveal the tile at the cursor.
    5 will flag or de-flag the tile at the cursor.
    The rest of the numbers will shift the cursor by one unit.
    Using '5' as the focal point, the cursor will shift towards the number pressed on the numberpad.
    For example, pressing '8' will move your cursor up."""

r = """Command: R <x> <y>
    Reveals the tile at the given coordiantes.
    If no coordinates are given it will instead reveal the tile at the cursor.
    Flagged tiles will not be revealed until unflagged."""

f = """Command: F <x> <y>
    Flags or De-Flags the tile at the given coordinates.
    If no coordinates are given it will instead flag or de-flag the tile at the cursor."""

exitc = """Command: Exit
    Closes the game."""

helpc = """Command: Help
    Displays the current list of commands.
    If a command is given along with it, the command is explained in further detail."""    

# Driver
def main():
    # Init
    board = Board()

    # Displaying Commands
    print(commands)

    # Playing Game
    while True:
        # Printing bombs, board, and game state
        print('\nBombs:', board.getRemainingBombs())
        board.print()
        gameState = board.getGameState()
        if gameState == 1: print('You Won!')
        elif gameState == 2: print('You Lost!')

        # Getting user input
        command: str = input('Command: ')   # Getting command
        params = command.split()            # Getting parameters
        inputs = len(params)                # Getting number of inputs
        p1 = p2 = 0                         # Init

        # Checking if too many inputs
        if inputs > 3:
            print("Invalid Command")
            continue

        # Consolidatding inputs
        try:
            command = params[0]
            if inputs > 1 and command.lower() == 'help': p1 = params[1]
            elif inputs > 1: p1 = int(params[1])
            if inputs > 2: p2 = int(params[2])
        except:
            print("Invalid Command")
            continue

        # Checking commands and inputs
        if inputs == 1 and command.isdigit(): board.shiftCursor(int(command))
        elif inputs == 1 and command.lower() == 'new': board.reset()
        elif inputs != 1 and command.lower() == 'c': board.createBoard(p1, p2)
        elif inputs == 3 and command.lower() == 'm': board.moveCursor(p1, p2)
        elif inputs != 2 and command.lower() == 'r': board.revealTile(p1, p2)
        elif inputs != 2 and command.lower() == 'f': board.flagTile(p1, p2)
        elif inputs == 1 and command.lower() == 'exit': break
        elif inputs != 3 and command.lower() == 'help':
            if inputs == 1: print(commands)
            elif p1.lower() == 'new': print(new)
            elif p1.lower() == 'c': print(c)
            elif p1.lower() == 'm': print(m)
            elif p1.lower() == 'r': print(r)
            elif p1.lower() == 'f': print(f)
            elif p1.lower() == 'exit': print(exitc)
            elif p1.lower() == 'help': print(helpc)
            else: print('Invalid Command')
        else: print('Invalid Command')

# Running main when script starts
if __name__ == '__main__': main()