import glob
import sys
import time

import numpy as np
import open3d as o3d
import tkinter.filedialog as file_chooser

import ply

LABEL = 'pre'
LABEL_IDX = 2

if __name__ == "__main__":

    print("Load a ply point cloud, print it, and render it")
    filename = file_chooser.askdirectory(initialdir="/home/alec/ASRL/vtr3/KPConvX_withlidar")
    if filename is None:
        print("No file selected")
        sys.exit(0)
    print("opening", filename)

    vis = o3d.visualization.Visualizer()
    vis.create_window()

    pcd = o3d.io.read_point_cloud(glob.glob(f'{filename}/*.ply')[0])
    vis.add_geometry(pcd)
    vis.poll_events()
    vis.update_renderer()

    tps = 0
    fps = 0
    fns = 0
    tns = 0

    for polyfile in sorted(glob.glob(f'{filename}/*.ply')):
        ply_pcd = ply.read_ply(polyfile)
        pcd.points = o3d.io.read_point_cloud(polyfile).points
        pcd.paint_uniform_color((0.45, 0.45, 0.45))
        colors = np.asarray(pcd.colors)

        tps += np.sum((ply_pcd['pre'] == LABEL_IDX) & (ply_pcd['gt'] == LABEL_IDX))
        fps += np.sum((ply_pcd['pre'] == LABEL_IDX) & (ply_pcd['gt'] != LABEL_IDX))
        fns += np.sum((ply_pcd['pre'] != LABEL_IDX) & (ply_pcd['gt'] == LABEL_IDX))
        tns += np.sum((ply_pcd['pre'] != LABEL_IDX) & (ply_pcd['gt'] != LABEL_IDX))

        colors[ply_pcd[LABEL] == LABEL_IDX] = (1, 0, 0)
        vis.update_geometry(pcd)
        t = time.time()
        while time.time() - t < 0.5:
            vis.poll_events()
            vis.update_renderer()
    print(f"Summary for run TP;FP;FN;TN;P;N;IOU;PRE;REC")
    print(f"{tps};{fps};{fns};{tns};{tps+fns};{tns+fps}")
    print(f"{tps/(fns+fps+tps)};{tps/(tps+fps)};{tps/(tps+fns)}")
