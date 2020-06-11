from pathlib import Path
import sys
path: Path = Path(__file__).parent.absolute()
sys.path.append(str(path.joinpath("../..")))
from optparse import OptionParser

from dataset.styleCrawling.crawler import crawl
from dataset.creation.generate_html import generate_html
from dataset.creation.render_html import render_html
from evaluation.add_boxes import add_boxes
from dataset.styleCrawling.visualise import visualise
from dataset.creation.zip_dataset import create_zip

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
    parser.add_option( '-v',
                    '--visualise',
                    dest = 'visualise',
                    action = 'store_true',
                    default = False)
    parser.add_option( '-z',
                    '--zip',
                    dest = 'create_zip',
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

    print('Crawling...')
    # crawl(crawl_urls, crawl_results)
    print('Generating HTML...')
    generate_html(crawl_results, int(options.top_values), html_results)
    print('Rendering HTML...')
    try:
        render_html(html_results, render_results)
    except Exception as e:
        print(e)
    if options.add_boxes:
        print('Adding Boxes...')
        boxes_results: Path = out_path.joinpath('dataset_boxes')
        add_boxes(render_results, render_results, boxes_results)
    if options.visualise:
        print('Visualising Crawl Data...')
        visualise_results: Path = out_path.joinpath('visualise')
        visualise(crawl_results, visualise_results)
    if options.create_zip:
        print('Zipping Dataset...')
        create_zip(out_path)


if __name__ == '__main__':
    main()
