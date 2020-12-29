import os
import math
import csv


def gen_curve(filename: str):
    with open(filename, 'w', newline='') as fs:
        writer = csv.writer(fs)
        for i in range(630):
            x = i / 100.0
            writer.writerow([x, math.cos(x), math.sin(x)])


def gen_state(filename: str):
    with open(filename, 'w', newline='') as fs:
        writer = csv.writer(fs)
        for i in range(30):
            writer.writerow([i, i % 2, (i // 10) % 2, i // 5])


base = os.path.basename(os.path.dirname(os.path.realpath(__file__)))
gen_curve(os.path.join(base, 'cos_sin.csv'))
gen_state(os.path.join(base, 'states.csv'))
