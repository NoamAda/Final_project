lst=[["tamar",88],["ella",97]]
best = ["nun",0]


def len_lst(lst):
    len_lst = len(lst)
    return len_lst

def memurtza(lst):
    memutza = 0
    for i in range(len(lst)):
        memutza = memutza + lst[i][1]
    return memutza / len(lst)

def mitztaien(lst,best):
    for i in range(len(lst)):
        if lst[i][1] > best[1]:
            best = lst[i]
    return best

def main():
    print("there is " ,len_lst(lst), " students in class")
    print("the memutza of the class is " , memurtza(lst))
    print("and the best student is ", mitztaien(lst,best) ,"high score!")

main()