import operator as op
import math 
import functools

def ncr(n, r):
    r = min(r, n-r)
    if r == 0: return 1
    numer = functools.reduce(op.mul, range(n, n-r, -1))
    denom = functools.reduce(op.mul, range(1, r+1))
    return numer//denom

class Distribution:
    def __init__(self, n):
        self.values = [0]*n

    def disp(self, n):
        count = 0
        res = '<'
        total = 0
        for x in self.values:
            count= count + 1
            if x != 0:
                res = res + ' {:6.5f}'.format(x)
                total = total + x
            if count > n:
                break
        res = res + '  : {}>'.format(total)
        return res

    def setValue(self, n, v):
        self.values[n] = v

    def getValue(self, n):
        return self.values[n]

if __name__ == '__main__':
    a = Distribution(4)



    p = 0.6
    q = 1 - p

    distributions = {}
    distributions[0] = Distribution(1)
    distributions[0].setValue(0, 1)
    distributions[1] = Distribution(3)
    distributions[1].setValue(0, q)
    distributions[1].setValue(2, p)
    for n in range(2,10):
        lastd = distributions[n-1]
        distributions[n] = Distribution(2**n + 1)
        d = distributions[n]
        
        res = lastd.getValue(0)
        for i in range(1, 2**(n-2) + 1):
            res = res + lastd.getValue(2*i)*q**(2*i)
        d.setValue(0,res)

        for i in range(1, 2**(n-1) + 1):
            res = 0
            fact = ncr(2*math.ceil(i/2), i)
            for j in range(math.ceil(i/2), 2**(n-2) + 1):
                res = res + lastd.getValue(2*j)*ncr(2*j,i)*p**i*q**(2*j-i)
                
            d.setValue(2*i, res)
 


    for (x,item) in distributions.items():
        print(x, item.disp(12))
        
        
