#!/usr/bin/python3

from pyrology import pyrology


def pippo():
    print('PIPPO')

if __name__ == '__main__':
    print('===============================================================')

    ns = pyrology.Simplespace()
    ns.a.b.c = 1234567890
    print(ns.a.b.c)

    print('===============================================================')


