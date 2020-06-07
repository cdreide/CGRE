import sys
sys.path.append("../..")
from pathlib import Path
from optparse import OptionParser

from dataset.styleCrawling.crawler import crawl
from dataset.creation.generate_html import generate_html
from dataset.creation.render_html import render_html
from evaluation.add_boxes import add_boxes

def main() -> None:
    parser = OptionParser()
    parser.add_option( '-i',
                    '--in',
                    dest = 'in_path')
    parser.add_option( '-o',
                    '--out',
                    dest = 'out_path')
    parser.add_option( '-t',
                    '--top',
                    dest = 'top_values',
                    default = 1)
    parser.add_option( '-b',
                    '--boxes',
                    dest = 'add_boxes',
                    action = 'store_true',
                    default = False)
    (options, _) = parser.parse_args()

    try:
        crawl_urls: Path = Path(options.in_path)
    except:
        print('Please provide an input url file! (-i)')
        return

    try:
        out_path: Path = Path(options.out_path)
    except:
        print('Please provide an output path! (-o)')
        return


    crawl_results: str = str(out_path.joinpath('crawl.json').absolute())
    html_results: str = str(out_path.joinpath('html').absolute())
    render_results: str = str(out_path.joinpath('dataset').absolute())

    crawl(crawl_urls, crawl_results)
    generate_html(crawl_results, int(options.top_values), html_results)
    render_html(html_results, render_results)
    if options.add_boxes:
        boxes_results: Path = out_path.joinpath('dataset_boxes')
        add_boxes(render_results, render_results, boxes_results)

if __name__ == '__main__':
    main()
