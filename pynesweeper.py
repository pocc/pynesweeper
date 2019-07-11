"""
PYNESWEEPER: A fine implementation of minesweeper

This is a python TUI that produces a gameboard that look like this:
   1 2 3 4 5 6 7 8
 A * * * * * * * * 
 B * * * * * * * * 
 C * * * * * * * * 
 D * * * * * * * * 
 E * * * * * * * * 
 F * * * * * * * * 
 G * * * * * * * * 
 H * * * * * * * * 

*       : Unchosen space
✵       : mine 
' ',1-8 : number of adjacent mines 

It will mimic Windows Minesweeper Beginner with 8x8 and 10 mines.
"""

import os
import random
import string

MAX_ADJACENCIES = 8

class Board():
    """Class Board keeps track of game state
    Board keeps track of the initial board with cells, 9 being mine, 0 being not-mine
    """
    def __init__(self, side_len: int, num_mines: int):
        self.side_len = side_len
        self.num_mines = num_mines
        self.num_cells = side_len * side_len
        self.cells = [[0 for _ in range(side_len)] for _ in range(side_len)]
        self.game_over = False
        self.moves = [[False for _ in range(side_len)] for _ in range(side_len)]
        self.last_move = [-1,-1]
        self.mines = []
        self.move_ct = 0
        self.board_header_str = self.gen_board_header()

        self.gen_board()

    def gen_board_header(self) -> str:
        header_str = "  P Y N E S W E E P E R\n\n"
        if self.side_len > 10:
            header_str += self.gen_tens_line()
        header_str += "  "
        for i in range(self.side_len):
            digit = (i+1)%10
            header_str += " " + str(digit)
        return header_str

    def gen_board(self):
        """This generates a board with n mines"""
        mine_locs = self.num_mines*[0]
        coords = random.sample(range(0, self.num_cells - 1), self.num_mines) 
        for coord in coords:
            x = coord//self.side_len
            y = coord%self.side_len
            self.mines.append([x,y])
            x0 = x == 0
            xmax = x == self.side_len - 1
            y0 = y == 0
            ymax = y == self.side_len - 1
            if not x0: 
                self.cells[x-1][y] += 1 
                if not y0:
                    self.cells[x-1][y-1] += 1 
                if not ymax:
                    self.cells[x-1][y+1] += 1
            if not xmax:
                self.cells[x+1][y] += 1
                if not y0:
                    self.cells[x+1][y-1] += 1 
                if not ymax:
                    self.cells[x+1][y+1] += 1
            if not y0:
                self.cells[x][y-1] += 1 
            if not ymax:
                self.cells[x][y+1] += 1
        # Set each mine to 8, which is greater than what any other cell can have
        for x,y in self.mines: 
            self.cells[x][y] = MAX_ADJACENCIES
    
    def get_user_input(self):
        """Gets user string in the form of "A1" and store it.
        The user can make the same move at the same coordinates
        if they want.
        """
        last_row_letter = chr(self.side_len+64)
        last_col_number = self.side_len
        user_str = input("Show me a move! ")
        user_str[0].capitalize()
        while not (last_row_letter >= user_str[0] >= 'A' and user_str[1:].isdigit() and last_col_number >= int(user_str[1:]) >= 1):
            user_str = input("You entered an invalid move.\n"+
                    "The first character MUST be a letter between A and {}.\n".format(last_row_letter) + 
                    "The next character(s) MUST be a number betwen 1 and {}.\n".format(last_col_number) + 
                    "\nShow me a move! ")
        x = ord(user_str[0])-65
        y = int(user_str[1:])-1  # fencepost error
        if not self.moves[x][y]: # If this is a new move, add to the move count
            self.move_ct += 1
        self.moves[x][y] = True
        self.last_move = [x,y]

    def check_state(self) -> bool:
        return self.game_over

    def hit_mine(self) -> bool:
        """Checks if the user lost or not.""" 
        for coord in self.mines:
            if self.last_move == coord:
                return True
        return False

    def draw_board(self):
        """ Draw the board!"""
        board_str = self.get_board_str()
        # [-1, -1] is starting move (i.e. not user input)
        if self.last_move != [-1, -1] and self.hit_mine():
            self.game_over = True
            board_str = self.get_board_str()
            board_str = board_str.replace("8\n", "8 \n")
            board_str = board_str.replace("8 ", "\033[41;1m✺ \033[0m")
            board_str += "\n   💣 GAME OVER! 💣"
        elif self.move_ct == self.num_cells - self.num_mines:
            self.game_over = True
            board_str = board_str.replace("⁇\n", "⁇ \n")
            board_str = board_str.replace("⁇ ", "\033[41;1m⚑ \033[0m")
            board_str += "\n   🎉 YOU WIN! 🎉"
        clear()
        print(self.board_header_str)
        print(board_str)

    def get_board_str(self):
        board_str = ""
        row_letter = 64
        for i, line in enumerate(self.cells):
            row_letter += 1
            board_str += " " + chr(row_letter)
            for j, cell in enumerate(line):
                if self.game_over or self.moves[i][j]:
                    elem = str(cell)
                else:
                    elem = "⁇"
                board_str += " " + elem
            board_str += "\n"
        
        return board_str

    def gen_tens_line(self):
        """ Print like so to keep track of tens
            1                   2
        8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 ... 
        """
        tens_line = "  "
        ten_multiple = 1
        side_len = self.side_len
        while side_len > 10:
            tens_line += 19*' ' + str(ten_multiple)
            ten_multiple += 1
            side_len -= 10
        return tens_line + '\n'

def clear(): 
    if os.name == 'nt': # Windows
        os.system('cls') 
    else: # Everything else
        os.system('clear') 

def main():
    game_end = False

    print("""
    ~~~ Welcome to Pynesweeper! ~~~

Beginner:     8x8 board with 10 mines
Intermediate: 16x16 board with 40 mines
Expert:       24x24 board with 99 mines
""")
    side_len_str = input("For an NxN board, what is N? ")
    num_mines_str = input("How many mines? ")
    if not side_len_str.isdigit() or not num_mines_str.isdigit():
        print("Invalid integers entered! Exiting...")
        exit(1)
    side_len = int(side_len_str)
    num_mines = int(num_mines_str)
    if side_len < 1 or num_mines < 1:
        print("Invalid side lengths or number of mines. Both must be greater than 0. Exiting...")
        exit(1)
    if num_mines >= side_len*side_len:
        print("More mines than cells! Exiting...")
        exit(1)
    clear() # If not done here, screen flashes with text
    game = Board(side_len, num_mines)
    game.draw_board()  # Draw initial screen
    while not game_end:
        game.get_user_input()
        game.draw_board()
        game_end = game.check_state()

if __name__ == '__main__':
    main()
