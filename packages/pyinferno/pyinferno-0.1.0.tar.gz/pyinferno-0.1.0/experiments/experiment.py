import pstats
import time
from pyinferno import InfernoProfiler, lines_from_stats

def factorial(i):
    result = 0
    while i > 0:
        result+=i*i-1
        i-=1

class TestClass:
    def __init__(self):
        ...
    def slow_method(self):
        time.sleep(1)

with InfernoProfiler("experiments/method.svg") as p:
    # import dis
    # for i in range(1000):
    #     dis.dis(dis.dis)

    # factorial(100000000)
    c = TestClass()
    c.slow_method()
profiler = p.profiler
stats = pstats.Stats(profiler)
with InfernoProfiler("experiments/lines.svg"):
    lines = lines_from_stats(stats.stats)
print(lines)
