import numpy as np
import progressbar
import codecs
import re
from pathlib import Path

def main():

    dataset_path = str(Path('./dataset').resolve())

    # Extract Data
    print('Extract Data:')
    data = extract_data(dataset_path)
    # print(data)
    # Create CSV
    print('Convert Data:')
    to_csv(dataset_path, data)


def to_csv(dataset_path, data):
    width = 1100.0
    height = 800.0

    csv_string: str = 'filepath,x1,y1,x2,y2,class_name\n'
    for i in progressbar.progressbar(range(len(data))):
        img = data[i]

        filename = img[0]

        iter_boxes = iter(img)
        next(iter_boxes)
        for box in iter_boxes:
            csv_string += filename
            csv_string += ','
            csv_string += str(box[0]/width)
            csv_string += ','
            csv_string += str(box[1]/height)
            csv_string += ','
            csv_string += str(box[2]/width)
            csv_string += ','
            csv_string += str(box[3]/height)
            csv_string += ','
            csv_string += 'text'
            csv_string += '\n'

    with codecs.open('./labels.csv', 'w', "utf-8") as f:
        f.write(csv_string)

def extract_data(dataset_path):

    files = []
    for path in Path(dataset_path).rglob('*.png'):
        files.append(path)

    all_coordinates = []
    for i in progressbar.progressbar(range(len(files))):
        # if i > 10: break

        p = files[i]
        name = [str(p)]

        # Retrieve Coordinates
        boxes = name + extract_boxes(p)

        # Save Filename & Coordinates
        all_coordinates.append(boxes)

    data = np.asarray(all_coordinates)
    return data


def extract_boxes(filename):
    boxes = []
    with open(str(filename).replace('.png', '.txt'), 'r') as f:
        next(f) # skip file name line
        for l in f:
            box = []
            coordinates = re.search(r'([0-9]+),([0-9]+),([0-9]+),([0-9]+)', l).groups()
            for coordinate in coordinates:
                box.append(int(float(coordinate)))
            boxes.append(box)
    return boxes


if __name__ == '__main__':
    main()
