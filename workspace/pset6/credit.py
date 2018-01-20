import cs50

def main():
    number = prompt()
    while number < 0:
        number = prompt()

    total = calc(number)
    check(total, number)
    # That's it :)

def prompt():
    print("Number: ",end="")
    number = cs50.get_int()
    return number

# multiply every other digit by 2, starting with the 2nd to last digit and add them together
def calc(number):
    #make a list from the number
    numberlist = [int(x) for x in str(number)]
    total = 0
    i = len(numberlist) -2
    # addresses initially the 2nd last digit, multiplies by two, adds to sum and goes down two steps, splits digit if multiplication yield two digits
    while i >= 0:
        number = str(numberlist[i] * 2)
        if len(number) == 1:
            total = total + int(number)
        else:
            total = total + int(number[0]) + int(number[1])
        i -= 2

    i = len(numberlist) -1
    # addresses initially the last digit, add to the total and go down two steps
    while i >=0:
        total = total + numberlist[i]
        i -= 2

    return total


# true if total %10 = 0
def check(total, number):

    if total % 10 != 0 or len(str(number)) > 16:
        print("INVALID")
        return False

    if(str(number)[0]) == str(4):
        print("VISA")
        return True
    elif len(str(number)) == 15:
        print("American Express")
        return True
    elif len(str(number)) == 16:
        print("MasterCard")
        return True

if __name__ == "__main__":
    main()