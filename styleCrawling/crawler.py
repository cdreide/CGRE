from requests_html import HTMLSession
import json
import re
import pprint

pre: str = 'http://'
urls: [str] = []

with open('resources/urls_us', 'r') as f:
    for url in f:
        if not pre in url:
            url = pre + url
        urls.append((url).replace('\n', '').lower())
# print(urls)
results = []
for url in urls:
    print('Loading: ' + url)

    retrieve_style = """
        () => {
            let font_family_list = [];
            let font_size_list = [];
            let font_style_list = [];
            let font_color_list = [];
            let background_color_list = [];
            let total = 0;
            let all = document.getElementsByTagName("*");

            let max = all.length;
            for (var i=0; i < max; i++) {
                if (all[i].textContent.length > 0) {
                    font_family_list.push(window.getComputedStyle(all[i]).getPropertyValue("font-family"));
                    font_size_list.push(window.getComputedStyle(all[i]).getPropertyValue("font-size"));
                    font_style_list.push(window.getComputedStyle(all[i]).getPropertyValue("font-style"));
                    font_style_list.push(window.getComputedStyle(all[i]).getPropertyValue("font-weight"));
                    font_style_list.push(window.getComputedStyle(all[i]).getPropertyValue("text-decoration"));
                    font_color_list.push(window.getComputedStyle(all[i]).getPropertyValue("color"));
                    background_color_list.push(window.getComputedStyle(all[i]).getPropertyValue("background"));
                    total++;
                }
            }

            const getOccurences = (list) => {
                return list.reduce((accumulator, currentValue) => {
                    !accumulator[currentValue] ? accumulator[currentValue] = 1 : accumulator[currentValue]++
                return accumulator
                }, {})
            }

            return {
                font_family: getOccurences(font_family_list),
                font_size: getOccurences(font_size_list),
                font_style: getOccurences(font_style_list),
                font_color: getOccurences(font_color_list),
                background_color: getOccurences(background_color_list),
                status: 'success',
                total: total
            }
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
        res = r.html.render(script = retrieve_style, retries = 10, timeout = 15.0)
    except Exception as e:
        print(e)
        res = {'status': 'fail'}

    # session = HTMLSession()
    # r = session.get(url)
    # res = r.html.render(script=retrieve_style)
    res['url'] = url
    results.append(res)
    # pprint.pprint(res, width=1)


with open('log.json', 'w') as f:
    f.write(json.dumps(results, indent=4))
    f.write('\n')


# Processing
def merge_dicts(total_dict, new_dict):
    for key in new_dict.keys():
        if key not in total_dict.keys():
            total_dict[key] = new_dict[key]
        else:
            total_dict[key] += new_dict[key]

    return total_dict

failed: [str] = []
succeeded: [str] = []
font_family_dict: [str] = {}
font_size_dict: [str] = {}
font_style_dict: [str] = {}
font_color_dict: [str] = {}
background_color_dict: [str] = {}

rgba_reg = r'rgba\(\d*, \d*, \d*, [\d\.]*\)'
rgb_reg = r'rgb\(\d*, \d*, \d*\)'

for page in results:
    tmp_font_family_dict: [str] = {}
    tmp_font_size_dict: [str] = {}
    tmp_font_style_dict: [str] = {}
    tmp_font_color_dict: [str] = {}
    tmp_background_color_dict: [str] = {}
    
    if page['status'] == 'fail':
        failed.append(page['url'])
        continue

    total: float = float(page['total'])
    succeeded.append(page['url'])

    # print(page['url'])
    for font_family in page['font_family']:
        font = font_family.split(', ')[0]
        font = font.replace('\"', '').lower()
        if font not in tmp_font_family_dict:
            tmp_font_family_dict[font] = page['font_family'][font_family]
        else:
            tmp_font_family_dict[font] += page['font_family'][font_family]
    for font_size in page['font_size']:
        if font_size.lower() not in tmp_font_size_dict:
            tmp_font_size_dict[font_size.lower()] = page['font_size'][font_size]
        else:
            tmp_font_size_dict[font_size.lower()] += page['font_size'][font_size]
    for font_style in page['font_style']:

        # sometimes there is color in style:
        # found = re.findall(rgba_reg, font_style.lower())
        # found += re.findall(rgb_reg, font_style.lower())
        # for color in found:
        #     if color.lower() not in tmp_font_color_dict:
        #         tmp_font_color_dict[color.lower()] = page['font_style'][font_style]
        #     else:
        #         tmp_font_color_dict[color.lower()] += page['font_style'][font_style]

        font_style_clean = re.sub(rgba_reg, '', re.sub(rgb_reg, '', font_style)).lower()
        # font_style_clean = font_style.lower()
        if 'none' in font_style_clean or '400' in font_style_clean:
            font_style_clean = 'normal'
        if 'none' in font_style_clean:
            font_style_clean = 'normal'

        if font_style_clean not in tmp_font_style_dict:
            tmp_font_style_dict[font_style_clean] = page['font_style'][font_style]
        else:
            tmp_font_style_dict[font_style_clean] += page['font_style'][font_style]
    for font_color in page['font_color']:
        if 'rgba' in font_color and ', 0)' in font_color:
            font_color_clean = 'rgb(255, 255, 255)'
        else: 
            font_color_clean = font_color.lower()

        if font_color_clean not in tmp_font_color_dict:
            tmp_font_color_dict[font_color_clean] = page['font_color'][font_color]
        else:
            tmp_font_color_dict[font_color_clean] += page['font_color'][font_color]
    for background_color in page['background_color']:
        
        # TODO: wenn background image -> color nehmen oder ignorieren?
        # rgba_reg, re.sub('url\(.*\)', '', background_color)
        if 'url' in background_color:
            continue

        found = re.findall(rgba_reg, background_color.lower())
        found += re.findall(rgb_reg, background_color.lower())
        
        if len(found) <= 0:
            continue

        if 'rgba' in found[0] and ', 0)' in found[0]:
            background_color_clean = 'rgb(255, 255, 255)'
        else: 
            background_color_clean = found[0].lower()

        if background_color_clean not in tmp_background_color_dict:
            tmp_background_color_dict[background_color_clean] = page['background_color'][background_color]
        else:
            tmp_background_color_dict[background_color_clean] += page['background_color'][background_color]

    tmp_font_family_dict_total: float = float(sum(list(tmp_font_family_dict.values())))
    tmp_font_size_dict_total: float = float(sum(list(tmp_font_size_dict.values())))
    tmp_font_style_dict_total: float = float(sum(list(tmp_font_style_dict.values())))
    tmp_font_color_dict_total: float = float(sum(list(tmp_font_color_dict.values())))
    tmp_background_color_dict_total: float = float(sum(list(tmp_background_color_dict.values())))
    tmp_font_family_dict = {k: v / tmp_font_family_dict_total for k, v in tmp_font_family_dict.items()}
    tmp_font_size_dict = {k: v / tmp_font_size_dict_total for k, v in tmp_font_size_dict.items()}
    tmp_font_style_dict = {k: v / tmp_font_style_dict_total for k, v in tmp_font_style_dict.items()}
    tmp_font_color_dict = {k: v / tmp_font_color_dict_total for k, v in tmp_font_color_dict.items()}
    tmp_background_color_dict = {k: v / tmp_background_color_dict_total for k, v in tmp_background_color_dict.items()}

    font_family_dict = merge_dicts(font_family_dict, tmp_font_family_dict)
    font_size_dict = merge_dicts(font_size_dict, tmp_font_size_dict)
    font_style_dict = merge_dicts(font_style_dict, tmp_font_style_dict)
    font_color_dict = merge_dicts(font_color_dict, tmp_font_color_dict)
    background_color_dict = merge_dicts(background_color_dict, tmp_background_color_dict)

# Sort the data in descending order by occurences
total: float = float(len(succeeded))
font_family_dict = {k: v / total for k, v in sorted(font_family_dict.items(), key=lambda item: item[1], reverse=True)}
font_size_dict = {k: v / total for k, v in sorted(font_size_dict.items(), key=lambda item: item[1], reverse=True)}
font_style_dict = {k: v / total for k, v in sorted(font_style_dict.items(), key=lambda item: item[1], reverse=True)}
font_color_dict = {k: v / total for k, v in sorted(font_color_dict.items(), key=lambda item: item[1], reverse=True)}
background_color_dict = {k: v / total for k, v in sorted(background_color_dict.items(), key=lambda item: item[1], reverse=True)}

log = {
    'succeeded': succeeded,
    'failed': failed,
    'font_family_dict': font_family_dict,
    'font_size_dict': font_size_dict,
    'font_style_dict': font_style_dict,
    'font_color_dict': font_color_dict,
    'background_color_dict': background_color_dict
    }


# print(font_color_dict)
with open('log_clean_example.json', 'w') as f:
    f.write(json.dumps(log, indent=4))
    f.write('\n')

print('Done!')
