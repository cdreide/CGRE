# Small helper script to zip the dataset if wanted and OS independent.
from pathlib import Path
import os
import zipfile
from optparse import OptionParser


def main() -> None:
    parser = OptionParser()
    parser.add_option( '-i',
                    '--in',
                    dest = 'in_path')
    (options, _) = parser.parse_args()

    in_path: str = str(Path(options.in_path).absolute())

    create_zip(in_path)

def create_zip(in_path: str):
    with zipfile.ZipFile(in_path + '.zip', "w", zipfile.ZIP_DEFLATED) as zf:
        for dirname, _, files in os.walk(in_path):
            for filename in files:
                absname: str = str(Path(dirname).joinpath(filename).absolute())
                arcname: str = absname[len(in_path) + 1:]
                # print('zipping ' + arcname)
                zf.write(absname, arcname)


if __name__ == '__main__':
    main()
