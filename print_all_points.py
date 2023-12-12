import os
import matplotlib.pyplot as plt
import numpy as np
from array import array
import ROOT

#filespath = "/home/luca/Desktop/Analisi/modules/Data_measurements/Batch2/Sides"
filespath = "/home/luca/Desktop/Analisi/modules/Data_measurements/Batch3/"
max_files = 1

px_temp, py_temp, pz_temp = [], [], []
filenames = []
px, py, pz = [[]], [[]], [[]]

n_points_per_file = 24
n_files = 0

for k, filename in enumerate(os.listdir(filespath)):
    if k > max_files:
        break
    if "cura" not in filename:
        continue 
    if os.path.isfile(os.path.join(filespath, filename)):
        #print(filename)
        filenames.append(filename)
        n_files = n_files+1
        count = 0  # Reset the count for each file
        with open(os.path.join(filespath, filename)) as file:
            for line in file:
                if count == 6:
                    break
                if "point" in line:
                    line = line[45:]  # Remove characters before the coordinates
                    coordinates = line.split()[:3]  # Split by spaces and take the first three values
                    if len(coordinates) == 3:
                        x, y, z = map(float, coordinates)
                        px_temp.append(x)
                        py_temp.append(y)
                        pz_temp.append(z)
                        count = count+1

plt.scatter(px_temp, py_temp, label='Scatter Plot', color='blue', marker='o')
plt.xlabel('X-axis [mm]')
plt.ylabel('Y-axis [mm]')
plt.show()
