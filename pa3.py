# -*- coding: utf-8 -*-
"""
Created on Thu Feb 29 13:08:38 2024

@author: LMOakes
"""

import numpy as np

def poly_solve(poly, x):
    return round(np.polyval(poly, x), 3)

def poly_deriv_solve(poly, x):
    deriv = np.polyder(poly)
    return round(np.polyval(deriv, x), 3)

def newtons_method(poly, x):
    print("----------------")
    x_val = poly_solve(poly, x)
    deriv_val = poly_deriv_solve(poly, x)
    new_x = round(x - (x_val / deriv_val), 3)
    print(x)
    print(new_x)
    print()
    if new_x == x:
        return
    newtons_method(poly, new_x)
    
def roots(poly):
    roots = np.roots(poly)
    print("Polynomial Roots:")
    print(roots)
    
def part1():
    print()
    print("Part 1: numpy Familiarization")
    print()
    print("Polynomail Function: ")
    poly_func = np.poly1d([2, 3, 1])
    print(np.poly1d(poly_func))
    print()
    print("At x = 2:")
    print(poly_solve(poly_func, 2))
    print()
    print("Polynomail Function: ")
    deriv_func = np.poly1d([1, 0, 1])
    print(np.poly1d(deriv_func))
    print()
    print("At x = 1 for the derivative: ")
    print(poly_deriv_solve(deriv_func, 1))
    
def part2():
    print()
    print("Part 2: Newtons Method Automation")
    print()
    print("Please enter an A, B, and C value to create polynomial")
    print("(Must be integers !!)")
    print()
    print("Polynomial: Ax^2 + Bx + C")
    polyA = int(input("A: "))
    polyB = int(input("B: "))
    polyC = int(input("C: "))
    print()
    print("Your polynomial:")
    poly = np.poly1d([polyA, polyB, polyC])
    print(np.poly1d(poly))
    x1 = int(input("Enter an X1 value: "))
    print()
    newtons_method(poly, x1)
    roots(poly)
    
def main():
    part = int(input("Test Part 1 or Part 2? (1/2): "))
    
    if part == 1:
        part1()
    elif part == 2:
        part2()

main()