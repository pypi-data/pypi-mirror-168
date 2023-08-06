from lib2to3.pytree import convert
import numpy as np
import open3d as o3d
import matplotlib.pyplot as plt
import random
import copy
from . import measure

def clustering(pcd, show=False):
    labels = np.array(pcd.cluster_dbscan(0.75, 5, print_progress=True))
    print(f"point cloud has {labels.max() + 1} clusters")
    colors = plt.get_cmap("tab20")(labels / (labels.max() if labels.max() > 0 else 1))
    colors[labels < 0] = 0
    pcd.colors = o3d.utility.Vector3dVector(colors[:, :3])
    if show: o3d.visualization.draw_geometries([pcd], "Open3D dbscanclusting")
    return pcd, labels

def select_cluster(pcds, labels, cluster):
    return np.array([pcds[index] for index, label in enumerate(labels) if label==cluster])

def sampling_and_cluster_filtering(pcd, vsize, with_normals=True):
    if vsize == 0: voxel_down_pcd = pcd
    else: voxel_down_pcd = pcd.voxel_down_sample(voxel_size=vsize)
    voxel_down_pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=vsize*15, max_nn=100))
    clustered_pcd, labels = clustering(voxel_down_pcd, False)
    clustered_pcd_as_array = np.asarray(clustered_pcd.points)
    return convert_numpy2pcd(select_cluster(clustered_pcd_as_array, labels, np.array([len(np.where(labels==label_idx)[0]) for label_idx in range(labels.max()+1)]).argmax()))

def ransac_normal(pcd, sample_points=10, iteration=100):
    min_error = np.Inf
    min_normal = None
    pcd_normals = np.asarray(pcd.normals)
    n_points = pcd_normals.shape[0]
    for _ in range(iteration):
        id_samples = random.sample(range(0, n_points), 2)
        id_samples_tunnel = random.sample(range(0, n_points), sample_points)
        normal_samples = pcd_normals[id_samples]
        normal = np.cross(normal_samples[0], normal_samples[1])
        normal_norm = normal/np.linalg.norm(normal)
        normal_stack = np.stack([normal_norm] * sample_points, 0)
        tunnel_sample_normals = pcd_normals[id_samples_tunnel]
        error = np.sum(abs(np.dot(normal_stack, tunnel_sample_normals.T)))
        if min_error > error :
            min_error = error
            min_normal = normal_norm
    if min_normal[0] < 0: min_normal = -1* min_normal
    return min_normal

def convert_numpy2pcd(pts, normals=None, colors=None, vsize=0.2, sampling=False):
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(pts)
    if normals is None:
        pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=vsize*15, max_nn=100))
    else:
        assert pts.shape==normals.shape
        pcd.normals = o3d.utility.Vector3dVector(normals)

    if colors is None: pcd.paint_uniform_color([0, 0, 0])
    else:
        assert pts.shape==colors.shape
        pcd.colors = o3d.utility.Vector3dVector(colors)
    return pcd if not sampling else pcd.voxel_down_sample(voxel_size=vsize)

def set_normal(pcd, normals):
    assert np.array(pcd.points).shape==normals.shape
    pcd.normals = o3d.utility.Vector3dVector(normals)
    return pcd

def set_color(pcd, colors):
    assert np.array(pcd.points).shape[0]==colors.shape[0]
    pcd.colors = o3d.utility.Vector3dVector(colors)
    return pcd

