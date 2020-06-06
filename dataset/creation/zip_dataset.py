# Small helper script to zip the dataset if wanted and OS independent.
import os
import zipfile

with zipfile.ZipFile("%s.zip" % ('dataset'), "w", zipfile.ZIP_DEFLATED) as zf:
    abs_in = os.path.abspath('dataset')
    for dirname, subdirs, files in os.walk('dataset'):
        for filename in files:
            absname = os.path.abspath(os.path.join(dirname, filename))
            arcname = absname[len(abs_in) + 1:]
            print('zipping ' + arcname)
            zf.write(absname, arcname)
