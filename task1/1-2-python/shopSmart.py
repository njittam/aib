# Theo Pijkeren s4481046
# Mattijn Kreuzen s4446402

# shopSmart.py
# ------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
Here's the intended output of this script, once you fill it in:

Welcome to shop1 fruit shop
Welcome to shop2 fruit shop
For orders:  [('apples', 1.0), ('oranges', 3.0)] best shop is shop1
For orders:  [('apples', 3.0)] best shop is shop2
"""

import shop
# please check shopSmart2
def shopSmart(orderList, fruitShops):
    """
        orderList: List of (fruit, numPound) tuples
        fruitShops: List of FruitShops
    """
    #return shopSmart2(orderList, fruitShops)
    cheapest_price = fruitShops[0].getPriceOfOrder(orderList)  # Cheapest price holds the current lowest price
    for shop in fruitShops:
        price = shop.getPriceOfOrder(orderList)  # price is the current price to be checked
        if price <= cheapest_price:  # if price is lower remember the shop and the according price
            cheapest_price = price
            cheapest_shop = shop
    return cheapest_shop

# Does the same as smartShop. but is shorter.
def shopSmart2(orderList, fruitShops):
    """
        orderList: List of (fruit, numPound) tuples
        fruitShops: List of FruitShops
    """
    priceList = [shop.getPriceOfOrder(orderList) for shop in fruitShops] # a list with al the total prices of shops in fruitShops
    return [shop for shop in fruitShops if shop.getPriceOfOrder(orderList) == min(priceList)][0] # a list of all the shops with the lowest price and return the first

if __name__ == '__main__':
  "This code runs when you invoke the script from the command line"
  orders = [('apples',1.0), ('oranges',3.0)]
  dir1 = {'apples': 2.0, 'oranges':1.0}
  shop1 =  shop.FruitShop('shop1',dir1)
  dir2 = {'apples': 1.0, 'oranges': 5.0}
  shop2 = shop.FruitShop('shop2',dir2)
  shops = [shop1, shop2]
  print("For orders ", orders, ", the best shop is", shopSmart(orders, shops).getName())
  orders = [('apples',3.0)]
  print("For orders: ", orders, ", the best shop is", shopSmart(orders, shops).getName())
