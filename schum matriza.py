

def matriz(a,b):
    c = a
    for row in range(len(b)):
        for cal in range(len(b[0])):
            c[row][cal] += b[row][cal]
            print(c[row][cal],end =",")
        print()

def main():
    a = [[2,1],[4,8],
         [2,9],[8,0],
         [6,7],[7,0]]

    b = [[3,6],[1,2],
         [4,7],[9,0],
         [2,9],[1,2]]

    print(matriz(a,b))




main()