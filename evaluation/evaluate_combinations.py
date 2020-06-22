from evaluation import evaluate
from pathlib import Path
import argparse

def main() -> None:
    parser = argparse.ArgumentParser(description='Evaluate the recognized dataset against the ideal dataset.')
    # Ideal Directory
    parser.add_argument('ideal', metavar='ideal', type=str, nargs=1, help='a directories containing the ideal dataset')
    # Recognized Directory
    parser.add_argument('recognized', metavar='recognized', type=str, nargs=1, help='a directories containing the recognized dataset')
    # Output Directory
    parser.add_argument('-o', metavar='output', type=str, nargs=1, help='A path where the results can be saved.')
    args = parser.parse_args()

    ideal_path: str = Path(args.ideal[0]).absolute()
    recognized_path: str = Path(args.recognized[0]).absolute()
    out_path: str = Path(args.o[0]).absolute()

    cps: [float] = [0.5, 0.6, 0.7, 0.8, 0.9]
    lps: [float] = [0.5, 0.6, 0.7, 0.8, 0.9]

    print('This script will evaluate ' + str(len(cps) * len(lps)) + ' times.')
    print('(for:')
    print('cps: ' + str(cps))
    print('lps: ' + str(lps))
    print(')')

    for cp in cps:
        for lp in lps:
            evaluate(ideal_path, recognized_path, out_path, cp, lp)

if __name__ == '__main__':
    main()
