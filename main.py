import glob
import sys
import time

import numpy as np
import open3d as o3d
import tkinter.filedialog as file_chooser

import ply

if __name__ == "__main__":

    print("Load a ply point cloud, print it, and render it")
    filename = file_chooser.askdirectory(initialdir="/home/alec/Documents/UofT")
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

    for polyfile in sorted(glob.glob(f'{filename}/*.ply')):
        ply_pcd = ply.read_ply(polyfile)
        pcd.points = o3d.io.read_point_cloud(polyfile).points
        pcd.paint_uniform_color((0.45, 0.45, 0.45))
        colors = np.asarray(pcd.colors)
        colors[ply_pcd['pre'] == 1] = (1, 0, 0)
        vis.update_geometry(pcd)
        t = time.time()
        while time.time() - t < 0.1:
            vis.poll_events()
            vis.update_renderer()
