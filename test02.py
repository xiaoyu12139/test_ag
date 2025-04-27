l = [1,2,3,4,5]
print(l)
print(*l)
print(l[0],l[1])
print(l[-1])
print(l[-2])
print(l[1:])

from base import *


class Solution(object):
    @ag_test(cases=[(1,2)],expected=[4])
    def solve1(self, a, b):
        return a + b

    # @pytest.mark.parametrize("a,b", [(1,2)])
    # def solve2(self, a, b):
    #     return a + b

    # def demo(self):
    #     return True