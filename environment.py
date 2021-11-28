import numpy as np
##agent: coins available method (coin, amount)


class Uni(object):
    def __init__(self, x_init, y_init, x_history, y_history):
        self.x = x_init
        self.y = y_init
        self.x_history = x_history
        self.y_history = y_history
        self.current_state = 0
        self.k = x_init * y_init
        self.fee = 0

    def get_liquidity(self):
        return np.sqrt(self.x * self.y)

    def provide_liquidity(self, x : float, y : float):
        assert(x / y == self.x / self.y), 'you can not provide this'

        self.x += x
        self.y += y

    #how much will we get for delta
    def slip_price(self, delta : float):
        if delta >= 0:
            self.y -= self.y - (self.x * self.y) / (self.x + delta * (1 - self.fee))
            return self.y - (self.x * self.y) / (self.x + delta * (1 - self.fee))

        elif delta < 0:
            delta = abs(delta)
            self.x -= self.x - (self.x * self.y) / ( self.y + (1 - self.fee) * delta)
            return self.x - (self.x * self.y) / ( self.y + (1 - self.fee) * delta)

    def swap(self, amount : float):
        #swap AMOUNT of X to Y, so we need to calculate slip price of Y
        if amount > 0 :
            self.x += amount
        else:
            amount = abs(amount)
            self.y += amount
        return self.slip_price(amount)

    def update_state(self):
        self.current_state += 1

    def x2y(self):
        return self.x / (self.y * (1 - self.fee))

    def y2x(self):
        return self.y / (self.x * (1 - self.fee))

