from optparse import OptionParser
from requests_html import HTMLSession
from pathlib import Path
import json
import re
import pprint

def main() -> None:
    parser = OptionParser()
    parser.add_option( '-i',
                    '--in',
                    dest = 'in_path',
                    metavar = 'FILE' )
    parser.add_option( '-o',
                '--out',
                dest = 'out_path',
                metavar = 'FILE' )
    (options, args) = parser.parse_args()

    crawl(options.in_path, options.out_path)


def crawl(in_path: str, out_path: str) -> None:

    if '.' not in out_path:
        Path(out_path).mkdir(parents=True, exist_ok=True)
    else:
        Path(out_path).parent.mkdir(parents=True, exist_ok=True)

    urls: [str] = []
    pre: str = 'http://'
    with open(in_path, 'r') as f:
        for url in f:
            if not pre in url:
                url = pre + url
            urls.append((url).replace('\n', '').lower())

    # print(urls)
    results = []
    for url in urls:
        print('Loading: ' + url)

        retrieve_style = """
            async () => {
                const sleep = (ms) => {
                    return new Promise(resolve => setTimeout(resolve, ms));
                }

                const renderedfont = (ele) => {
                    var getDefaultFonts = function () {
                        var iframe = document.createElement('iframe');
                        var html = '<html><body>';
                        var fonts;
                        document.body.appendChild(iframe);
                        iframe.contentWindow.document.open();
                        iframe.contentWindow.document.write(html);
                        var subele = iframe.contentWindow.document.createElement(ele.tagName);
                        iframe.contentWindow.document.body.appendChild(subele);
                        fonts = getComputedStyle(subele)['font-family'];
                        document.body.removeChild(iframe);
                        return fonts;
                    }
                    var fonts = getComputedStyle(ele)['font-family'] + ',' + getDefaultFonts();
                    var fontsArray = fonts.split(',');
                    var canvas = document.createElement('canvas');
                    var ctx = canvas.getContext("2d");
                    var testString = "abcdefghijklmnopqrstuvwxyz!@#$%^&*()ñ";
                    var prevImageData;
                    document.body.appendChild(canvas);
                    canvas.width = 500;
                    canvas.height = 300;
                    fontsArray.unshift('"Font That Doesnt Exists ' + Math.random() + '"');

                    for (var i = 0; i < fontsArray.length; i++) {
                        var fontName = fontsArray[i].trim();
                        ctx.clearRect(0, 0, canvas.width, canvas.height);
                        ctx.font = '16px ' + fontName + ', monospace';
                        ctx.fillText(testString, 10, 100);
                        var idata = ctx.getImageData(0, 0, canvas.width, canvas.height); 
                        var data = idata.data
                        if (prevImageData) {
                            for (var j = 0; j < data.length; j += 3) {
                                if (prevImageData[j + 3] !== data[j + 3]) {
                                    document.body.removeChild(canvas);
                                    return fontName;
                                }
                            }
                        }
                        prevImageData = data;
                    }

                    document.body.removeChild(canvas);
                    return 'monospace';
                }

                const getOccurences = (list) => {
                    return list.reduce((accumulator, currentValue) => {
                        !accumulator[currentValue] ? accumulator[currentValue] = 1 : accumulator[currentValue]++
                    return accumulator
                    }, {})
                }

                const crawl = () => {
                    let font_family_list = [];
                    let font_size_list = [];
                    let font_style_list = [];
                    let font_weight_list = [];
                    let text_decoration_line_list = [];
                    let font_color_list = [];
                    let background_color_list = [];
                    let total = 0;
                    let all = document.getElementsByTagName("*");

                    let max = all.length;
                    for (var i=0; i < max; i++) {
                        if (all[i].textContent.length > 0) {
                            font_family_list.push(renderedfont(all[i]));
                            font_size_list.push(window.getComputedStyle(all[i]).getPropertyValue("font-size"));
                            font_style_list.push(window.getComputedStyle(all[i]).getPropertyValue("font-style"));
                            font_weight_list.push(window.getComputedStyle(all[i]).getPropertyValue("font-weight"));
                            text_decoration_line_list.push(window.getComputedStyle(all[i]).getPropertyValue("text-decoration-line"));
                            font_color_list.push(window.getComputedStyle(all[i]).getPropertyValue("color"));
                            background_color_list.push(window.getComputedStyle(all[i]).getPropertyValue("background"));
                            total++;
                        }
                    }
                    return {
                        font_family: getOccurences(font_family_list),
                        font_size: getOccurences(font_size_list),
                        font_style: getOccurences(font_style_list),
                        font_weight: getOccurences(font_weight_list),
                        text_decoration_line: getOccurences(text_decoration_line_list),
                        font_color: getOccurences(font_color_list),
                        background_color: getOccurences(background_color_list),
                        status: 'success',
                        total: total
                    }
                }

                await sleep(1000);

                return crawl();
            }
        """

        try:
            session = HTMLSession()
            r = session.get(url)
            # def render(self, 
            # retries: int = 8, 
            # script: str = None, 
            # wait: float = 0.2, 
            # scrolldown=False, 
            # sleep: int = 0, 
            # reload: bool = True, 
            # timeout: Union[float, int] = 8.0, 
            # keep_page: bool = False, 
            # cookies: list = [{}], 
            # send_cookies_session: bool = False):
            res = r.html.render(script = retrieve_style, retries = 5, timeout = 10.0)
        except Exception as e:
            print(e)
            res = {'status': 'fail'}

        # session = HTMLSession()
        # r = session.get(url)
        # res = r.html.render(script=retrieve_style)
        res['url'] = url
        results.append(res)
        # pprint.pprint(res, width=1)


    with open(str(Path(out_path).parent.joinpath('crawl_raw.json')), 'w') as f:
        f.write(json.dumps(results, indent=4))
        f.write('\n')

    # Processing
    failed: [str] = []
    succeeded: [str] = []
    font_family_dict: [str] = {}
    font_size_dict: [str] = {}
    font_style_dict: [str] = {}
    font_weight_dict: [str] = {}
    text_decoration_line_dict: [str] = {}
    font_color_dict: [str] = {}
    background_color_dict: [str] = {}

    rgba_reg = r'rgba\(\d*, \d*, \d*, [\d\.]*\)'
    rgb_reg = r'rgb\(\d*, \d*, \d*\)'

    for page in results:
        tmp_font_family_dict: [str] = {}
        tmp_font_size_dict: [str] = {}
        tmp_font_style_dict: [str] = {}
        tmp_font_weight_dict: [str] = {}
        tmp_text_decoration_line_dict: [str] = {}
        tmp_font_color_dict: [str] = {}
        tmp_background_color_dict: [str] = {}
        
        if page['status'] == 'fail':
            failed.append(page['url'])
            continue

        total: float = float(page['total'])
        succeeded.append(page['url'])


        for font_family in page['font_family']:
            font_family_clean: str = font_family.split(', ')[0]
            font_family_clean = font_family_clean.replace('\"', '').lower()

            add_to_dict(tmp_font_family_dict, font_family_clean, page['font_family'][font_family])

        for font_size in page['font_size']:
            font_size_clean: str = font_size.lower()

            add_to_dict(tmp_font_size_dict, font_size_clean, page['font_size'][font_size])

        for font_style in page['font_style']:

            font_style_clean: str = font_style.lower()
            
            add_to_dict(tmp_font_style_dict, font_style_clean, page['font_style'][font_style])

        for font_weight in page['font_weight']:

            font_weight_clean: str = font_weight.lower()

            add_to_dict(tmp_font_weight_dict, font_weight_clean, page['font_weight'][font_weight])

        for text_decoration_line in page['text_decoration_line']:
            text_decoration_line_clean: str = text_decoration_line.lower()

            add_to_dict(tmp_text_decoration_line_dict, text_decoration_line_clean, page['text_decoration_line'][text_decoration_line])

        for font_color in page['font_color']:

            font_color_clean: str = font_color.lower()

            add_to_dict(tmp_font_color_dict, font_color_clean, page['font_color'][font_color])

        for background_color in page['background_color']:

            found: [str] = re.findall(rgba_reg, background_color.lower())
            found += re.findall(rgb_reg, background_color.lower())
            
            if len(found) <= 0:
                continue

            background_color_clean: str = found[0].lower()

            add_to_dict(tmp_background_color_dict, background_color_clean, page['background_color'][background_color])


        tmp_font_family_dict_total: float = float(sum(list(tmp_font_family_dict.values())))
        tmp_font_size_dict_total: float = float(sum(list(tmp_font_size_dict.values())))
        tmp_font_style_dict_total: float = float(sum(list(tmp_font_style_dict.values())))
        tmp_font_weight_dict_total: float = float(sum(list(tmp_font_weight_dict.values())))
        tmp_text_decoration_line_dict_total: float = float(sum(list(tmp_text_decoration_line_dict.values())))
        tmp_font_color_dict_total: float = float(sum(list(tmp_font_color_dict.values())))
        tmp_background_color_dict_total: float = float(sum(list(tmp_background_color_dict.values())))

        tmp_font_family_dict = {k: v / tmp_font_family_dict_total for k, v in tmp_font_family_dict.items()}
        tmp_font_size_dict = {k: v / tmp_font_size_dict_total for k, v in tmp_font_size_dict.items()}
        tmp_font_style_dict = {k: v / tmp_font_style_dict_total for k, v in tmp_font_style_dict.items()}
        tmp_font_weight_dict = {k: v / tmp_font_weight_dict_total for k, v in tmp_font_weight_dict.items()}
        tmp_text_decoration_line_dict = {k: v / tmp_text_decoration_line_dict_total for k, v in tmp_text_decoration_line_dict.items()}
        tmp_font_color_dict = {k: v / tmp_font_color_dict_total for k, v in tmp_font_color_dict.items()}
        tmp_background_color_dict = {k: v / tmp_background_color_dict_total for k, v in tmp_background_color_dict.items()}

        font_family_dict = merge_dicts(font_family_dict, tmp_font_family_dict)
        font_size_dict = merge_dicts(font_size_dict, tmp_font_size_dict)
        font_style_dict = merge_dicts(font_style_dict, tmp_font_style_dict)
        font_weight_dict = merge_dicts(font_weight_dict, tmp_font_weight_dict)
        text_decoration_line_dict = merge_dicts(text_decoration_line_dict, tmp_text_decoration_line_dict)
        font_color_dict = merge_dicts(font_color_dict, tmp_font_color_dict)
        background_color_dict = merge_dicts(background_color_dict, tmp_background_color_dict)

    # Sort the data in descending order by occurences
    total: float = float(len(succeeded))
    font_family_dict = {k: v / total for k, v in sorted(font_family_dict.items(), key=lambda item: item[1], reverse=True)}
    font_size_dict = {k: v / total for k, v in sorted(font_size_dict.items(), key=lambda item: item[1], reverse=True)}
    font_style_dict = {k: v / total for k, v in sorted(font_style_dict.items(), key=lambda item: item[1], reverse=True)}
    font_weight_dict = {k: v / total for k, v in sorted(font_weight_dict.items(), key=lambda item: item[1], reverse=True)}
    text_decoration_line_dict = {k: v / total for k, v in sorted(text_decoration_line_dict.items(), key=lambda item: item[1], reverse=True)}
    font_color_dict = {k: v / total for k, v in sorted(font_color_dict.items(), key=lambda item: item[1], reverse=True)}
    background_color_dict = {k: v / total for k, v in sorted(background_color_dict.items(), key=lambda item: item[1], reverse=True)}

    log = {
        'succeeded': succeeded,
        'failed': failed,
        'font_family_dict': font_family_dict,
        'font_size_dict': font_size_dict,
        'font_style_dict': font_style_dict,
        'font_weight_dict': font_weight_dict,
        'text_decoration_line_dict': text_decoration_line_dict,
        'font_color_dict': font_color_dict,
        'background_color_dict': background_color_dict
        }


    # print(font_color_dict)

    with open('/home/christopher/Git/OCROnWebpages/results/crawl.json', 'w') as f:
        f.write(json.dumps(log, indent=4))
        f.write('\n')

    print('Done!')




def add_to_dict(dic, key, value) -> None:
    if key not in dic:
        dic[key] = value
    else:
        dic[key] += value

def merge_dicts(total_dict, new_dict) -> dict:
    for key in new_dict.keys():
        if key not in total_dict.keys():
            total_dict[key] = new_dict[key]
        else:
            total_dict[key] += new_dict[key]

    return total_dict

if __name__ == '__main__':
    main()
