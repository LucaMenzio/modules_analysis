import os
import matplotlib.pyplot as plt
import numpy as np
from array import array
import ROOT


def graph_and_fit(x_first, y_first, x_second, y_second):
    graph_first = ROOT.TGraph(len(x_first),x_first,y_first)
    fit_function_first = ROOT.TF1("pol1_first","[0]+x*[1]")
    graph_first.Fit("pol1_first","Q0")
    graph_second = ROOT.TGraph(len(x_second),x_second,y_second)
    fit_function_second = ROOT.TF1("pol1_second","[0]+x*[1]")
    fit_function_second.FixParameter(1,fit_function_first.GetParameter(1))
    graph_second.Fit("pol1_second","Q0")
    return np.abs(fit_function_first.GetParameter(0) - fit_function_second.GetParameter(0))/np.sqrt(fit_function_first.GetParameter(1)*fit_function_first.GetParameter(1)+1) #distance between two parallel lines

filespath = "/home/luca/Desktop/Analisi/modules/Data_measurements/Batch3/"
px_temp, py_temp, pz_temp = [], [], []
filenames = []
px, py, pz = [[]], [[]], [[]]

selection_string = "precura"
n_points_per_file = 24
n_files = 1

for k, filename in enumerate(os.listdir(filespath)):
    px_temp, py_temp, pz_temp = [], [], []
    if os.path.isfile(os.path.join(filespath, filename)):
        #print(filename)
        filenames.append(filename)
        n_files = n_files+1
        with open(os.path.join(filespath, filename)) as file:
            count = 0  # Reset the count for each file
            for line in file:
                if "point" in line:
                    line = line[45:]  # Remove characters before the coordinates
                    coordinates = line.split()[:3]  # Split by spaces and take the first three values
                    if len(coordinates) == 3:
                        x, y, z = map(float, coordinates)
                        px_temp.append(x)
                        py_temp.append(y)
                        pz_temp.append(z)
        if len(px_temp) == n_points_per_file:
            px.append(px_temp)
            py.append(py_temp)
            pz.append(pz_temp)

#some fitting and extraction of the distances
distance_left, distance_right, distance_top, distance_bottom = [], [], [], []
n_bins = 20
min_bin = .1
max_bin = .4
hist_total  = ROOT.TH1F("total distances between sides","total distances between sides", n_bins, min_bin, max_bin)
hist_left   = ROOT.TH1F("distances between sides on the left","distances between sides on the left", n_bins, min_bin, max_bin)
hist_right  = ROOT.TH1F("distances between sides on the right","distances between sides on the right", n_bins, min_bin, max_bin)
hist_top    = ROOT.TH1F("distances between sides on the top","distances between sides on the top", n_bins, min_bin, max_bin)
hist_bottom = ROOT.TH1F("distances between sides on the bottom","distances between sides on the bottom", n_bins, min_bin, max_bin)

