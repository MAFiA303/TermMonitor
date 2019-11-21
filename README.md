# TermMonitor
Monitor laptop from terminal

![alt text](https://external-preview.redd.it/DrP4Frol6RhowD6omd3G47iuERRioBvt1fAqxgY5tFc.png?width=640&crop=smart&format=pjpg&auto=webp&s=b14b4f9e2a9f2faabf2024d391472708ecbc7797)

Using a mixure of bash and python, you can observe laptop's temperature from the terminal.
First lets make sure you go the dependencies:
* Python pipeline

```bash
sudo apt install python3-pip
```

* termpltlib to plot in ascii format into the terminal

```bash
pip3 install termplotlib
pip3 install numpy
```


# Background
to know the temperature in linux, you can use `sensors` in terminal to view it.
```
acpitz-virtual-0
Adapter: Virtual device
temp1:        +49.8°C  (crit = +104.0°C)
temp2:        +49.8°C  (crit = +104.0°C)

coretemp-isa-0000
Adapter: ISA adapter
Package id 0:  +52.0°C  (high = +87.0°C, crit = +105.0°C)
Core 0:        +52.0°C  (high = +87.0°C, crit = +105.0°C)
Core 1:        +49.0°C  (high = +87.0°C, crit = +105.0°C)
```

I only need `Core 0:` so I wil filter this line out using `grep`. I also used `regular expression` to extract the number out and convert to `int` using python.

# Python Code
Here i will explain what I used and why to help you understand the process.

To run `bash`commands from `python`, i used `subprocess`.
```python
import subprocess
bashCommand = '''t=$(eval "sensors | grep 'Core 0'")
echo "$t"'''
process = subprocess.check_output(bashCommand, shell=True)
```

convert from byte format to string:

```python
str = process.decode("utf-8")
```

Use Regular Expression in Python to extract the temperature int:
```python
import re
y = re.sub("^(.*?\\+)", "", str)
y = re.sub(".0°C.*", "", y) 
```
To plot over time, save the readings into a local file. I cannot save it in python, because the way the program runs, is by running the code every second from the terminal. So save it outside:
```python
fpath = "Downloads/scripts/data-plot.dat" #file location
f = open(fpath, "a")
f.write(y)
f.close()
```

Optional: in order to keep the file from becoming huge, I decided to delete values when they reach 600 inputs:
```python
with open(fpath) as f:
    y = f.read().splitlines()
if len(y) > 600:
    open(fpath, 'w').close()
```

I want to plot only the past 3 minutes. Since the code refreshes every second, so that 3x60 points:
```python
y = y[-180:]
for i in range(0, len(y)): 
    y[i] = int(y[i]) 
```
# Plotting with termplotlib
it takes x,y as input. so i created `x` from 0 to 180 array
```python
import termplotlib as tpl
import numpy as np
x = np.arange(len(y))
fig = tpl.figure()
fig.plot(x,y, width=60, height=20)
fig.show()
```

The has little more things, you can download and run the code if you dont want to DIY.

# Terminal
To run from terminal, I will use `watch`. I will also add `-c` to the python code to run from console:
```terminal
watch -n1 --color python3 Downloads/scripts/pyplt.py -c
```

There is big room for optimization and adding more colors and features. waht what I did in my free time yesterday.






