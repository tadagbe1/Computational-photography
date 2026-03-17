# Tout generer par IA

import matplotlib
from skimage import io
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import numpy as np

from scipy.spatial import Delaunay


def save_triangulation_image(image_path, points_path, output_path):

    # charger l'image
    image = io.imread(image_path)

    # charger les points
    points = np.loadtxt(points_path)

    # triangulation de Delaunay
    tri = Delaunay(points)

    # créer la figure
    plt.figure()
    plt.imshow(image)

    # dessiner triangles
    plt.triplot(points[:,0], points[:,1], tri.simplices, color="yellow", linewidth=0.8)

    # dessiner points
    plt.scatter(points[:,0], points[:,1], c="red", s=10)

    plt.axis("off")

    # sauvegarder
    plt.savefig(output_path, bbox_inches="tight", pad_inches=0)

    plt.close()


def show_image(image, title=None):
    plt.figure()
    plt.imshow(image)
    if title is not None:
        plt.title(title)
    plt.axis("off")
    plt.show()


def show_points(image, points):
    plt.figure()
    plt.imshow(image)
    plt.scatter(points[:, 0], points[:, 1], c="red", s=20)
    plt.axis("off")
    plt.show()


def show_triangulation(image, points, tri):
    plt.figure()
    plt.imshow(image)
    plt.triplot(points[:, 0], points[:, 1], tri.simplices, color="yellow", linewidth=0.8)
    plt.scatter(points[:, 0], points[:, 1], c="red", s=10)
    plt.axis("off")
    plt.show()


def show_triangle(image, triangle):
    plt.figure()
    plt.imshow(image)

    polygon = Polygon(triangle, closed=True, fill=False, edgecolor="yellow", linewidth=2)
    plt.gca().add_patch(polygon)

    plt.scatter(triangle[:, 0], triangle[:, 1], c="red", s=30)
    plt.axis("off")
    plt.show()

def show_image_with_points(image_path, points_path):
    image = io.imread(image_path)
    points = np.loadtxt(points_path)

    show_points(image, points)

if __name__ == '__main__':
    img_noir_path = '../web/images/noir.jpg'
    pts_noir_path = '../web/points/noir.txt'
    out_path = "../web/images/triangulation_noir.jpg"
    show_image_with_points(img_noir_path, pts_noir_path)
    save_triangulation_image(
        img_noir_path, 
        pts_noir_path,
        out_path
    )

    # img_tadagbe_path = '../web/images/tadagbe.jpg'
    # pts_tadagbe_path = '../web/points/tadagbe.txt'
    # out_path_tadagbe = "../web/images/triangulation_tadagbe.jpg"
    # show_image_with_points(img_tadagbe_path, pts_tadagbe_path)
    # save_triangulation_image(
    #     img_tadagbe_path, 
    #     pts_tadagbe_path,
    #     out_path_tadagbe
    # )

    # img_vianney_path = '../web/images/vianney.jpg'
    # pts_vianney_path = '../web/points/vianney.txt'
    # out_path_vianney = "../web/images/triangulation_vianney.jpg"
    # show_image_with_points(img_vianney_path, pts_vianney_path)
    # save_triangulation_image(
    #     img_vianney_path, 
    #     pts_vianney_path,
    #     out_path_vianney
    # )

    # img_tadagbe_path = '../web/images/tadagbe.jpg'
    # pts_tadagbe_path = '../web/points/tadagbe.txt'
    # out_path_tadagbe = "../web/images/triangulation_tadagbe.jpg"
    # show_image_with_points(img_tadagbe_path, pts_tadagbe_path)
    # save_triangulation_image(
    #     img_tadagbe_path, 
    #     pts_tadagbe_path,
    #     out_path_tadagbe
    # )

    # img_vianney_path = '../web/images/vianney.jpg'
    # pts_vianney_path = '../web/points/vianney.txt'
    # out_path_vianney = "../web/images/triangulation_vianney.jpg"
    # show_image_with_points(img_vianney_path, pts_vianney_path)
    # save_triangulation_image(
    #     img_vianney_path, 
    #     pts_vianney_path,
    #     out_path_vianney
    # )


