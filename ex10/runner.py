import matplotlib.pyplot as plt
import os
import subprocess

def createNamefileString(alpha):
    return '''! namelist for numerical simulation of the predator prey model
&model_parameters
alpha = ''' + alpha + '''
beta = 10.0
gamma = 1.0
delta = 3.0
lambda = 1.0
mu = 2.0
/
&spatial_parameters
kappaInverted = 1000
bigN = 1
/
&time_parameters
tZero = 0.0
T = 20
dt = 0.01
/
'''

intrStart = 4.5
intrEnd = 8
runs = 200
outFileText = []
outputVals = []

def getAlpha(i):
    return intrStart * (1 - (i / (runs - 1))) + intrEnd * (i / (runs - 1))

# ensemble runs 
for i in range(runs):
    with open('predatorprey.nml', 'w') as filetowrite:
        filetowrite.write(createNamefileString(str(getAlpha(i))))

    p = subprocess.Popen('predator-prey.exe')
    p.wait()

    with open('outfile.txt', 'r') as myfile:
        outFileText.append(myfile.read())

    split = outFileText[i].split()
    boxes = split.__len__()
    outputVals.append(list(map(lambda x: float(x), split)))

# plot
print(boxes)
plt.plot(list(map(lambda i: getAlpha(i), range(runs))), list(map(lambda x: x[0], outputVals)))
plt.title("Ensemble run")
plt.xlabel("Alpha")
plt.ylabel("x(T)")
plt.ticklabel_format(useOffset=False)
plt.show()
