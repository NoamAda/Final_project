import random
from operator import index


ROW = 5
COL = 5
PLAYER1 = "I"
PLAYER2 = "O"vfd
POS1 = (0,0)
POS2 = (0,0)
SNAKE = "~"
LATTER = "#"
snake_indx = []
snake_val = []
latter_indx = [""]
latter_val = []

board = [["S",0,0,0,0],
         [0,0,0,0,0],
         [0,0,0,0,0],
         [0,0,0,0,0],
         [0,0,0,0,"W"]]

def print_board(board):
    for row in range(ROW):
        current = "  "
        for col in range(COL):
            current += str(board[row][col]) + "  "
        print(current)

def roll_cube():
    return random.randint(1,4)

def turn(count):
    if count%2 == 0:
        return 2
    else:
        return 1


def random_position(board):
        for i in range(5):
            x = random.randint(1,4)
            y  = random.randint (0,4)
            posis = (x,y)
            snake_indx.append(posis)
            random_minus = random.randint(-10,0)
            snake_val.append(random_minus)
            board[x][y] = SNAKE
        for i in range(4):
            x = random.randint(1,4)
            y  = random.randint (0,3)
            posup = (x,y)
            latter_indx.append(posup)
            random_plus = random.randint(0,10)
            latter_val.append(random_plus)
            board[x][y] = LATTER
        return board


random_position(board)
print_board(board)
