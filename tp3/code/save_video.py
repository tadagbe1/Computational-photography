

import imageio
import os


def save_video(frames_folder, outpath):
    frames = []

    for i in range(100):
        path = os.path.join(frames_folder, f"frame_{i:05d}.png")
        frames.append(imageio.imread(path))

    imageio.mimsave(outpath, frames, fps=25)

if __name__ == '__main__':
    frames_folder = '../frames_vianney_tadagbe'
    outpath = '../video/morph_vianney_tadagbe.mp4'
    save_video(frames_folder, outpath)