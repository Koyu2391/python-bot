first = int(input("enter firt number: "))
second = int(input("Enter second number: "))

operand = input("Enter the operand")

if (operand == '+') :
    print(first+second)
if (operand == '-') : 
    print(first-second) 
if (operand == '*') :
    print(first*second)
if (operand == '/') :
    print(first/second)
    
else :
    print("Invalid Operand Entered")