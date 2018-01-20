import sys
import cs50

def main():
    if len(sys.argv) != 2:
        print("ERROR, you did not give me two command line arguments")
        return 1
    key = sys.argv[1]
    if not key.isnumeric():
        print("ERROR, you did not give me a number")

    plaintext = prompt()
    res = calculate(plaintext, key)
    printres(res)
    return 0

def prompt():
    print("plaintext: ", end="")
    plaintext = cs50.get_string()
    return plaintext
    i = 1

def calculate(plaintext, key):
    lis = list(plaintext)
    print(lis)
    for i in lis:
        print(lis[i]
    res = key
    return res


def printres(res):
    print("Result: {}".format(res))


if __name__ == "__main__":
    main()