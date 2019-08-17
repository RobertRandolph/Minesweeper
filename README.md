### Overview
A fun personal project to create a simple yet working minesweeper game that is run inside of a terminal.
This was created from scratch using python, and was mostly done for fun, and to learn python.
A board is created using a list of tiles, which are the individual pieces such as bombs and numbers.
The board follows a coordinate system and uses a basic command structure to interact with the game.

### Actions
The command structure allows the user to input commands to interact with the game.
These actions can reset and create new boards, reveal and flag tiles, and move the player cursor around.
There are also help commands in case the user needs more details for any specific command.

### Interface
Because this uses a terminal as an interface I added a player 'cursor' to improve clarity and usability.
The cursor will hover over a tile which can be moved around and used for "quick actions."
A quick action is an alternative method for inputting commands, but with a single number 0-9.
These actions are centered around the curser, and help the user more easily interact with the game.
Most of these shift the cursor around but a couple will act upon the tile the cursor is over.
This was intended to be used by a numeric keypad on a keyboard.

### Downsides
There are two major downside to this.
As this is run in a terminal and uses a command structure, there is no GUI for this.
The commands take a little more time then simply clicking a tile.
The other is that is can be difficult to quickly determine what a tile is.
If I go over this again perhaps I'll work on displaying the board differently.
