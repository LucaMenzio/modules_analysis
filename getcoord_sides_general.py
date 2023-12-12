import os
import matplotlib.pyplot as plt
import numpy as np
from array import array
import ROOT

#constants
PI = 3.14159265359

def graph_and_fit(x_first, y_first, x_second, y_second):
    graph_first = ROOT.TGraph(len(x_first),x_first,y_first)
    fit_function_first = ROOT.TF1("pol1_first","[0]+x*[1]")
    graph_first.Fit("pol1_first","Q0")
    graph_second = ROOT.TGraph(len(x_second),x_second,y_second)
    fit_function_second = ROOT.TF1("pol1_second","[0]+x*[1]")
    fit_function_second.FixParameter(1,fit_function_first.GetParameter(1))
    graph_second.Fit("pol1_second","Q0")
    return np.abs(fit_function_first.GetParameter(0) - fit_function_second.GetParameter(0))/np.sqrt(fit_function_first.GetParameter(1)*fit_function_first.GetParameter(1)+1) #distance between two parallel lines

def fit_for_angles(x_first,y_first,x_second,y_second):
    graph_first = ROOT.TGraph(len(x_first),x_first,y_first)
    fit_function_first = ROOT.TF1("pol1_first","[0]+x*[1]")
    graph_first.Fit("pol1_first","Q0")
    graph_second = ROOT.TGraph(len(x_second),x_second,y_second)
    fit_function_second = ROOT.TF1("pol1_second","[0]+x*[1]")
    graph_second.Fit("pol1_second","Q0")
    return fit_function_first.GetParameter(1), fit_function_first.GetParError(1), fit_function_second.GetParameter(1), fit_function_second.GetParError(1)
    

#filespath = "/home/luca/Desktop/Analisi/modules/Data_measurements/Batch3/precura/"
filespath = "/home/luca/Desktop/Analisi/modules/Data_measurements/Batch3/postcura/"
plots_dir = ""
if "Batch3" in filespath:
    if "precura" in filespath:
        plots_dir = "/home/luca/Desktop/Analisi/modules/scripts/Figures/batch3_sides/precura/"
    if "postcura" in filespath:
        plots_dir = "/home/luca/Desktop/Analisi/modules/scripts/Figures/batch3_sides/postcura/"
    if "both" in filespath:
        plots_dir = "/home/luca/Desktop/Analisi/modules/scripts/Figures/batch3_sides/both/"
if "Batch2" in filespath:
    plots_dir = "/home/luca/Desktop/Analisi/modules/scripts/Figures/batch2_sides/"
max_files = 100

px_temp, py_temp, pz_temp = [], [], []
filenames = []
px, py, pz = [[]], [[]], [[]]
n_points_per_file = 24
n_files = 1
for k, filename in enumerate(os.listdir(filespath)):
    if(k > max_files):
        break
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

cut_bottom = -0.25 #first set of points always has a point outside of ROI (bug in mitutoyo script)

Angle_br, Angle_bl, Angle_rt, Angle_rb, Angle_tr, Angle_tl, Angle_lt, Angle_lb = [], [], [], [], [], [], [], []
eAngle_br, eAngle_bl, eAngle_rt, eAngle_rb, eAngle_tr, eAngle_tl, eAngle_lt, eAngle_lb = [], [], [], [], [], [], [], []

angle_min_bin_horizontal, angle_max_bin_horizontal = -2,2.
angle_min_bin_vertical, angle_max_bin_vertical = 89.,91

hist_angle_left_top     = ROOT.TH1F("angles left top","angles left top", n_bins, angle_min_bin_horizontal, angle_max_bin_horizontal)
hist_angle_left_bottom  = ROOT.TH1F("angles left bottom","angles left bottom", n_bins, angle_min_bin_horizontal, angle_max_bin_horizontal)
hist_angle_right_top    = ROOT.TH1F("angles right top","angles right top", n_bins, angle_min_bin_horizontal, angle_max_bin_horizontal)
hist_angle_right_bottom = ROOT.TH1F("angles right bottom","angles right bottom", n_bins, angle_min_bin_horizontal, angle_max_bin_horizontal)
hist_angle_top_right    = ROOT.TH1F("angles top right","angles top right", n_bins, angle_min_bin_vertical, angle_max_bin_vertical)
hist_angle_top_left     = ROOT.TH1F("angles top left","angles top left", n_bins, angle_min_bin_vertical, angle_max_bin_vertical)
hist_angle_bottom_right = ROOT.TH1F("angles bottom right","angles bottom right", n_bins, angle_min_bin_vertical, angle_max_bin_vertical)
hist_angle_bottom_left  = ROOT.TH1F("angles bottom left","angles bottom left", n_bins, angle_min_bin_vertical, angle_max_bin_vertical)

