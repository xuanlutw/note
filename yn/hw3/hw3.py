import pydicom
import scipy.misc
import os

#Task 1
f = open("./hw3_data/data_list.txt", 'r')
data = f.read().splitlines();
f.close();
print(data);

#Task 2
ds = [];
for item in data:
    ds.append(pydicom.dcmread("./hw3_data/" + item));
for item in ds:
    print("Patient's name: " + item.PatientName);
    print("Patient ID: " + item.PatientID);

#Task 3
for item in ds:
    item.PatientName = "CutePusheen";
    item.PatientID = "00000";

#Task 4
for item in ds:
    index = str(ds.index(item));
    #scipy.misc.imsave(index + "_pre.png", item.pixel_array);
    g_max = item.pixel_array.max();
    g_min = item.pixel_array.min();
    g_th = (g_max + g_min) / 2;
    item.pixel_array[item.pixel_array > g_th] = g_max;
    item.pixel_array[item.pixel_array <= g_th] = g_min;
    #scipy.misc.imsave(index + "_after.png", item.pixel_array);

#Task 5
os.mkdir("output");
for item in ds:
    index = str(ds.index(item));
    item.save_as("./output/" + index + "-00000.dcm");

#Task 6
f = open("./output/output_list.txt", "w+");
for item in ds:
    index = str(ds.index(item));
    f.write(index + "-00000.dcm\n");
f.close();
