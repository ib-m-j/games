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
    cure = 0
    for i,v in enumerate(seq):
        if i >= 2:
            prev = math.exp(seq[i-1])
            cure = math.exp(seq[i])
            cur = seq[i]
        print("{: >4d}: {:.3f} {:.3f}   {:.10f}  {:.4f}".format(
            i,cur,cure, cure - prev, math.log(i+1)+math.log(1.7810)))


    
