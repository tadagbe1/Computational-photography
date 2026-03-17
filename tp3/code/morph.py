from matplotlib.path import Path
import geometry
import numpy as np
from scipy.interpolate import RectBivariateSpline


def morph(img1, img2, img1_pts, img2_pts, tri, warp_frac, dissolve_frac):

    inter_points = geometry.compute_intermediate_points(img1_pts, img2_pts, warp_frac)
    result_img = np.zeros_like(img1, dtype=np.float64)
    for triangle_indices in tri.simplices:
        process_triangle(img1, img2, result_img, img1_pts, img2_pts, inter_points, triangle_indices, dissolve_frac)

    return np.clip(result_img, 0, 1)


def process_triangle(img1, img2, result_img, pts1, pts2, inter_pts, triangle_indices, dissolve_frac):
    # Get the original images and the intermediate one triangle vertices
    tri1 = geometry.get_triangle_vertices(pts1, triangle_indices)
    tri2 = geometry.get_triangle_vertices(pts2, triangle_indices)
    tri_mid = geometry.get_triangle_vertices(inter_pts, triangle_indices)

    # get the inside corrdinate of the intermediate image
    inside_pixels = get_pixels_in_triangle(tri_mid)

    # get the transformation matrixes from intermediate triangle to the original triangles
    M1 = geometry.compute_affine_matrix(tri_mid, tri1)
    M2 = geometry.compute_affine_matrix(tri_mid, tri2)

    # apply the trasformation to the inside pixeel of the triangle
    inside_to_src1 = geometry.apply_affine_transform(M1, inside_pixels)
    inside_to_src2 = geometry.apply_affine_transform(M2, inside_pixels)

    colors1 = interpolate_colors(img1, inside_to_src1)
    colors2 = interpolate_colors(img2, inside_to_src2)

    # blend the colors
    blended = blend_colors(colors1, colors2, dissolve_frac)

    # write the resulting image
    xs = inside_pixels[:, 0].astype(int)
    ys = inside_pixels[:, 1].astype(int)
    result_img[ys, xs] = blended

def get_pixels_in_triangle(triangle):
    # Get the bbox to reduce the search space
    bbox = geometry.compute_bounding_box(triangle)
    xmin, xmax, ymin, ymax = bbox
    xs = np.arange(xmin, xmax + 1)
    ys = np.arange(ymin, ymax + 1)

    X, Y = np.meshgrid(xs, ys)
    points = np.vstack((X.ravel(), Y.ravel())).T
    path = Path(triangle)
    mask = path.contains_points(points)
    inside_points = points[mask]

    return inside_points

def blend_colors(color1, color2, dissolve_frac):
    return (1 - dissolve_frac)*color1 + dissolve_frac*color2

def interpolate_colors(image, points):
    h, w, c = image.shape

    xs = points[:, 0]
    ys = points[:, 1]

    x_grid = np.arange(w)
    y_grid = np.arange(h)

    colors = np.zeros((points.shape[0], c), dtype=np.float64) # colors for each point

    for channel in range(c):
        spline = RectBivariateSpline(y_grid, x_grid, image[:, :, channel])
        colors[:, channel] = spline.ev(ys, xs)

    return colors
