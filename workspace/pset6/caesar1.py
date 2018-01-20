import sys
import cs50

def main():
    # error if the user did not give a key
    if len(sys.argv) != 2:
        print("ERROR, you did not give me a command line argument")
        return 1
    # error if the user did not give a key
    key = sys.argv[1]
    if not key.isnumeric():
        print("ERROR, you did not give me a number")
        return 1

    #prompt the user for plaintext
    plaintext = prompt()
    #calculate the encrypted text
    res = calculate(plaintext, key)

    # print result
    print("Result: {}".format(res))
    return 0

def prompt():
    print("plaintext: ", end="")
    plaintext = cs50.get_string()
    return plaintext

def calculate(plaintext, key):
    # initialize the string to be returned
    res = ""
    # create a list from the plaintext
    lis = list(plaintext)
    for i in lis:
        #transform the letter to an integer
        c = ord(i)
        #transform if i is lowercase
        if i.islower():
            res = res +chr(((c-97+int(key))%26)+97)
        #transform if i is uppercase
        elif i.isupper():
            res = res + chr(((c - 65+ int(key))%26)+65)
        # no transformation if neither uppercase nor lowercase
        else:
            res = res + chr(c)
    return res

def printres(res):
    #print r
    print("Result: {}".format(res))

if __name__ == "__main__":
    main()