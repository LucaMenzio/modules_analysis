import os
import matplotlib.pyplot as plt
import numpy as np

filespath = "/home/luca/Desktop/Analisi/modules/Data_measurements/Batch2"
px = []
py = []
pz = []

n_points_per_file = 8
n_files = 0

for filename in os.listdir(filespath):
    if os.path.isfile(os.path.join(filespath, filename)):
        print(filename)
        n_files = n_files+1
        with open(os.path.join(filespath, filename)) as file:
            count = 0  # Reset the count for each file
            for line in file:
                if "point" in line:
                    line = line[45:]  # Remove characters before the coordinates
                    coordinates = line.split()[:3]  # Split by spaces and take the first three values
                    if len(coordinates) == 3:
                        x, y, z = map(float, coordinates)
                        px.append(x)
                        py.append(y)
                        pz.append(y)

plt.scatter(px, py, label='Scatter Plot', color='blue', marker='o')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.show()

distances_x = []
distances_y = []

for i in range(int(len(px)/n_points_per_file)):
    distances_x.append(-1*px[i*n_points_per_file]+px[i*n_points_per_file+1]-2.)
    distances_x.append(px[i*n_points_per_file+4]-px[i*n_points_per_file+5]-2.)
    distances_y.append(-1*py[i*n_points_per_file+2]+py[i*n_points_per_file+3]-2.)
    distances_y.append(py[i*n_points_per_file+6]-py[i*n_points_per_file+7]-2.)

 
# Create histograms for X and Y distances
plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.hist(distances_x, bins=20, color='blue', edgecolor='black')
plt.xlabel('Distance along X-axis')
plt.ylabel('Frequency')
plt.title('Histogram of X Distances')

plt.subplot(1, 2, 2)
plt.hist(distances_y, bins=20, color='green', edgecolor='black')
plt.xlabel('Distance along Y-axis')
plt.ylabel('Frequency')
plt.title('Histogram of Y Distances')

plt.tight_layout()
plt.show()


