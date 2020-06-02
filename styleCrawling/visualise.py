import numpy as np
import matplotlib.pyplot as plt
import json
from pathlib import Path

out_path: str = "visualisations/"

with open('log_clean_example.json', 'r') as f:
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

    save_path: str = out_path + 'bar/' + dic + '.pdf'
    Path(save_path).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(save_path, bbox_inches='tight')

    plt.clf()

    # PIE
    # plt.pie(labels=list(log[dic].keys())[:10], x=list(log[dic].values())[:10])
    plt.pie(labels=list(log[dic].keys()), x=list(log[dic].values()))

    plt.title(dic)
    

    plt.tight_layout()

    save_path: str = out_path + 'pie/' + dic + '.pdf'
    Path(save_path).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(save_path, bbox_inches='tight')
    plt.clf()
    # plt.show()
