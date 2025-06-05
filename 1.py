from random import choice

doc = """
בקוד עצמו אני אתחיל בהצבה של הרשימות של החסה סלק וגזר לאחר מכאן אני אתחיל את הלולאות של הקלט
"""


#הצבה של הרשימות והמשתנים
signs = ["@","!","&"]
price = [10,12,15]
space = [3,0,1]
amount_of_obj = [1,1,1]
name = ["lettuce","carrot","beet"]
min_price = 0
budget = 0
i=0


#ההדפסה ההתחלתית שמסבירה מה כל דבר
print("!Welcome to MOUSTACHE - field planning assistant")
while i < 3:
    print(signs[i] + " = " +name[i])
    print(price[i])
    print(space[i])
    i += 1
budget = int(input("Enter field budget:"))
width = int(input("Enter field width:"))
while budget != 0:
    print("Remaining budget: " , budget)
    choice = input("Enter your choice:")
    if choice in name:
        if width%4==0:
            min_price = (width/4)*10
        else:
            r = width%4
            o = width-r
            min_price = ((o/4)*10)+10

    elif choice == "exit":
        break
    print("min_price ",min_price)




