#!/bin/python3

def odd_pair():
    number = int(input().strip())
    if number % 2 != 0 or (number >= 6 and number <= 20):
        print("Weird")
    else:
        print("Not Weird")

odd_pair()
