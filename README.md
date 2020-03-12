### Overview
A fun personal project to create a simple yet working minesweeper game that is run inside of a terminal.
This was created from scratch using python, and was done to learn and have a better understanding of the language.

### Structure
The  game is comprised of two classes and a driver.
There is a tile class which represents one of the tiles that a user can interact with (number, bomb, blank),
and a board class witch uses the tiles to form the board.
The driver runs the game and allows the user to enter commands to interact with the board.

### Interface
Due to the use of a terminal the interface does not include a GUI and is run inside of the terminal.
Updates to the game are printed to the terminal each time the board changes.
Any actions the user takes are done using commands.
<Insert Picture Here of board>

### User Actions
The command structure allows the user to input commands to interact with the game.
These actions can reset and create new boards, reveal and flag tiles, and move the player cursor around.
There are also help commands in case the user needs more details for any specific command.
<Insert picture of commands here> 
  
To more easily interact with the game a player cursor was added.
The cursor will hover over one of the tiles in the board and can be moved.
Instead of entering a command the user can enter a "quick action".
A quick action is an alternative method for inputting commands, but with a single number 0-9.
The idea was that the number pad would be used to make use of this more intuative.
These actions are done centered around the curser.
Most of these shift the cursor around; i.e. 8 moves the cursor up, and 3 moves the cursor down and to the right.
but a couple will act upon the tile the cursor is over. 5 will reveal the tile, and 0 will flag it.
< Add  images>

### Possible Improvments
As this is run in a terminal and uses a command structure, there is no GUI for this.
The commands take a little more time then simply clicking a tile.
A GUI could be created and the commands could be scrapped. 

Since only clear text is used it can be difficult to quickly determine what a tile is.
If I go over this again perhaps I'll work on displaying the board differently. 

Finally improving some basic user experience.
The cursor could wrap around instead of stopping at the board edges.
A legend could be added to help users determine what a tile symbol is; i.e. \# for a non-revealed tile.
