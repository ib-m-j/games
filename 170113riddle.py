import statistics
import PIL
import plotly
import plotly 
plotly.tools.set_credentials_file(username='ib.m.jorgensen', 
                                  api_key='l9HRRRx9SozelyejpQ9V')
import math

if __name__ == '__main__':
    seq = [0]
    
    for i in range(1,100):
        seq.append(statistics.mean(seq[:i]) + 1)

    prev = 0
    cur = 0
    for i,v in enumerate(seq):
        if i >= 2:
            prev = math.log(seq[i-1])
            cur = math.log(seq[i])
        print("{: >4d}: {:.3f}   {:.5f}".format(
            i,cur,cur - prev))


    