for j in range(1,n_files):
    print(filenames[j-1])
    if(j>max_files):
        break
    x_bottom_right, y_bottom_right = array('d'), array('d')
    x_bottom_left, y_bottom_left = array('d'), array('d')
    
    x_right_top, y_right_top = array('d'), array('d')
    x_right_bottom, y_right_bottom = array('d'), array('d')
    
    x_top_right, y_top_right = array('d'), array('d')
    x_top_left, y_top_left = array('d'), array('d')
    
    x_left_top, y_left_top = array('d'), array('d')
    x_left_bottom, y_left_bottom = array('d'), array('d')
    
    for i in range(len(px[j])):
        if i%2 != 0:
            continue
        #bottom
        if i < 6:
            if(px[j][i] < cut_bottom or px[j][i+1] < cut_bottom):
                continue
            if(px[j][i]>px[j][i+1]):
                x_bottom_right.append(px[j][i])
                y_bottom_right.append(py[j][i])
                x_bottom_left.append(px[j][i+1])
                y_bottom_left.append(py[j][i+1])
            else:
                x_bottom_right.append(px[j][i+1])
                y_bottom_right.append(py[j][i+1])
                x_bottom_left.append(px[j][i])
                y_bottom_left.append(py[j][i])     
                
        #right
        if i >= 6 and i < 12:
            if(py[j][i]>py[j][i+1]):
                x_right_top.append(px[j][i])
                y_right_top.append(py[j][i])
                x_right_bottom.append(px[j][i+1])
                y_right_bottom.append(py[j][i+1])
            else:
                x_right_top.append(px[j][i+1])
                y_right_top.append(py[j][i+1])
                x_right_bottom.append(px[j][i])
                y_right_bottom.append(py[j][i])
                
        #top
        if i>=12 and i < 18:
            if(px[j][i]>px[j][i+1]):
                x_top_right.append(px[j][i])
                y_top_right.append(py[j][i])
                x_top_left.append(px[j][i+1])
                y_top_left.append(py[j][i+1])
            else:
                x_top_right.append(px[j][i+1])
                y_top_right.append(py[j][i+1])
                x_top_left.append(px[j][i])
                y_top_left.append(py[j][i])
        #left
        if i>=18 and i<24:
            if(py[j][i]>py[j][i+1]):
                x_left_top.append(px[j][i])
                y_left_top.append(py[j][i])
                x_left_bottom.append(px[j][i+1])
                y_left_bottom.append(py[j][i+1])
            else:
                x_left_top.append(px[j][i+1])
                y_left_top.append(py[j][i+1])
                x_left_bottom.append(px[j][i])
                y_left_bottom.append(py[j][i])
    

    #print(len(x_bottom_left),len(x_bottom_right),len(x_right_bottom),len(x_right_top),len(x_top_left),len(x_top_right),len(x_left_bottom),len(x_left_top))
    
    #computing distances for each measurement and filling histograms
    distance_bottom.append(graph_and_fit(x_first=x_bottom_right,y_first=y_bottom_right,x_second=x_bottom_left,y_second=y_bottom_left))
    hist_bottom.Fill(distance_bottom[j-1])
    hist_total.Fill(distance_bottom[j-1])
    
    distance_right.append(graph_and_fit(x_first=x_right_top,y_first=y_right_top,x_second=x_right_bottom,y_second=y_right_bottom))
    hist_right.Fill(distance_right[j-1])
    hist_total.Fill(distance_right[j-1])
    
    distance_top.append(graph_and_fit(x_first=x_top_right,y_first=y_top_right,x_second=x_top_left,y_second=y_top_left))
    hist_top.Fill(distance_top[j-1])
    hist_total.Fill(distance_top[j-1])
    
    distance_left.append(graph_and_fit(x_first=x_left_top,y_first=y_left_top,x_second=x_left_bottom,y_second=y_left_bottom))
    hist_left.Fill(distance_left[j-1])
    hist_total.Fill(distance_left[j-1])
    
    #computing tilt angles for each measurement and filling histograms
    angle_bottom_right, err_angle_bottom_right, angle_bottom_left, err_angle_bottom_left = fit_for_angles(x_first=x_bottom_right,y_first=y_bottom_right,x_second=x_bottom_left,y_second=y_bottom_left)
    Angle_br.append(angle_bottom_right)
    eAngle_br.append(err_angle_bottom_right)
    Angle_bl.append(angle_bottom_left)
    eAngle_bl.append(err_angle_bottom_left)
    hist_angle_bottom_right.Fill(180./PI*ROOT.TMath.Abs(ROOT.TMath.ATan(angle_bottom_right)))
    hist_angle_bottom_left.Fill(180./PI*ROOT.TMath.Abs(ROOT.TMath.ATan(angle_bottom_left)))
    
    angle_right_top, err_angle_right_top, angle_right_bottom, err_angle_right_bottom = fit_for_angles(x_first=x_right_top,y_first=y_right_top,x_second=x_right_bottom,y_second=y_right_bottom)
    Angle_rt.append(angle_right_top)
    eAngle_rt.append(err_angle_right_top)
    Angle_rb.append(angle_right_bottom)
    eAngle_rb.append(err_angle_right_bottom)
    hist_angle_right_top.Fill(180./PI*ROOT.TMath.Abs(ROOT.TMath.ATan(angle_right_top)))
    hist_angle_right_bottom.Fill(180./PI*ROOT.TMath.Abs(ROOT.TMath.ATan(angle_right_bottom)))
    
    angle_top_right, err_angle_top_right, angle_top_left, err_angle_top_left = fit_for_angles(x_first=x_top_right,y_first=y_top_right,x_second=x_top_left,y_second=y_top_left)
    Angle_tr.append(angle_top_right)
    eAngle_tr.append(err_angle_top_right)
    Angle_tl.append(angle_top_left)
    eAngle_tl.append(err_angle_top_left)
    hist_angle_top_right.Fill(180./PI*ROOT.TMath.Abs(ROOT.TMath.ATan(angle_top_right)))
    hist_angle_top_left.Fill(180./PI*ROOT.TMath.Abs(ROOT.TMath.ATan(angle_top_left)))
    
    angle_left_top, err_angle_left_top, angle_left_bottom, err_angle_left_bottom = fit_for_angles(x_first=x_left_top,y_first=y_left_top,x_second=x_left_bottom,y_second=y_left_bottom)
    Angle_lt.append(angle_left_top)
    eAngle_lt.append(err_angle_left_top)
    Angle_lb.append(angle_left_bottom)
    eAngle_lb.append(err_angle_left_bottom)
    hist_angle_left_top.Fill(180./PI*ROOT.TMath.Abs(ROOT.TMath.ATan(angle_left_top)))
    hist_angle_left_bottom.Fill(180./PI*ROOT.TMath.Abs(ROOT.TMath.ATan(angle_left_bottom)))

