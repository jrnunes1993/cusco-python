from operator import mod
from pyexpat import model
from z3 import *
from itertools import combinations

def at_most_one(literals):
    c = []
    for pair in combinations(literals,2):
        a, b = pair[0],pair[1]
        c += [Or(Not(a), Not(b))]
    return And(c)

len = 5
#create all the literals
x = [[Bool("x_%i_%i" % (i,j))for j in range (len)] for i in range(len)]

#create solver instance
s = Solver()

#create all the constraints
#at last 5 queens
for i in range(len):
    s.add(Or(x[i]))

#constraints: at most one per row
#at most one queen per column
for i in range(len):
    col = []
    for j in range(len):
        col += [x[j][i]]
    s.add(at_most_one(col))
    s.add(at_most_one(x[i]))

#constraints: at most one quuen per diagonal
for i in range(4):
    diag_1 = []
    diag_2 = []
    diag_3 = []
    diag_4 = []
    for j in range(len-i):
        diag_1 += [x[i+j][j]]
        diag_2 += [x[i+j][4-j]]
        diag_3 += [x[4-(i+j)][j]]
        diag_4 += [x[4-(i+j)][4-j]]
    s.add(at_most_one(diag_1))
    s.add(at_most_one(diag_2))
    s.add(at_most_one(diag_3))
    s.add(at_most_one(diag_4))

print(s.check())
m = s.model()

for i in range(len):
    line = ""
    for j in range(len):
        if m.evaluate(x[i][j]):
            line+= "x "
        else:
            line += ". "
    print(line)