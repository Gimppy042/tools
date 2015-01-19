def calc(numbers, op):

    if op.lower() == "mult":
        total = 1
        for num in numbers:
            total = total * num
            
    elif op.lower() == "add":
        total = 0
        for num in numbers:
            total = total + num
            
    else:
        print "{0}".format("This calculator only supports * or +")
                
    return total


def main():
    digits = [5,5,2]
    print calc(digits, "add")
    print calc(digits, "mult")


if __name__ == "__main__":
    main()
