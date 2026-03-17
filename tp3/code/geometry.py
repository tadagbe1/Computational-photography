import numpy as np

def compute_intermediate_points(pts1, pts2, warp_frac):
    return (1 - warp_frac)*pts1 + warp_frac*pts2

def get_triangle_vertices(points, triangle_indices):
    return points[triangle_indices]

def compute_affine_matrix(src_triangle, dst_triangle):
    src = np.vstack([src_triangle.T, np.ones((1, 3))])
    dst = np.vstack([dst_triangle.T, np.ones((1, 3))])
    return dst @ np.linalg.inv(src)

def apply_affine_transform(matrix, points):
    ones = np.ones((points.shape[0], 1))
    homo_points = np.hstack([points, ones]) #(N, 3)
    transformed = (matrix @ homo_points.T).T  #(N, 3)
    return transformed[:, :2]

def inverse_affine_transform(matrix, points):
    inv_matrix = np.linalg.inv(matrix)
    return apply_affine_transform(inv_matrix, points)

def compute_bounding_box(triangle):

    xmin = int(np.floor(np.min(triangle[:,0])))
    xmax = int(np.ceil(np.max(triangle[:,0])))

    ymin = int(np.floor(np.min(triangle[:,1])))
    ymax = int(np.ceil(np.max(triangle[:,1])))

    return xmin, xmax, ymin, ymax