def remove_specific_vector_plane(pcd, vector, threshold=0.6):
    pts = np.array([pcd.points])[0]
    best_eq = []
    best_inliers = []
    pts_endpoints, _min, _max = measure.min_max_range(pts)
    maxIteration=1000
    for it in range(maxIteration):
        d = random.uniform(_min, _max)
        plane_eq = [vector[0], vector[1], vector[2], d]

        # Distance from a point to a plane
        # https://mathworld.wolfram.com/Point-PlaneDistance.html
        pt_id_inliers = []  # list of inliers ids
        dist_pt = (
            plane_eq[0] * pts[:, 0] + plane_eq[1] * pts[:, 1] + plane_eq[2] * pts[:, 2] + plane_eq[3]
        ) / np.sqrt(plane_eq[0] ** 2 + plane_eq[1] ** 2 + plane_eq[2] ** 2)

        # Select indexes where distance is biggers than the threshold
        pt_id_inliers = np.where(np.abs(dist_pt) <= threshold)[0]
        if len(pt_id_inliers) > len(best_inliers):
            best_eq = plane_eq
            best_inliers = pt_id_inliers
    pt_inliers_plane = pts[best_inliers]
    ind = np.ones(pts.shape[0], dtype=bool)
    ind[best_inliers] = False
    pt_outliers = pts[ind]
    return convert_numpy2pcd(pt_outliers), convert_numpy2pcd(pt_inliers_plane), best_eq

def get_points_within_plane(pcd, plane_eq, threshold = 2.0):
    pts = np.array([copy.deepcopy(pcd).points])[0]
    dist_pt = (
        plane_eq[0] * pts[:, 0] + plane_eq[1] * pts[:, 1] + plane_eq[2] * pts[:, 2] + plane_eq[3]
    ) / np.sqrt(plane_eq[0] ** 2 + plane_eq[1] ** 2 + plane_eq[2] ** 2)

    # Select indexes where distance is biggers than the threshold
    pt_inliers = np.where(np.abs(dist_pt) <= threshold)[0]
    pt_outliers = np.ones(pts.shape[0], dtype=bool)
    pt_outliers[pt_inliers] = False
    return convert_numpy2pcd(pts[pt_outliers]), convert_numpy2pcd(pts[pt_inliers])

def correct_normal_direction(pcd, idx, positive=True):
    pts = np.array(pcd.points)
    normals = np.array(pcd.normals)
    assert pts.shape==normals.shape
    if positive: normals = np.array([normal if normal[idx] > 0 else -1 * normal for normal in normals ])
    else: normals = np.array([normal if normal[idx] < 0 else -1 * normal for normal in normals ])
    return convert_numpy2pcd(pts, normals=normals)

# get closest plane to origin[0, 0, 0]
def get_closest_plane(pts, normal):
    return np.append(normal, measure.get_thickness_for_given_direction(pts, normal)[2][0])

def project_pts2line(line_origin, line_vector, pts):
    return line_origin + np.dot((pts - pts), line_vector[np.newaxis].T)

def project_pts2plane(pts, plane):
    dists_plane = measure.calc_dist_pts2plane(pts, plane)
    n_points = pts.shape[0]
    vecs = np.stack([plane[:3]] * n_points, 0)
    return (pts - (vecs.T*dists_plane).T)

def extend_pcd_for_given_direction(pcd, direction, length, start_pos=0, div_num=15):
    extended_pts = None
    extended_normals = None
    for i in np.linspace(-start_pos, -start_pos+length, div_num):
        if extended_pts is None: extended_pts = np.array((copy.deepcopy(pcd).translate(-direction*i)).points)
        extended_pts = np.vstack((extended_pts, np.array((copy.deepcopy(pcd).translate(-direction*i)).points)))
        if extended_normals is None: extended_normals = np.array(pcd.normals)
        extended_normals = np.vstack((extended_normals, np.array(pcd.normals)))
    return convert_numpy2pcd(extended_pts, normals=extended_normals, vsize=0.2, sampling=True)

def define_quadrant_bounding_box(bounding_box, quadrant_ignore_axis=0):
    box_endpts = np.array(bounding_box.get_box_points())
    quadrant_centers = measure.get_quadrant_centers(bounding_box.center, box_endpts)
    idxes = measure.define_quadrant_relative_position(bounding_box.center, quadrant_centers, quadrant_ignore_axis)
    divided_extent = [*bounding_box.extent[:2]/2, bounding_box.extent[2]]
    obb_quadrants = [o3d.geometry.OrientedBoundingBox(qudrant_center, bounding_box.R, divided_extent) for qudrant_center in quadrant_centers]
    return obb_quadrants[idxes[0]], obb_quadrants[idxes[1]], obb_quadrants[idxes[2]], obb_quadrants[idxes[3]]