import pydicom, os
data = open("./hw3_data/data_list.txt", 'r').read().splitlines();
print(data);
os.mkdir("output");
f = open("./output/output_list.txt", "w+");
for filename in data:
    item = pydicom.dcmread("./hw3_data/" + filename);
    print("Patient's name: " + item.PatientName + "\nPatient ID: " + item.PatientID);
    item.PatientName = "CutePusheen";
    item.PatientID = "00000";
    g_th = (item.pixel_array.max() + item.pixel_array.min()) / 2;
    item.pixel_array[item.pixel_array > g_th] = item.pixel_array.max();
    item.pixel_array[item.pixel_array <= g_th] = item.pixel_array.min();
    item.save_as("./output/" + str(data.index(filename)) + "-00000.dcm");
    f.write(str(data.index(filename)) + "-00000.dcm\n");
