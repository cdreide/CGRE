import time
from pathlib import Path
import re
import subprocess

root = Path().absolute()
load = '/dataset/'
load_root = str(root) + load
save = '/dataset_Tesseract_Determiner/'

files = []

for path in Path(load_root).rglob('*.png'):
    files.append(path)

oem = 1
psm = 3

start_whole = time.time()

for p in files:
  print('load: ' + str(p))
  start = time.time()

  texts: [str] = []

  all_coordinates: [[int]] = []
  with open(str(p).replace('.png', '.txt'), 'r') as f:
    next(f)
    for l in f:
      coordinate_tuple_list: [int] = []
      coordinates = re.search(r'([0-9.]+),([0-9.]+),([0-9.]+),([0-9.]+)', l).groups()
      for coordinate in coordinates:
        coordinate_tuple_list.append(int(float(coordinate)))
      coordinate_tuple = tuple(coordinate_tuple_list)
      all_coordinates.append(coordinate_tuple)
      print(coordinate_tuple)
      (left, top, width, height) = coordinate_tuple 
      text: str = ''
      subprocess.call(['./tesseract_determiner/build/tesseract_determiner', str(p), str(left), str(top), str(width), str(height)])
      texts.append(text)

  save_path = str(p).replace(load, save)
  Path(save_path).parent.mkdir(parents=True, exist_ok=True)
  
  with open(save_path.replace('.png', '.txt'), 'w') as f:
    for i in range(len(texts)):
      (left, top, width, height) = all_coordinates[i] 
      f.write(texts[i] + '\ţ' + str(left) + str(top) + str(width) + str(height) + '\n')
  print('save: ' + str(save_path.replace('.png', '.txt')))

  end = time.time()
  print('save: ' + str(save_path), end - start)

end_whole = time.time()
print('Whole:', end_whole - start_whole)
