import math
import numpy

limit = 1000
values = numpy.full((1, 1000), 0)[0]

for i in range(100000):
    v = math.ceil(numpy.random.lognormal()**2)
    if v < limit:
        values[v] = values[v] + 1

for i in range(limit):
    print(str(i) + "\t" + str(values[i]))
