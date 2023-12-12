import os
import matplotlib.pyplot as plt

filespath = "/home/luca/Desktop/Analisi/modules/Data_first_measurements"
filesnames = []
px = []
py = []
pz = []

n_points_per_file = 8

for path in os.listdir(filespath):
    if os.path.isfile(os.path.join(filespath, path)):
        filesnames.append(path)

#for filename in filesnames:
filename = filespath+"/"+filesnames[0]
print(filename)
where_to_cut_string = []
with open(filename) as file:
    for line in file.readlines():
        string = ""
        count = 0
        if "point" in line:
            for i,el in enumerate(line):
                if " " not in el and i>45:
                    where_to_cut_string.append(i)
                    break
            string=line[where_to_cut_string[count-1]:len(line)]
            count=count+1
            index = []
            for i in range(len(string)-1):
                if i > 1 and " " in string[i] and not " " in string[i-1]:
                    index.append(i)
                    if len(index) > 2:
                        break
            for i,ind in enumerate(index):
                if i == 0:
                    px.append(float(string[0:ind]))
                if i == 1:
                    py.append(float(string[index[i-1]:ind]))
                if i == 2:
                    pz.append(float(string[index[i-1]:ind]))  

plt.scatter(px, py, label='Scatter Plot', color='blue', marker='o')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
#plt.show()


'''
distances_x = []
distances_y = []

i = 0
distances_x.append(px[i*n_points_per_file]-px[i*n_points_per_file+1])
distances_x.append(px[i*n_points_per_file+4]-px[i*n_points_per_file+5])
distances_y.append(py[i*n_points_per_file+2]-py[i*n_points_per_file+3])
distances_y.append(py[i*n_points_per_file+6]-py[i*n_points_per_file+7])
'''
