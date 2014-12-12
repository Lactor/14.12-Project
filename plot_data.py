import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

import sys

file_name = sys.argv[1]

data_file = open(file_name, "r")

cols = sys.argv[2]

l =10
k =0

data_gd = []
data_bd = []

for line in data_file:
    
    values = line.split()
    if values[0] == 'None':
        break
    for i in range(len(values)):
        #print values[i]
        if values[i] == 'True' or values[i] == 'False':
            continue
        #print values[i][0].isdigit()
        if not values[i][0].isdigit():
            values[i] = values[i][1:]
        if not values[i][-1].isdigit():
            values[i] = values[i][:-1]
        
    #print values
    for i in range(len(values) - 1):
        values[i] = float(values[i])
    #print cols
    temp = []
    stop = False
    for i in range(len(values) - 1):
        if cols[i] == '0' and not values[i] == 0.0:
            #print "STOP", i
            stop = True
            break
        elif cols[i] == '1':
            temp.append(float(values[i]))
    
    if not stop:
        if values[-1] == 'True':
            #print "Ap gd"
            data_gd.append(temp)
        else:
            #print temp
            data_bd.append(temp)


#print np.size(data_gd)
data_gd = np.array(data_gd)
data_bd = np.array(data_bd)
#print data_bd

#print np.shape(data_gd)



fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(data_gd[:,0], data_gd[:,1], data_gd[:,2], marker = '+', color = 'green', s = np.zeros(np.size(data_gd[:,0]))+50)

ax.scatter(data_bd[:,0], data_bd[:,1], data_bd[:,2], marker = 'o', color = 'red', s = np.zeros(np.size(data_bd[:,0])) +50)
 

ax.yaxis.set_label_text("y")
 
plt.show()           


