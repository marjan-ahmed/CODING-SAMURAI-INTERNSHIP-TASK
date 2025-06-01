print("Welcome to Simple Calculator".center(50))

num1 = int(input("Enter a number: "))
num2 = int(input("Enter a number: "))
opr = input("Enter an operation to perform (+, -, x, /): ")

match opr:
    case "+":
        print(f"{num1}+{num2}: {num1 + num2}")
    case "-":
        print(f"{num1}-{num2}: {num1 - num2}")
    case "x":
        print(f"{num1}*{num2}: {num1 * num2}")
    case "/":
        print(f"{num1}/{num2}: {num1 / num2}")