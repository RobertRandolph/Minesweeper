# board.py
# Author: Wolf
# Created: 08/15/2019
# Minesweeper board and tiles

import random

# Tile of the minesweeper board
# Interacted with by the user
# Types: blank, number, bomb
class Tile:
    # Constructor
    def __init__(self):
        self.reset()

    # Resets the tile to its default values
    def reset(self):
        self.type = 'blank'     # Type of tile
        self.adjBombs = 0       # Number of adjacent bombs
        self.revealed = False   # Whether or not the tile is revealed to the player
        self.flagged = False    # Whether or not the tile has been flagged by the player

# Board for the game.
# Holds a list of tiles.
# Player Can reveal and flag tiles given a set of coordinates...
# or at the player cursor if no coordinates were given
# Player cursor highlights a tile at a set of coordiantes
# Cursor can be moved around by the player.
# Can create a new board given a size and bomb count
# Bomb count is optional, and will default to 25% of the board
# Can reset the board using the same size and bomb count
# Keeps track of game state: 0 Playing, 1 Win, 2 Lost
# Sample Board Layout
# Bombs: 3
# //===========\\ Y
# || # # # 2 # || 5
# || 1 1 2 2 1 || 4
# ||       1 1 || 3
# || 1 1   1 # || 2
# || F 1   1 # || 1
# \\===========//
#  X 1 2 3 4 5
class Board:
    # Constructor
    def __init__(self):
        # Init
        self.__tiles = list()   # Empty list
        self.createBoard(10)    # Creating the inital board

    # @Parem size: Dimensions of the board. Must be greater then 3
    # @Parem bombs: Number of bombs on the board. Must be greater then 0.
    # Create a new board with the given size and bomb count.
    # There must be at least 9 guaranteed non-bomb tiles
    # Bomb count is optional.
    # If a bomb count wasn't set, then 25% of the tiles become bombs
    def createBoard(self, size: int, bombs: int = 0):
        # Validating input
        if size > 3: self.__size = size
        if bombs > 0 and bombs < self.__size**2 - 8: self.__bombs = bombs
        else: self.__bombs = int(self.__size**2*.25)   # 25% of tiles are bombs

        # Creating tiles
        self.__tiles.clear()
        self.__tiles = [Tile() for i in range(self.__size**2)]

        # Setting player cursor
        self.__cursor = (1, 1)

        # Initalizing game data
        self.reset()

    # Adds bombs to the board
    # Won't add bombs around the first tile revealed
    # Ensures that first move will always work
    def __addBombs(self):
        # Init
        restricted = set()  # Set of board coordinates that are restricted
        x = self.__cursor[0]
        y = self.__cursor[1]

        # Restricting adjacent tiles
        for i in range(-1, 2):
            for j in range(-1, 2):
                if not self.__validCoordinates(x + i, y + j): continue
                restricted.add((x + i, y + j))

        # Adding bombs to the board
        for i in range(self.__bombs):
            # Getting a random non-restricted tile
            while (x, y) in restricted:
                x = random.randint(1, self.__size)
                y = random.randint(1, self.__size)

            # Getting tile
            # Adding tile to restricted list
            # Setting tile to bomb
            tile = self.__getTile(x, y)
            restricted.add((x, y))
            tile.type = 'bomb'

            # Updating adjacent tile bomb counts
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if not self.__validCoordinates(x + i, y + j): continue
                    tile = self.__getTile(x + i, y + j)
                    if tile.type == 'bomb' : continue   # Skipping if tile is a bomb
                    tile.type = 'number'    # Setting tile type to number
                    tile.adjBombs += 1      # Incrimenting adjbomb count

    # Resets board with the current size and bomb count
    def reset(self):
        # Resetting tiles
        for tile in self.__tiles: tile.reset()

        # Resetting game information
        self.__gameState = 0        # State of the game, playing 0, win 1, lost 2
        self.__revealedTiles = 0    # Number of tiles that are current revealed
        self.__flaggedTiles = 0     # Number of tiles that are currently flagged

        # Resetting flags
        self.__gameState = 0        # State of the game, playing, win, lost
        self.__firstMove = True     # Whether the first tile revealed is the first one
        self.__revealedTiles = 0    # Number of tiles that are current revealed
        self.__flaggedTiles = 0     # Number of tiles that are currently flagged

    # Moves the player cursor to the given coordinates
    def moveCursor(self, x: int, y: int):
        # Validating coordinates
        if not self.__validCoordinates(x, y): return
        self.__cursor = (x, y)  # Setting coordinates

    # Shifts the cursor towards the given direction.
    # Can reveal or flag a tile.
    # Used for quick actions. Ideally used by the numberpad.
    # Directions: (Same as number pad)
    # 7 8 9
    # 4   6
    # 1 2 3
    # 5 will flag current tile
    # 0 will reveal current tile
    def shiftCursor(self, d: int):
        # Checking if direction is inbounds
        if d < 0 or d > 9: return

        # Getting cursor coordinates
        x = self.__cursor[0]
        y = self.__cursor[1]

        # Checking direction
        if d == 0: self.revealTile()
        elif d == 5: self.flagTile()
        elif d == 8: y += 1
        elif d == 4: x -= 1
        elif d == 6: x += 1
        elif d == 2: y -= 1
        elif d == 7:
            x -= 1
            y += 1
        elif d == 9:
            x += 1
            y += 1
        elif d == 1:
            x -= 1
            y -= 1
        elif d == 3:
            x += 1
            y -= 1

        # Validating new coordinates
        if (d != 0 or d != 5) and self.__validCoordinates(x, y): self.__cursor = (x, y)

    # Reveals the tile at the given coordinates
    # If no coordiantes are given uses player cursor coordinates
    def revealTile(self, x: int = 0, y: int = 0):
        # Checking if the game is over
        if self.__gameState != 0: return

        # Validating coordinates
        if not self.__validCoordinates(x, y):
            x = self.__cursor[0]
            y = self.__cursor[1]
        else: self.__cursor = (x, y)

        # Checking if this is the first move of the game
        if self.__firstMove:
            self.__firstMove = False
            self.__addBombs()
            self.__revealCascade()
            return

        # Getting tile
        tile = self.__getTile(x, y)

        # Skips if tile is revealed or flagged
        if tile.revealed or tile.flagged: return

        # Checking tile types
        if tile.type == 'blank': self.__revealCascade() # Revealing and cascading tile(s)
        elif tile.type == 'number':
            tile.revealed = True        # Revealing the tile
            self.__revealedTiles += 1   # Incrimenting revealed tile count
        else:   # Tile is a bomb
            self.__gameState = 2    # Game lost
            # Revealing all bombs on the board
            for tile in self.__tiles:
                if tile.type == 'bomb':
                    tile.revealed = True
                    tile.flagged = False

        # Checking if game was won
        if self.__revealedTiles == self.__size**2 - self.__bombs: self.__gameState = 1

    # Flags or de-flags the tile at the given coordinates
    # If no coordinates are given uses player cursor coordinates instead
    def flagTile(self, x: int = 0, y: int = 0):
        # Checking if the game is over
        if self.__gameState != 0: return

        # Validating coordinates
        if not self.__validCoordinates(x, y):
            x = self.__cursor[0]
            y = self.__cursor[1]
        else: self.__cursor = (x, y)

        # Getting tile
        tile = self.__getTile(x, y)

        # Skips if tile is revealed
        if tile.revealed: return

        # Flagging / deflagging tile
        tile.flagged = not tile.flagged

        # Incrimenting / decrimenting flagged tile count
        if tile.flagged: self.__flaggedTiles += 1
        else: self.__flaggedTiles -= 1

    # Reveals all non-bomb adjacent tiles at the cursor
    # If a revealed tile is a blank, then reveals new adjacent tiles as well.
    # Avoids a recursive version as this can be called many times for a sufficantly large board
    def __revealCascade(self):
        # Init
        process = {self.__cursor}   # Tiles to be processed in current iteration
        nextp = set()               # Tiles to be processed next iteraiton

        # Processing tiles until finished
        while len(process):
            for (x, y) in process:
                # Revealing adjacent tiles
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if not self.__validCoordinates(x + i, y + j): continue
                        tile = self.__getTile(x + i, y + j)
                        if tile.revealed or tile.type == 'bomb': continue   # Skipping revealed and bomb tiles
                        tile.revealed = True                                # Revealing tile
                        if tile.flagged: self.__flaggedTiles -= 1           # Checking if tile was flagged
                        self.__revealedTiles += 1                           # Incrimenting revealed tile count
                        if tile.type == 'blank': nextp.add((x + i, y + j))  # Cascading blank tiles
            
            # Transfering tiles to be processed
            process = nextp.copy()          
            nextp.clear()

        # Checking if game was won
        if self.__revealedTiles == self.__size**2 - self.__bombs: self.__gameState = 1        

    # Returns the games state
    def getGameState(self):
        return self.__gameState

    # Returns the number of bombs in the game
    # This is decrimented by flagged tiles.
    # If the number of flagged tiles is more then the bomb count...
    # then the number will be negative
    def getRemainingBombs(self):
        return self.__bombs - self.__flaggedTiles

    # Prints the board to the terminal
    def print(self):
        # Init
        line = self.__size
        column = 0
        x = self.__cursor[0]
        y = self.__cursor[1]

        # Top of board
        board = '//=' + '==' * self.__size + '\\\\\n'

        # Adding tiles
        for tile in self.__tiles:
            # Border
            if column == 0: board += '||'                                   # Left border
            if x == column + 1 and y == line: board += '>'                  # Player Cursor Start
            elif x == column and y == line: board += '<'                    # Playor Cursor End
            else: board += ' '                                              # No Player Cursor

            # Tiles
            if not tile.revealed and tile.flagged: board += 'F'             # Non-Revealed Flagged Tile
            elif not tile.revealed: board += '#'                            # Non-Revealed Tile
            elif tile.type == 'blank': board += ' '                         # Blank tile
            elif tile.type == 'number': board += str(tile.adjBombs)         # Number tile
            elif tile.type == 'bomb': board += 'X'                          # Bomb tile

            # Border
            if column == self.__size - 1:
                if x == column + 1 and y == line: board += '<'              # Player Cursor End
                else: board += ' '                                          # No Player Cursor
                board += '|| ' + str(line) + '\n'                           # Right border and row number

            # Incriments
            column = (column + 1) % self.__size                             # Incrimenting column
            if column == 0: line -= 1                                       # Decrimenting line

        # Adding Bottom of board
        board += '\\\\=' + '==' * self.__size + '//\n'

        # Adding Column numbers
        rows = len(str(self.__size))    # Number of rows needed
        for r in range(rows):
            # Adding spacing
            board += ' ' * 3
            if r > 0: board += '  ' * (10**r - 1)

            # Adding number
            for i in range(10**r, self.__size + 1):
                num = str(i)
                board += num[r] + ' '
            board += '\n'

        # Printing board
        print(board)

    # Determines whether the given coordinates are valid.
    # Returns true if they are valid, and false otherwise.
    def __validCoordinates(self, x: int, y: int):
        # Checking if coordiantes are within range
        if x < 1 or x > self.__size or y < 1 or y > self.__size: return False
        return True

    # Returns the tile at the given coordiantes
    def __getTile(self, x: int, y: int):
        rx = x - 1                      # Calculating x index
        ry = (y*-1) + self.__size       # Calculating y index
        index = ry*self.__size + rx     # Calculating tile index
        return self.__tiles[index]      # Returning tile