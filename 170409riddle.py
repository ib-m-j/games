import itertools
import statistics

register = []

class Strategy:
    def __init__(self):
        self.register = []
        self.details = []

    def setValue(self, x):
        self.register.append((x[0]*10+x[1])*(x[2]*10+x[3]))
        self.details.append(x)

    def getMean(self):
        return statistics.mean(self.register)


class CheatingBest(Strategy):
    def setValue(self, x):
        y = list(x)
        y.sort()
        self.register.append((y[0]*10+y[2])*(y[1]*10+y[3]))
        self.details.append((y, y[0]*10+y[2], y[1]*10+y[3]))

class AdvancedBest(Strategy):
    def setValue(self, x):
        decades = {}
        dindexes = [0,1]
        units = {}
        uindexes = [0,1]
        for n in x:
            #print(n, uindexes, dindexes)
            if n < 5:
                if len(dindexes) > 0:
                    if len(dindexes) == 1 or len(uindexes) == 2:
                        insertat = dindexes[0]
                    elif len(uindexes) == 1:
                        if n < 3:
                            if units[0] < 8: 
        #if we get here the units must befilled in index 0
                                insertat = 0
                            else:
                                insertat = 1
                        else:
                            if units[0] < 8:
                                insertat = 1
                            else:
                                insertat = 0
                    else: #len(uindexes == 0
                        if n < 3:
                            if units[0] < units[1]:
                                insertat = 0
                            else:
                                insertat = 1
                        else:
                            if units[0] < units[1]:
                                insertat = 1
                            else:
                                insertat = 0
                            
                    decades[insertat] = n
                    dindexes.remove(insertat)
                else:
                    if len(uindexes) == 2:
                        if decades[0] < decades[1]:
                            insertat = 0
                        else:
                            insertat = 1
                    else: #no choice
                        insertat = uindexes[0]

                    units[insertat] = n
                    uindexes.remove(insertat)
            else:
                if len(uindexes) > 0:
                    if len(uindexes) == 1 or len(dindexes) == 2:
                        insertat = uindexes[0]
                    elif len(dindexes) == 1:
                        if n < 8:
                            if decades[0] < 3:
        #if we get here the decades must befilled in index 0
                                insertat = 0
                            else:
                                insertat = 1
                        else:
                            if decades[0] < 3:
                                insertat = 1
                            else:
                                insertat = 0
                    else: #len(dindexes) == 0
                        if n < 8:
                            if decades[0] < decades[1]:
                                insertat = 0
                            else:
                                insertat = 1
                        else:
                            if decades[0] < decades[1]:
                                insertat = 1
                            else:
                                insertat = 0
                            
                    units[insertat] = n
                    uindexes.remove(insertat)
                else:
                    if len(dindexes) == 2:
                        if units[0] < units[1]:
                            insertat = 0
                        else:
                            insertat = 1
                    else: #no choice
                        insertat = dindexes[0]

                    decades[insertat] = n
                    dindexes.remove(insertat)

        self.register.append(
            (decades[0]*10+units[0])*(decades[1]*10+units[1]))
        self.details.append((x,decades[0]*10+units[0],decades[1]*10+units[1])) 
                

class SimpleBest(Strategy):
    def setValue(self, x):
        decades = {}
        units = {}
        for n in x:
            if n < 5:
                if len(decades) < 2:
                    if len(decades) == 0:
                        decades[0] = n
                    else:
                        decades[1] = n
                else:
                    if len(units) == 0:
                        units[0] = n
                    else:
                        units[1] = n
            else:
                if len(units) < 2:
                    if len(units) == 0:
                        units[0] = n
                    else:
                        units[1] = n
                else:
                    if len(decades) == 0:
                        decades[0] = n
                    else:
                        decades[1] = n

        self.register.append(
            (decades[0]*10+units[0])*(decades[1]*10+units[1]))
        self.details.append((x,decades[0]*10+units[0],decades[1]*10+units[1])) 
                

        


if __name__ == '__main__':
    count = 0
    strategy = AdvancedBest()
    #strategy = SimpleBest()
    #strategy = CheatingBest()
    for x in itertools.permutations(range(10), 4):
        count = count + 1
        strategy.setValue(x)

        #if count == 100:
        #    break

    for (n,(a,b)) in enumerate(zip(strategy.details, strategy.register)):
        if n%1000 == 0:
            print(n,a,b)
    print(strategy.getMean())
