def power_of(number, power):

    if number % power == 0:
        x = float(number)
        while True:
            #print x
            x = x / float(power)
            if x == 1.0:
                print "{0} is a power of {1}".format(number, power)
                return 1
            
            elif x < 1.0:
                return 0

                
for num in range(0, 1024):
    power_of(num, 2)
