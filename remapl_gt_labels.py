import glob
import sys
import time

import numpy as np
import open3d as o3d
import tkinter.filedialog as file_chooser

import ply
from metrics import fast_confusion

LABEL = 'pre'
LABEL_IDX = 1
mappings = [(0, 1), (1, 2), (2, 0)]

if __name__ == "__main__":

    print("Load a ply point cloud, print it, and render it")
    filename = file_chooser.askdirectory(initialdir="/home/alec/ASRL/vtr3/KPConvX_withlidar")
    if filename is None:
        print("No file selected")
        sys.exit(0)
    print("opening", filename)

    tps = 0
    fps = 0
    fns = 0
    tns = 0

    for polyfile in sorted(glob.glob(f'{filename}/*.ply')):
        ply_pcd = ply.read_ply(polyfile)
        pre = ply_pcd['pre']

        conf = fast_confusion(ply_pcd['gt'], pre.astype(np.int32), label_values=np.array([0, 1, 2]))
        print(conf)

        tps += conf[1, 1]
        fps += conf[1, 0] + conf[1, 2]
        fns += conf[0, 1] + conf[2, 1]
        tns += conf[0, 0]

    print(f"Summary for run TP:{tps}, FP:{fps}, FN:{fns}, TN:{tns}. IoU:{tps/(fns+fps+tps)}")
