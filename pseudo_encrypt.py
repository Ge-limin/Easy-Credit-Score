# https://wiki.postgresql.org/wiki/Pseudo_encrypt
import numpy as np

def pseudo_encrypt(value):
    value = int(value)
    l1 = (value >> 16) & 0xffff
    r1 = value & 0xffff
    i = 0
    while i < 3:
        l2 = r1
        r2 = l1 ^ int(round((((1366 * r1 + 150889) % 714025) / 714025.0) * 32767))
        l1 = l2
        r1 = r2
        i = i + 1
    return ((r1 << 16) + l1)