for j in range(n_files):
    if j==1:
        break
    if selection_string not in filenames[j]:
        continue
    print(filenames[j],j)
    #first distance, bottom
    x_bottom_first, y_bottom_first = array('d'), array('d')
    x_bottom_second, y_bottom_second = array('d'), array('d')
    
    for i in range(len(px[j+1])):
        if px[j+1][i] < 0 and py[j+1][i] < -5: 
            if py[j+1][i] < -9: #excluding the points in the top left    
                x_bottom_first.append(1.*px[j+1][i])
            y_bottom_first.append(1.*py[j+1][i])
        if px[j+1][i] > -0. and py[j+1][i] < -5:
            x_bottom_second.append(px[j+1][i])
            y_bottom_second.append(py[j+1][i])
    distance_bottom.append(graph_and_fit(x_first=x_bottom_first,y_first=y_bottom_first,x_second=x_bottom_second,y_second=y_bottom_second))
    hist_bottom.Fill(distance_bottom[j])
    hist_total.Fill(distance_bottom[j])
    
    #second distance, right
    x_right_first, y_right_first = array('d'), array('d')
    x_right_second, y_right_second = array('d'), array('d')    
    for i in range(len(px[j+1])):
        if px[j+1][i] > 5.  and py[j+1][i] < 0.: #excluding the points in the top left    (px[i] <0.1 and py[i > -8])
            x_right_first.append(1.*px[j+1][i])
            y_right_first.append(1.*py[j+1][i])
        if px[j+1][i] > 5. and py[j+1][i] > 0.:
            x_right_second.append(px[j+1][i])
            y_right_second.append(py[j+1][i])
            
    distance_right.append(graph_and_fit(x_first=x_right_first,y_first=y_right_first,x_second=x_right_second,y_second=y_right_second))
    hist_right.Fill(distance_right[j])
    hist_total.Fill(distance_right[j])
    
    #third distance, top
    x_top_first, y_top_first = array('d'), array('d')
    x_top_second, y_top_second = array('d'), array('d')    
    for i in range(len(px[j+1])):
        if px[j+1][i] > -.1  and py[j+1][i] > 5: #excluding the points in the top left    (px[i] <0.1 and py[i > -8])
            x_top_first.append(1.*px[j+1][i])
            y_top_first.append(1.*py[j+1][i])
        if px[j+1][i] <-.1 and py[j+1][i] > 5:
            x_top_second.append(px[j+1][i])
            y_top_second.append(py[j+1][i])
    
    distance_top.append(graph_and_fit(x_first=x_top_first,y_first=y_top_first,x_second=x_top_second,y_second=y_top_second))
    hist_top.Fill(distance_top[j])
    hist_total.Fill(distance_top[j])
    
    #fourth distance, left
    x_left_first, y_left_first = array('d'), array('d')
    x_left_second, y_left_second = array('d'), array('d')    
    for i in range(len(px[j+1])):
        if px[j+1][i] < -5. and py[j+1][i] > -.1: #excluding the points in the top left    (px[i] <0.1 and py[i > -8])
            x_left_first.append(1.*px[j+1][i])
            y_left_first.append(1.*py[j+1][i])
        if px[j+1][i] < -5. and py[j+1][i] < -.1:
            x_left_second.append(px[j+1][i])
            y_left_second.append(py[j+1][i])
        
    distance_left.append(graph_and_fit(x_first=x_left_first,y_first=y_left_first,x_second=x_left_second,y_second=y_left_second))
    hist_left.Fill(distance_left[j])
    hist_total.Fill(distance_left[j])
    
c = ROOT.TCanvas("c","multigraph",200,10,700,500)
c.Divide(2,2)
c.cd(1)
hist_bottom.GetXaxis().SetTitle("Distance Between Sides [mm]")
hist_bottom.Draw("h")
c.cd(2)
hist_right.GetXaxis().SetTitle("Distance Between Sides [mm]")
hist_right.Draw("h")
c.cd(3)
hist_top.GetXaxis().SetTitle("Distance Between Sides [mm]")
hist_top.Draw("h")
c.cd(4)
hist_left.GetXaxis().SetTitle("Distance Between Sides [mm]")
hist_left.Draw("h")


c1 = ROOT.TCanvas("all distances between sides")
c1.cd()
hist_total.GetXaxis().SetTitle("Distance Between Sides [mm]")
hist_total.Draw("h")


input("press any key to close")

    

#plt.scatter(px, py, label='Scatter Plot', color='blue', marker='o')
#plt.xlabel('X-axis')
#plt.ylabel('Y-axis')
#plt.show()
#
#distances_x = []
#distances_y = []

#for i in range(int(len(px)/n_points_per_file)):
#    distances_x.append(-1*px[i*n_points_per_file]+px[i*n_points_per_file+1]-2.)
#    distances_x.append(px[i*n_points_per_file+4]-px[i*n_points_per_file+5]-2.)
#    distances_y.append(-1*py[i*n_points_per_file+2]+py[i*n_points_per_file+3]-2.)
#    distances_y.append(py[i*n_points_per_file+6]-py[i*n_points_per_file+7]-2.)

 
# Create histograms for X and Y distances
#plt.figure(figsize=(12, 4))
#plt.subplot(1, 2, 1)
#plt.hist(distances_x, bins=20, color='blue', edgecolor='black')
#plt.xlabel('Distance along X-axis')
#plt.ylabel('Frequency')
#plt.title('Histogram of X Distances')
#
#plt.subplot(1, 2, 2)
#plt.hist(distances_y, bins=20, color='green', edgecolor='black')
#plt.xlabel('Distance along Y-axis')
#plt.ylabel('Frequency')
#plt.title('Histogram of Y Distances')
#
#plt.tight_layout()
#plt.show()


