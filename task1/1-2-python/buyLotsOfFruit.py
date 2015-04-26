# Theo Pijkeren s4481046
# Mattijn Kreuzen s4446402
## buyLotsOfFruit.py
# -----------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
To run this script, type

  python buyLotsOfFruit.py
  
Once you have correctly implemented the buyLotsOfFruit function,
the script should produce the output:

Cost of [('apples', 2.0), ('pears', 3.0), ('limes', 4.0)] is 12.25
"""
import sys
import re

fruitPrices = {'apples': 2.00, 'oranges': 1.50, 'pears': 1.75,
               'limes': 0.75, 'strawberries': 1.00}

# please check buyLotsOfFruit2
def buyLotsOfFruit(orderList):
    """
        orderList: List of (fruit, numPounds) tuples
            
    Returns cost of order
    """
    #return buyLotsOfFruit2(orderList)
    totalCost = 0.0
    for item in orderList:
        if item[0] in fruitPrices:
            totalCost += fruitPrices[item[0]] * item[1]  # adds the price of an item to totalCost
        else:
            return None  # return None if the item is not in fruitPrices
    return totalCost     # return the total price if all the items are in fruitPrices


# Does the same as buyLotsOfFruit. but is shorter.
def buyLotsOfFruit2(orderList):
    """
        orderList: List of (fruit, numPounds) tuples

    Returns cost of order
    """
    list = [fruitPrices[item[0]] * item[1] if item[0] in fruitPrices else None for item in orderList] # list contains the total price of every item in orderlist. None if the item isn't in fruitPrices.
    if None in list:
        return None         # return None if the item is not in fruitPrices
    else:
        return sum(list)        # return the total price if all the items are in fruitPrices

# Main Method    
if __name__ == '__main__':
    "This code runs when you invoke the script from the command line"
    orderList = [('apples', 2.0), ('pears', 3.0), ('limes', 4.0),]
    print('Cost of', orderList, 'is', buyLotsOfFruit(orderList))
    if len(sys.argv) == 1:
        args = input("Enter any command line arguments?")
    if args != '':
        sys.argv.extend(re.split(r' *', args))
    print(str(len(sys.argv)) + ': ')
    print(sys.argv)
