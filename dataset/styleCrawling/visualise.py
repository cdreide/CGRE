from optparse import OptionParser
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import json

out_path: str = "visualisations/"
def main():
    parser = OptionParser()
    parser.add_option( '-i',
                    '--input',
                    dest = 'input',
                    metavar = 'FILE' )
    parser.add_option( '-o',
                    '--output',
                    dest = 'output',
                    metavar = 'FOLDER' )
    (options, _) = parser.parse_args()

    in_path = str(Path(options.input))
    out_path = str(Path(options.output))

    visualise(in_path, out_path)

def visualise(in_path, out_path):
    with open(in_path, 'r') as f:
        log = json.load(f)

    for dic in log.keys():
        if dic == 'succeeded' or dic == 'failed':
            continue

        # BAR
        plt.barh(list(log[dic].keys())[:10], list(log[dic].values())[:10], color='b')

        plt.title(dic)
        plt.xlabel('Occurences')
        plt.ylabel('Type')

        plt.tight_layout()

        save_path: str = str(Path(out_path).joinpath('bar').joinpath(dic)) + '.pdf'
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, bbox_inches='tight')

        plt.clf()

        # PIE
        # plt.pie(labels=list(log[dic].keys())[:10], x=list(log[dic].values())[:10])
        plt.pie(labels=list(log[dic].keys()), x=list(log[dic].values()))

        plt.title(dic)

        plt.tight_layout()

        save_path: str = str(Path(out_path).joinpath('pie').joinpath(dic)) + '.pdf'
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, bbox_inches='tight')
        plt.clf()
        # plt.show()


if __name__ == '__main__':
    main()
