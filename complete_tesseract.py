import time
from pathlib import Path
import re
import pytesseract
from pytesseract import Output
import cv2
import matplotlib.pyplot as plt

root = Path().absolute()
load = '/dataset/'
load_root = str(root) + load
save = '/dataset_Tesseract_Complete/'

files = []

for path in Path(load_root).rglob('*.png'):
    files.append(path)

oem = 1
psm = 3

start_whole = time.time()

for p in files:
  print('load: ' + str(p))
  start = time.time()

  mapping_content: str = ''

  img = cv2.imread(str(p))
  img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

  d = pytesseract.image_to_data(img, output_type=Output.DICT, config='--oem ' + str(oem) + '--psm ' + str(psm))
  n_boxes = len(d['level'])
  for i in range(n_boxes):
    text = re.search(r'^[a-zA-Z0-9]+', d['text'][i])
    if(text):
      (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])

      text = text.group()
      mapping_content += text + '\t(' + str(x) + ',' + str(y) + ',' + str(w) + ',' + str(h) + ')\n'
      
      cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

  save_path = str(p).replace(load, save)
  Path(save_path).parent.mkdir(parents=True, exist_ok=True)
  plt.imsave(save_path, img)
  
  with open(save_path.replace('.png', '.txt'), 'w') as f:
    f.write(mapping_content)
  print('save: ' + str(save_path.replace('.png', '.txt')))

  end = time.time()
  print('save: ' + str(save_path), end - start)

end_whole = time.time()
print('Whole:', end_whole - start_whole)
