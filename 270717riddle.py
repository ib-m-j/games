import math
import sys

allfactors = {}

def primes(n):
    res = [x for x in range(1,n+1)]
    count = 1
    p = res[count]
    while p < math.sqrt(n):
        for i in range(2, math.floor(n/p) + 1):
            if i*p in res:
                res.remove(i*p)
        count = count + 1
        p = res[count]
        
    return res


def getFactors(n):
    if n in allfactors:
        return allfactors[n]
    res = []
    
    end = math.sqrt(n)
    for i in range(1,math.ceil(end)):
        if n % i == 0:
            res.extend([i, int(n/i)])

    if (math.floor(end))**2 == n:
        res.append(math.floor(end))

    res.sort()
    return res


class FactorSequence:
    def __init__(self, n, distribution, start = []):
        self.limit = n
        self.start = start
        self.length = len(self.start)
        self.best = self.start
        self.variants = None
        self.distribution = distribution

    def legalNexts(self):
        if len(self.start) == 0:
            beginWith = 1
        else:
            beginWith = self.start[-1]

        res = [
            i*beginWith for i in range(2,self.limit // beginWith + 1)]
        res.extend(getFactors(beginWith))

        res = list(set(res) - set(self.start))
        return res
        
    def expand(self):
        for x in self.legalNexts():
            #if (self.length == 0):
            #    print("level 0", x)
            child = FactorSequence(self.limit, self.distribution, self.start + [x])
            child.expand()
            
            if len(child.best) > len(self.best):
                self.best = child.best
                self.variants = [child.best]
            elif len(child.best) == len(self.best):
                    self.variants.append(child.best)

            if len(child.best) in self.distribution:
                self.distribution[len(child.best)].append(
                    (self.start, child.best[-1]))
            else:
                self.distribution[len(child.best)] = [
                    (self.start, child.best[-1])]
            

            #if child.length > self.length:
            #    self.best = child.best
            #    self.length = child.length
            #elif child.length == self.length:
            #    if self.best:
            #        self.best = self.best.append(child.best)
            #    else:
            #        self.best = child.best
        
        return(self)
        

class FactorFragments(FactorSequence):
    def __init__(self, n, space, log, start = []):
        self.spaces = (set(space[0]), set(space[1]))
        self.log = log
        FactorSequence.__init__(self, n, start)
    

    def legalNexts(self):
        res1 = set(FactorSequence.legalNexts(self))
        #print(res1, self.start, self.space, res1 & self.space)
        res = list(res1 & self.spaces[0])
        res.sort()
        return res
        
    def expand(self, level ):
        #print("bb", level, self.legalNexts(), self.start)
        #if len(self.best) == len(self.spaces[0]):
        #    print(
        #        self.length, self.best[0], self.best[-1], 
        #        "missing ", self.spaces[1] - set(self.best))
        for x in self.legalNexts():
            #if level == 0:
            #    newSpaces = (self.spaces[1], self.spaces[1])
            #else:
            #    newSpaces = self.spaces

            child = FactorFragments(
                self.limit, self.spaces, self.log, self.start + [x])
            #print("aa",x, child.length, child.start, self.spaces)
            child.expand(level + 1)
            if level == 0:
                if child.length >= self.length:
                    print(
                        child.length, child.best[0], child.best[-1], 
                        "missing ", self.spaces[1] - set(child.best))
                    self.log.write(
                        "{}, {}, {}, {}, {}\n".format(
                            child.length, child.best[0], child.best[-1],
                            child.best, self.spaces[1] - set(child.best)))
            

            if child.length > self.length:
                self.best = child.best
                self.length = child.length
        
            

        return(self)



def basicTest():
    fact = getFactors(24)
    print(fact)

    initial = FactorSequence(15, [1,3, 6])
    print( initial.legalNexts())

    print(FactorSequence(7,[]).legalNexts())


def findFactorsequence(n):
    begin = FactorSequence(n ,[])
    begin.expand()
    print(begin.start, begin.best)


def findPrimes(n):
    global primes
    primes = primes(n)
    #print(res)

def findRestrictedSpace(n, x):
    largerPrimes = []
    for j in primes:
        if j > x:
            largerPrimes.append(j)

    space1 = []
    space2 = []
    for i in range(1, math.floor(n/x) + 1):
        space1.append(i*x)
        remove = False
        for lp in largerPrimes:
            if i*x % lp == 0:
                remove= True
                break
        if not remove:
            space2.append(i*x)

    return (space2, space2)

def findFactorFragments(n):
    findPrimes(n)
    space = []
    #for i in range(1, math.floor(n/fragmentId) + 1):
    #    print(i, i in primes)
    #    if (i < fragmentId) or not (i in primes):
    #        space.append(i*fragmentId)
    #print(space)
    #space = [i*fragmentId for i in range(1, math.floor(n/fragmentId) + 1)]

    print(primes)
    f = open('fragments.txt','w')
    for fragmentId in primes[1:]:
        print(fragmentId)
        spaces = findRestrictedSpace(n, fragmentId)
        print(spaces[0]) 
        f.write("Starting: {} {}\n".format(fragmentId, space))
        begin = FactorFragments(n, spaces, f)
        begin.expand(0)
        print("result is", begin.start, begin.best)
    f.close()

def findCoreFragments(n):
    space = []
    for maxValue in range(6,n):
        distribution = {}
        print("\nStarting: {}".format(maxValue))
        #    begin = FactorSequence(maxValue, [])
        #    begin.expand()
        #    print("result for start {} is {}".format(entry, begin.best))
        for entry in range(1, maxValue + 1):
            begin = FactorSequence(maxValue, distribution, [entry])
            begin.expand()
            #print(
            #    "result for start {} is {}, {}".format(
            #        entry, begin.best, begin.variants))
            
        for (a,b) in distribution.items():
            print(a,b)

def testRestrictedSpace():
    findPrimes(100)
    print(findRestrictedSpace(100, 7))


if __name__ == '__main__':
    #x = findFactorFragments(100)
    x = findCoreFragments(7)
    
