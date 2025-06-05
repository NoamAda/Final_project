import random

PARAMETERS = ['color', 'num', 'shape', 'shading']
COLORS = ['green', 'purple', 'red']
SHADING = ['solid', 'striped', 'open']
SHAPES = ['oval', 'diamond', 'squiggle']
NUMBER = [1,2,3]

NO_SET = -2
SHOW_HINT = -1
LEN_BOARD = 12

def print_board(board):
    for card in board:
        print(card)


def shuffle_deck(deck):
    random.shuffle(deck)

def create_card(Color,Shape,Shadeing,Num):
    card = {"Color": Color,"Shape":Shape,"Shadeing":Shadeing,"Num":Num}
    return card

def is_set(card1,card2,card3):
    for i in PARAMETERS:
        if card1[i] == card2[i]==card3[i] or card1[i] != card2[i] != card3[i]:
            return True


        else:
            return False

def create_deck():
    deck = []
    for c in COLORS:
        for a in SHAPES:
            for r in SHADING:
                for d in NUMBER:
                    card = create_card(c,a,r,d)
                    deck.append(card)

    shuffle_deck(deck)
    return deck

def create_board(deck):
    board = []
    for i in range(LEN_BOARD):
        board.append(deck.pop(0))
    return board