import os
from pydicom import dcmread
import glob
import csv
filenum = 0
x = 0
n = 80
dir = '/dir/path'
tree = []
eighty_studies = []
good_massive = []
for dirpath, dirnames, files in os.walk(dir):
    tree.append(dirpath)
for element in tree:
    num_files = len([f for f in os.listdir(element) if os.path.isfile(os.path.join(element, f))])
    if num_files > n:
        eighty_studies.append(element)

    #print('\n'.join(eighty_studies))

for dirpath in eighty_studies:
    pathh = str(dirpath)
    for root, dirs, files in os.walk(pathh):
        for file in files:
            abspath = os.path.join(root, file)
            dcm = dcmread(abspath)
            if dcm.ConvolutionKernel == "STANDARD" and dcm.StudyDescription == "CHEST":
                elem = dirpath
            if elem not in good_massive:
                good_massive.append(dirpath)
            else:
                continue

with open("studies.csv", mode='w') as w_file:
    names = ['StudyInstanceUID', 'SeriesInstanceUID', 'StudyDescription', 'ConvolutionKernel', 'SliceThickness']
    file_writer = csv.DictWriter(w_file, delimiter=",",
                                     lineterminator="\r", fieldnames=names)
    file_writer.writeheader()
    for good_study in good_massive:
        path2 = str(good_study)
        for root, dirs, files in os.walk(path2):
            for file in files:
                abspath = os.path.join(root, file)
                ds = dcmread(abspath)
            file_writer.writerow({'StudyInstanceUID': f'{ds.StudyInstanceUID}', 'SeriesInstanceUID': f'{ds.SeriesInstanceUID}',
                                  'StudyDescription': f'{ds.WholeBodyTechnique}', 'ConvolutionKernel': f'{ds.ConvolutionKernel}', 'SliceThickness': f'{ds.SliceThickness}'})

print('\n'.join(good_massive))
