""" Check if a number is prime """

import math


def isPrime(n):
    if n > 1:
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        for x in range(3, int(math.sqrt(n) + 1), 2):
            if n % x == 0:
                return False
        return True
    return False
