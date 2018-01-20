import cs50

def main():
    # prompts user and keeps prompting if input is not valid
   # height = prompt()
    height = prompt()
    while height < 0 or height > 23:
        height = prompt()
    # initialize the initial amount of hashes and spaces
    hashes = 1
    spaces = height -1

    #prints double pyramid
    for i in range(height):
        prints(spaces)
        printh(hashes)
        print("  ", end = "")
        printh(hashes)
        prints(spaces)
        ## decrease the amount of spaces, increase the amount of hashes
        spaces -= 1
        hashes += 1
        # print new line
        print()


#prompts the user for height
def prompt():
    print("Height: ", end ="")
    height = cs50.get_int()
    return height


def prints(spaces):
    for i in range(spaces):
        print(" ", end ="")


def printh(hashes):
    for i in range(hashes):
        print("#", end ="")

if __name__ == "__main__":
    main()