import open3d as o3d
import numpy as np
import sensor_msgs.point_cloud2 as pc2
import csv

def read_pcds_from_bag(rosbag, pcd_topic:str, device=o3d.core.Device("CPU:0")):
    pcds = []
    times = []
    for topic, msg, t in rosbag.read_messages():
        if topic == pcd_topic:
            pcd = np.array(list(pc2.read_points(msg)))
            _pcd = o3d.t.geometry.PointCloud(device)
            _pcd.point["positions"] = o3d.core.Tensor(pcd[:, :3], device=device)
            _pcd.point["intensities"] = o3d.core.Tensor(pcd[:, 3], device=device)
            pcds.append(_pcd)
            times.append(t.to_time())
    return pcds, times

def write_csv(filename, pts, normals=None, dists=None):
    if normals is not None: assert pts.shape==normals.shape
    if dists is not None: assert pts.shape[0]==dists.shape[0]
    with open(filename, 'w') as f:
        writer = csv.writer(f)
        header = ["point_x", "point_y", "point_z"]
        if normals is not None: header.extend(["normal_x", "normal_y", "normal_z"])
        if dists is not None: header.extend(["distance"])
        writer.writerow(header)
        for idx in range(pts.shape[0]):
            data = []
            if normals is not None and dists is not None: data = [*pts[idx], *normals[idx], dists[idx]]
            elif normals is not None : data = [*pts[idx], *normals[idx]]
            elif dists is not None: data = [*pts[idx], dists[idx]]
            else:  data = [*pts[idx]]
            assert len(header) == len(data)
            writer.writerow(data)

# @ return points, normals, distances
def load_csv(filepath):
    arr = np.loadtxt(filepath, delimiter=',', skiprows=1, dtype='float64')
    print(filepath, arr.shape)
    if arr.shape[1]==7:
        return arr[:, :3], arr[:, 3:6], arr[:, 6]
    elif arr.shape[1]==3:
        return arr, None, None
    else:
        return None, None, None