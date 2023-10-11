class PriceProcessor:
    def __init__(self, prices):
        self.prices = prices

    def process(self):
        for price in self.prices:
            print("Time: ", price.time)
            print("Price: {0} c/kWh".format(price.price))


