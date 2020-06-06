import argparse
import time
from pathlib import Path
import re
import os
import cv2
import matplotlib.pyplot as plt
import progressbar

def main() -> None:
    parser = argparse.ArgumentParser(description='Add bounding boxes to image.')
    # Ideal Directory
    parser.add_argument('input_img', metavar='input_img', type=str, nargs=1, help='a directory containing the images')
    # Label Directory
    parser.add_argument('input_txt', metavar='input_txt', type=str, nargs=1, help='a directory containing the labels')
    # Output Directory
    parser.add_argument('output', metavar='output', type=str, nargs=1, help='a directory for the output')

    args = parser.parse_args()

    add_boxes(args.input_img[0], args.input_txt[0], args.output[0])


def add_boxes(in_imgs: str, in_txts: str, out: str):
    # INPUT FEEDBACK
    # Paths
    input_img_path: Path = Path(in_imgs).absolute()
    input_txt_path: Path = Path(in_txts).absolute()
    output_path: Path = Path(out).absolute()

    root: Path = Path().absolute()
    load_root = root.joinpath(input_img_path)
    print(str(load_root))

    files = []

    for path in Path(load_root).rglob('*.png'):
        files.append(path)

    start_whole = time.time()

    for i in progressbar.progressbar(range(len(files))):
        p = files[i]
        start = time.time()

        all_coordinates: [[int]] = []

        txt_path: str = (str(p).replace(str(input_img_path), str(input_txt_path))).replace('.png', '.txt')
        with open(txt_path, 'r') as f:
            for l in f:
                if 'file://' in l:
                    continue
                coordinate_tuple: [int] = []
                coordinates = re.search(r'([0-9]+),([0-9]+),([0-9]+),([0-9]+)', l).groups()
                for coordinate in coordinates:
                    coordinate_tuple.append(int(float(coordinate)))
                all_coordinates.append(tuple(coordinate_tuple))
        #print(all_coordinates)

        img = cv2.imread(str(p))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        for coordinate_tuple in all_coordinates:
            (left, top, width, height) = coordinate_tuple 
            cv2.rectangle(img, (left, top), (left + width, top + height), (0, 255, 0), 2)

        save_path = str(p).replace(str(input_img_path), str(output_path))
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        plt.imsave(save_path, img)
        end = time.time()

    end_whole = time.time()
    print('Whole:', end_whole - start_whole)

if __name__ == '__main__':
    main()
