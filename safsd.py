import random
from os import times


def game(side,num1,num2,g,times,action_times,schum):
    times = int(input("how many times you want to play?"))
    times = action_times
    while times>0:
        num1=random.randint(1,side)
        num2=random.randint(1,side)
        print(num1,num2)
        g = 1
        while num1!=num2:
            num1 = random.randint(1, side)
            num2 = random.randint(1, side)
            print("attempt number" , g ,":",num1,num2 )
            g+=1
        schum += g
        if g<10:
            print(g,"Times! , preety nice")
        else:
            print(g , "times??! damn what is that luck")
        times -= 1
        print("come on we have " , times , "times to play!")
print(game(6,0,0,0,0,0,0))
def action_game(memutza):
  game(6,0,0,0,0,0,0)
  memutza = (int(times) * int(schum))/times