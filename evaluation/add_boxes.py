import argparse
import time
from pathlib import Path
import re
import os
import cv2
import matplotlib.pyplot as plt
import progressbar

prints: bool = False

def main() -> None:
    parser = argparse.ArgumentParser(description='Evaluate the recognized dataset against the ideal dataset.')
    # Ideal Directory
    parser.add_argument('input', metavar='input', type=str, nargs=1, help='a directories containing the ideal dataset')
    # Recognized Directory
    parser.add_argument('output', metavar='output', type=str, nargs=1, help='a directories containing the recognized dataset')

    args = parser.parse_args()

    # INPUT FEEDBACK
    # Paths
    input_path: Path = Path(args.input[0]).absolute()
    output_path: Path = Path(args.output[0]).absolute()

    root: Path = Path().absolute()
    load_root = root.joinpath(input_path)
    print(str(load_root))

    files = []

    for path in Path(load_root).rglob('*.png'):
        files.append(path)

    start_whole = time.time()

    for i in progressbar.progressbar(range(len(files))):
        p = files[i]
        if prints: print('load: ' + str(p))
        start = time.time()

        all_coordinates: [[int]] = []
        with open(str(p).replace('.png', '.txt'), 'r') as f:
            next(f)
            for l in f:
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

        save_path = str(p).replace(str(input_path), str(output_path))
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        plt.imsave(save_path, img)
        end = time.time()
        if prints: print('save: ' + str(save_path), end - start)

    end_whole = time.time()
    print('Whole:', end_whole - start_whole)

if __name__ == '__main__':
    main()
