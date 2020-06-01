import numpy as np
import matplotlib.pyplot as plt
import json
from pathlib import Path

out_path: str = "visualisations/"
Path(out_path).mkdir(parents=True, exist_ok=True)

with open('log_clean_example', 'r') as f:
    log = json.load(f)

for dic in log.keys():
    if dic == 'succeeded' or dic == 'failed':
        continue

    plt.barh(list(log[dic].keys())[:10], list(log[dic].values())[:10], color='b')

    plt.title(dic)
    plt.xlabel('Occurences')
    plt.ylabel('Type')

    plt.tight_layout()

    plt.savefig(out_path + dic + '.pdf', bbox_inches='tight')

    plt.clf()
    # plt.show()
