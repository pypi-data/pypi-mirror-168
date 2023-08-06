import numpy as np

def min_max_range(pcd_numpy):
    pts_endpoints = np.array([[pcd_numpy[:, i].min(), pcd_numpy[:, i].max()] for i in range(pcd_numpy.shape[1])])
    return pts_endpoints, pts_endpoints.min(), pts_endpoints.max()

# return thickness, endpoints, endpoints_values
def get_thickness_for_given_direction(pts, direction):
    ds = -np.dot(pts, direction)
    thickness = ds.max() - ds.min()
    endpoints = np.array([pts[ds.argmin()], pts[ds.argmax()]])
    endpoints_values = np.array([ds.min(), ds.max()])
    return thickness, endpoints, endpoints_values

def calc_pcds_distance_center(src_pcd, dist_pcd):
    return np.linalg.norm(src_pcd.get_center() - dist_pcd.get_center())

def calc_pcds_distance_to_direction_of_normal(src_pcd, dist_pcd):
    src_pts = np.array(src_pcd.points)
    src_pts_normal = np.array(src_pcd.normals)
    dist_pts = np.array(dist_pcd.points)
    dists = np.array([])
    for i in range(src_pts.shape[0]):
        # A + dot(AP,AB) / dot(AB,AB) * AB
        line_pts = src_pts[i] + np.dot((dist_pts - src_pts[i]), src_pts_normal[i][np.newaxis].T)
        dists2line = np.linalg.norm(line_pts - dist_pts, axis=1)
        inliers = np.where(np.abs(dists2line) <= 0.2)[0]
        signed_dist = (line_pts[inliers] - src_pts[i])[:, 0]
        # positive_inliers = np.where(signed_dist > 0)[0]
        if len(inliers)==0: dists = np.append(dists, 1)
        else: dists = np.append(dists, signed_dist.max())
    return dists

def calc_dist_pt2pts(origin, pts):
    return np.linalg.norm((pts[:] - origin), axis=1)

def calc_dist_pts2plane(pts, plane_eq):
    return (plane_eq[0] * pts[:, 0] + plane_eq[1] * pts[:, 1] + plane_eq[2] * pts[:, 2] + plane_eq[3]) / np.sqrt(plane_eq[0] ** 2 + plane_eq[1] ** 2 + plane_eq[2] ** 2)

def find_nearest_point_pair(bounding_box_points):
    pairs_idx = []
    excluded_idx = []
    for i, src_pt in enumerate(bounding_box_points):
        if i in excluded_idx: continue
        dists = np.array([np.linalg.norm(dist_pt - src_pt) if not i==j else 1e18 for j, dist_pt in enumerate(bounding_box_points) ])
        pairs_idx.append([i, dists.argmin()])
        excluded_idx.append(dists.argmin())
    return pairs_idx

def get_quadrant_centers(center, endpoints):
    pairs_idx = find_nearest_point_pair(endpoints)
    return np.mean(np.array([[center, np.mean(endpoints[pair_idx], axis=0)] for pair_idx in pairs_idx]), axis=1)


def define_quadrant_relative_position(center, quadrant_centers, quadrant_ignore_axis=0):
    right_upper_idx, right_lower_idx, left_upper_idx, left_lower_idx = None, None, None, None
    vectors = np.array([quadrant - center for quadrant in quadrant_centers])
    # left side vectors order
    left_ids = np.array(vectors[:, (quadrant_ignore_axis+1)%3]).argsort()
    # right side vectors order
    right_ids = np.array(- vectors[:, (quadrant_ignore_axis+1)%3]).argsort()
    # uppeer side vectors order
    upper_ids = np.array(vectors[:, (quadrant_ignore_axis+2)%3]).argsort()

    if vectors[np.where(right_ids==1)][0][(quadrant_ignore_axis+1)%3] != vectors[np.where(right_ids==2)][0][(quadrant_ignore_axis+1)%3]:
        if upper_ids[np.where(right_ids==0)] > upper_ids[np.where(right_ids==1)]:
            right_upper_idx = np.where(right_ids==0)[0][0]
            right_lower_idx = np.where(right_ids==1)[0][0]
        else:
            right_upper_idx = np.where(right_ids==1)[0][0]
            right_lower_idx = np.where(right_ids==0)[0][0]
    else:
        right_lower_idx = upper_ids[np.where(right_ids==0)]
        # get upper side orde of most right side vector
        if upper_ids[np.where(right_ids==1)] > upper_ids[np.where(right_ids==2)]: right_upper_idx = np.where(right_ids==2)[0][0]
        else: right_upper_idx = np.where(right_ids==1)[0][0]

    if vectors[np.where(left_ids==1)][0][(quadrant_ignore_axis+1)%3] != vectors[np.where(left_ids==2)][0][(quadrant_ignore_axis+1)%3]:
        if upper_ids[np.where(left_ids==0)] > upper_ids[np.where(left_ids==1)]:
            left_upper_idx = np.where(left_ids==0)[0][0]
            left_lower_idx = np.where(left_ids==1)[0][0]
        else:
            left_upper_idx = np.where(left_ids==1)[0][0]
            left_lower_idx = np.where(left_ids==0)[0][0]
    else:
        left_lower_idx = upper_ids[np.where(left_ids==0)]
        # get upper side orde of most right side vector
        if upper_ids[np.where(left_ids==1)] > upper_ids[np.where(left_ids==2)]: left_upper_idx = np.where(left_ids==2)[0][0]
        else: left_upper_idx = np.where(left_ids==1)[0][0]
    return right_upper_idx, right_lower_idx, left_upper_idx, left_lower_idx