import termplotlib as tpl
import numpy as np
import time as T
import subprocess
import re

bashCommand = '''t=$(eval "sensors | grep 'Core 0'")
echo "$t"'''

process = subprocess.check_output(bashCommand, shell=True)
str = process.decode("utf-8")
y = re.sub("^(.*?\\+)", "", str)
y = re.sub(".0°C.*", "", y) 

fpath = "Downloads/scripts/data-plot.dat"
f = open(fpath, "a")
f.write(y)
f.close()

with open(fpath) as f:
    y = f.read().splitlines()
if len(y) > 600:
    open(fpath, 'w').close()

y = y[-180:]
for i in range(0, len(y)): 
    y[i] = int(y[i]) 

x = np.arange(len(y))


fig = tpl.figure()
fig.plot(x,y, width=60, height=20)
print(y[-1],'°C')
print(T.ctime())
fig.show()



# plotting horizontally
#ek=4
#for i in range(-30,0,1):
#    print(y[i],int(ek*(y[i]-min(y)+1/ek))*'*')



