import visualization
import io_utils
import matplotlib.pyplot as plt
import morph

from scipy.spatial import Delaunay
import numpy as np


def add_boundary_points(pts, h, w):
    # Add the whole image not only the the point of interest
    boundary_points = np.array([
        [0, 0],
        [w // 2, 0],
        [w - 1, 0],
        [0, h // 2],
        [w - 1, h // 2],
        [0, h - 1],
        [w // 2, h - 1],
        [w - 1, h - 1]
    ], dtype=np.float64)

    return np.vstack([pts, boundary_points])


def main(img1_path, img2_path, pt1_path, pt2_path):

    img1 = io_utils.load_image(img1_path)
    img2 = io_utils.load_image(img2_path)

    pts1 = io_utils.load_points(pt1_path)
    pts2 = io_utils.load_points(pt2_path)

    h, w = img1.shape[:2]

    pts1 = add_boundary_points(pts1, h, w)
    pts2 = add_boundary_points(pts2, h, w)

    avg_pts = 0.5 * (pts1 + pts2)

    tri = Delaunay(avg_pts)

    generate_morph_sequence(
        img1,
        img2,
        pts1,
        pts2,
        tri,
        n_frames=100,
        output_dir="../frames_vianney_tadagbe"
    )


def generate_morph_sequence(img1, img2, pts1, pts2, tri, n_frames, output_dir):

    io_utils.create_directory(output_dir)

    for i in range(n_frames):
        t = i / (n_frames - 1)

        frame = morph.morph(
            img1,
            img2,
            pts1,
            pts2,
            tri,
            warp_frac=t,
            dissolve_frac=t
        )

        io_utils.save_image(f"{output_dir}/frame_{i:05d}.png", frame)


if __name__ == "__main__":    

    img1_path = '../web/images/vianney.jpg'
    img2_path = '../web/images/tadagbe.jpg'

    pt1_path = '../web/points/vianney.txt'
    pt2_path = '../web/points/tadagbe.txt'

    main(img1_path, img2_path, pt1_path, pt2_path)