minbin_diff, maxbin_diff = -.05,.05

#comparison of precuring vs postcuring
hDiffBottom = ROOT.TH1F("Diff Bottom","Diff Bottom",n_bins,minbin_diff,maxbin_diff)
hDiffBottom.GetXaxis().SetTitle("Pre- minus Post- curing distance [mm]")
hDiffTop = ROOT.TH1F("Diff Top","Diff Top",n_bins,minbin_diff,maxbin_diff)
hDiffTop.GetXaxis().SetTitle("Pre- minus Post- curing distance [mm]")
hDiffRight = ROOT.TH1F("Diff Right","Diff Right",n_bins,minbin_diff,maxbin_diff)
hDiffRight.GetXaxis().SetTitle("Pre- minus Post- curing distance [mm]")
hDiffLeft = ROOT.TH1F("Diff Left","Diff Left",n_bins,minbin_diff,maxbin_diff)
hDiffLeft.GetXaxis().SetTitle("Pre- minus Post- curing distance [mm]")

if "both" in filespath:
    compared = False
    already_compared = []
    print("\nComparing measurements from both pre-curing and post-curing")
    for k, filename in enumerate(filenames):
        
        #looking for the pre-curing files only
        if("precura" not in filename):
            continue
        
        jPostCuring = -1
        #looking for the index of the other file
        for j, post_filename in enumerate(filenames):
            if post_filename == filename.replace("_precura",""): 
                jPostCuring = j
                print(f"Found that file {filenames[jPostCuring]} corresponds to {filename}")
        if jPostCuring == -1:
            print(f"The file {filename} does not have a corresponding post-curing file, aborting")
            exit()

        hDiffBottom.Fill(abs(distance_bottom[k])-abs(distance_bottom[jPostCuring]))
        hDiffTop.Fill(abs(distance_top[k])-abs(distance_top[jPostCuring]))
        hDiffRight.Fill(abs(distance_right[k])-abs(distance_right[jPostCuring]))
        hDiffLeft.Fill(abs(distance_left[k])-abs(distance_left[jPostCuring]))

#some plotting

c = ROOT.TCanvas("c","multigraph",2000,10,7000,6000)
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
c.SaveAs(plots_dir+"single_dist.pdf")

c1 = ROOT.TCanvas("all distances between sides")
c1.cd()
hist_total.GetXaxis().SetTitle("Distance Between Sides [mm]")
hist_total.Draw("h")
c1.SaveAs(plots_dir+"all_dist.pdf")

c_angles = ROOT.TCanvas("c_angles","Tilt angles of modules",2000,10,7000,6000)
c_angles.Divide(4,2)
c_angles.cd(1)
hist_angle_bottom_left.Draw("h")
c_angles.cd(2)
hist_angle_bottom_right.Draw("h")
c_angles.cd(3)
hist_angle_right_top.Draw("h")
c_angles.cd(4)
hist_angle_right_bottom.Draw("h")
c_angles.cd(5)
hist_angle_top_right.Draw("h")
c_angles.cd(6)
hist_angle_top_left.Draw("h")
c_angles.cd(7)
hist_angle_left_top.Draw("h")
c_angles.cd(8)
hist_angle_left_bottom.Draw("h")
c_angles.SaveAs(plots_dir+"single_angles.pdf")

c_differences = ROOT.TCanvas("c_differences","Shift between pre and post curing",2000,10,7000,6000)
c_differences.Divide(2,2)
c_differences.cd(1)
hDiffBottom.Draw("h")
c_differences.cd(2)
hDiffRight.Draw("h")
c_differences.cd(3)
hDiffTop.Draw("h")
c_differences.cd(4)
hDiffLeft.Draw("h")
c_differences.SaveAs(plots_dir+"differences.pdf")

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


