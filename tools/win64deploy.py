#!/usr/bin/python3

import os
import shutil
import glob

#%% EXTERNAL PATHS
qt_path = "c:/Qt/5.12.10/msvc2017_64"
qbin_path = qt_path + "/bin"
msvc_path = r"C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC"

#%% INTERNAL PATHS
root = "C:/Users/Wagenaar/Documents/Progs/qplot"
qplot_build = root + "/build-qplot-Desktop_Qt_5_12_10_MSVC2017_64bit-Release/release"
release_path = root + "/release-x64"
bin_path = release_path + "/bin"
py_path = release_path + "/pyqplot"

#%%
envpath = os.environ['PATH'].split(";")
usepath = [p for p in envpath if "anaconda" not in p.lower()]
os.environ['PATH'] = ';'.join(usepath)
os.environ['VCINSTALLDIR'] = msvc_path

#%%
if not os.path.exists(qplot_build + "/qplot.exe"):
    raise Exception("qplot executable not found")

#%%
if os.path.exists(release_path):
    shutil.rmtree(release_path)
os.mkdir(release_path)
os.mkdir(bin_path)
os.mkdir(py_path)

os.system(f"{qbin_path}/windeployqt --release --dir {bin_path} {qplot_build}/qplot.exe")
shutil.copy(f"{qplot_build}/qplot.exe", bin_path)

for py in glob.glob(f"{root}/pyqplot/*.py"):
    shutil.copy(py, py_path)

#%%
print("Now run 'tools/qplot-x64.iss' using Inno Setup.")
