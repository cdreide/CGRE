from optparse import OptionParser
import os
from pathlib import Path
import sys
import htmlmin
import dominate
from dominate.tags import *
import lorem
import re
from enum import Enum
import progressbar
import codecs
import json
import random
import shutil

# html/font_family/font_size/font_style/layout

def main() -> None:
    parser = OptionParser()
    parser.add_option( '-c',
                    '--crawled',
                    dest = 'crawl_data_path',
                    metavar = 'FILE' )
    parser.add_option( '-t',
                    '--top',
                    dest = 'top_values',
                    default = 1,
                    metavar = 'INT' )
    parser.add_option( '-o',
                    '--out',
                    dest = 'out_path',
                    metavar = 'FOLDER' )
    (options, args) = parser.parse_args()

    generate_html(Path(options.crawl_data_path), int(options.top_values), Path(options.out_path))

def generate_html(crawl_data_path: Path, top_values: int, out_path: Path) -> None:
    crawl_data: dict = {}
    tmp_data: dict = {}
    with open(crawl_data_path) as f:
        tmp_data = json.load(f)

    for category in tmp_data.keys():
        if isinstance(tmp_data[category], dict):
            crawl_data[category] = list(tmp_data[category].keys())[0:top_values]

    generator: Generator = Generator(crawl_data, out_path)

    print('Create Dataset:')
    generator.save_directory: str = out_path
    generator.generate_html()

class Layout(Enum):
    center = 1
    left = 2
    top = 3
    wall_of_text = 4
    l_word_c_text = 5
    words = 6

class Generator(object):
    def __init__(self, crawl_data: dict, out_path: Path):
        self.save_directory: Path = out_path
        self.misc_path: Path = self.save_directory.joinpath('misc')
        self.misc_path.mkdir(parents=True, exist_ok=True)
        shutil.copyfile('style.css', self.misc_path.joinpath('style.css'))
        shutil.copyfile('script.js', self.misc_path.joinpath('script.js'))
        self.img_path: Path = self.misc_path.joinpath('imgs')
        if self.img_path.exists():
            shutil.rmtree(self.img_path)
        shutil.copytree(Path('resources/imgs/'), self.img_path)

        self.font_families: [str] = crawl_data['font_family_dict']
        self.font_sizes: [str] = crawl_data['font_size_dict']
        self.font_styles: [str] = crawl_data['font_style_dict']
        # self.font_weights: [str] = crawl_data['font_weight_dict']
        # self.text_decorations: [str] = crawl_data['text_decoration_dict']
        self.font_colors: [str] = crawl_data['font_color_dict']
        self.background_colors: [str] = crawl_data['background_color_dict']
        self.layouts = [e for e in Layout]
        self.content_types = ['bible', 'lorem', 'random'] # all of them use usernames
        self.other_types = ['images_only', 'only_text', 'with_images']

        self.word_list: [str] = prepare_words()
        self.bible_list: [str] = prepare_bible()
        self.img_list: [str] = self.prepare_imgs()


    def generate_html(self):
        iterations = (len(self.other_types)-1) * len(self.font_families) * len(self.font_sizes) * len(self.font_styles) * len(self.font_colors) * len(self.background_colors) * len(self.layouts) * len(self.content_types) + (len(self.background_colors) * len(self.layouts))
        curr_it = 0
        with progressbar.ProgressBar(max_value=iterations) as bar:
            for other_type in self.other_types:
                if other_type == 'images_only':
                    for background_color in self.background_colors:
                        count: int = 0
                        for layout in self.layouts:
                            # Generate path
                            file_path: Path = Path(other_type.replace(' ', '_') + '/' + background_color.replace(' ', '_') + '/' + str(count))
                            count += 1
                            self.prepare(
                                file_path=file_path,
                                other_type=other_type,
                                background_color=background_color,
                                layout=layout,
                                )
                else:
                    for font_family in self.font_families:
                        for font_size in self.font_sizes:
                            for font_style in self.font_styles:
                                # for font_style in self.font_styles:
                                # for text_decoration in self.text_decorations:
                                for font_color in self.font_colors:
                                    for background_color in self.background_colors:
                                        for layout in self.layouts:
                                            for content_type in self.content_types:
                                                bar.update(curr_it)
                                                curr_it += 1
                                                # Generate path
                                                file_path: Path = Path(other_type.replace(' ', '_') + '/' + font_family.replace(' ', '_') + '/' + font_size.replace(' ', '_') + '/' + font_style.replace(' ', '_') + '/' + font_color.replace(' ', '_') + '/'.replace(' ', '_') + '/' + background_color.replace(' ', '_') + '/' + layout.name.replace(' ', '_') + '/' + content_type.replace(' ', '_'))
                                                self.prepare(
                                                    file_path=file_path,
                                                    other_type=other_type,
                                                    font_family=font_family,
                                                    font_size=font_size,
                                                    font_style=font_style,
                                                    # font_weight=font_weight,
                                                    # text_decoration=text_decoration,
                                                    font_color=font_color,
                                                    background_color=background_color,
                                                    layout=layout,
                                                    content_type=content_type,
                                                    )


    def prepare(self,
        file_path: Path=Path(''),
        other_type: str='',
        font_family: str='',
        font_size: str='',
        font_style: str='',
        font_weight: str='',
        text_decoration: str='',
        font_color: str='',
        background_color: str='',
        layout: Layout=Layout.center,
        content_type: str='',
    ):

        style: str = ''
        if len(font_family) > 0: style += 'font-family: ' + font_family + '; '
        if len(font_size) > 0: style += 'font-size: ' + font_size + '; '
        if len(font_style) > 0: style += 'font-style: ' + font_style + '; '
        if len(font_weight) > 0: style += 'font-weight: ' + font_weight + '; '
        if len(text_decoration) > 0: style += 'text-decoration: ' + text_decoration + '; '
        if len(font_color) > 0: style += 'color: ' + font_color + '; '
        if len(background_color) > 0: style += 'background: ' + background_color + '; '

        if font_color[1:] == background_color[1:]:
            return

        # Generate content
        words: [str] = ['']
        sentences: [str] = ['']
        paragraphs: [str] = ['']
        usernames: [str] = ['']
        background_images: [str] = []

        # Get words, sentences, paragraphs and usernames
        if other_type != 'images_only':
            if content_type == 'lorem':
                for _ in range(10):
                    words.append(lorem.get_word())
                    sentences.append(lorem.get_sentence())
                    paragraphs.append(lorem.get_paragraph())
                    usernames.append(self.gen_username())

            elif content_type == 'bible':
                for _ in range(10):
                    words.append(random.choice(self.word_list))
                    sentences.append(random.choice(self.bible_list))
                    temp_paragraph = ''
                    for _ in range(random.randint(2, 5)):
                        temp_paragraph += random.choice(self.bible_list) + ' '
                    paragraphs.append(temp_paragraph)
                    usernames.append(self.gen_username())

            elif content_type == 'random':
                for _ in range(10):
                    words.append(self.gen_random_word())
                    sentences.append(self.gen_random_sentence())
                    paragraphs.append(self.gen_random_paragraph())
                    usernames.append(self.gen_username())

            # Remove firsts
            words.pop(0)
            sentences.pop(0)
            paragraphs.pop(0)
            usernames.pop(0)

        else:
            words = ['', '','','','','','','','','']
            sentences = ['', '','','','','','','','','']
            paragraphs = ['', '','','','','','','','','']
            usernames = ['', '','','','','','','','','']

        # Get images
        if other_type == 'with_images' or other_type == 'images_only':
            background_images = self.get_images()

        # Generate and save document
        self.generate_file(
            path=file_path,
            words=words,
            sentences=sentences,
            paragraphs=paragraphs,
            usernames=usernames,
            background_images=background_images,
            style=style,
            layout=layout
            )

    def generate_file(self, 
        path: Path=Path(''),
        words: [str]=[''],
        sentences: [str]=[''],
        paragraphs: [str]=[''],
        usernames: [str]=[''],
        background_images: [str]=[],
        style: str='',
        layout: Layout=Layout.center
        ) -> None:

        misc_prefix = ''
        for _ in range(str(path).count('/')):
            misc_prefix += '../'
        misc_prefix += self.misc_path.name
        doc = dominate.document(title='generated')

        background_images = [str(Path(misc_prefix).joinpath(img)) for img in background_images]

        indexes: [int] = []
        possible_indexes: [int] = [0,1,2,3,4,5,6,7,8]
        random.shuffle(possible_indexes)
        for _ in range(len(background_images)):
            indexes.append(possible_indexes.pop())

        with doc.head:
            link(rel='stylesheet', href=str(Path(misc_prefix).joinpath('style.css')))

        with doc.body:
            with div(cls='grid', style=style):
                if layout == Layout.center:
                    if 0 not in indexes:
                        div(cls='cell')
                    else:
                        div(cls='cell').add(img(cls='img', src=background_images.pop()))
                    if 1 not in indexes:
                        div(cls='cell').add(str_to_span(paragraphs[0]))
                    else:
                        div(cls='cell').add(img(cls='img', src=background_images.pop()))
                    if 2 not in indexes:
                        div(cls='cell')
                    else:
                        div(cls='cell').add(img(cls='img', src=background_images.pop()))
                    if 3 not in indexes:
                        div(cls='cell')
                    else:
                        div(cls='cell').add(img(cls='img', src=background_images.pop()))
                    if 4 not in indexes:
                        div(cls='cell').add(str_to_span(paragraphs[1]))
                    else:
                        div(cls='cell').add(img(cls='img', src=background_images.pop()))
                    if 5 not in indexes:
                        div(cls='cell')
                    else:
                        div(cls='cell').add(img(cls='img', src=background_images.pop()))
                    if 6 not in indexes:
                        div(cls='cell')
                    else:
                        div(cls='cell').add(img(cls='img', src=background_images.pop()))
                    if 7 not in indexes:
                        div(cls='cell').add(str_to_span(paragraphs[2]))
                    else:
                        div(cls='cell').add(img(cls='img', src=background_images.pop()))
                    if 8 not in indexes:
                        div(cls='cell')
                    else:
                        div(cls='cell').add(img(cls='img', src=background_images.pop()))

                elif layout == Layout.left:
                    if 0 not in indexes:
                        div(cls='cell').add(str_to_span(paragraphs[0]))
                    else:
                        div(cls='cell').add(img(cls='img', src=background_images.pop()))
                    if 1 not in indexes:
                        div(cls='cell')
                    else:
                        div(cls='cell').add(img(cls='img', src=background_images.pop()))
                    if 2 not in indexes:
                        div(cls='cell')
                    else:
                        div(cls='cell').add(img(cls='img', src=background_images.pop()))
                    if 3 not in indexes:
                        div(cls='cell').add(str_to_span(paragraphs[1]))
                    else:
                        div(cls='cell').add(img(cls='img', src=background_images.pop()))
                    if 4 not in indexes:
                        div(cls='cell')
                    else:
                        div(cls='cell').add(img(cls='img', src=background_images.pop()))
                    if 5 not in indexes:
                        div(cls='cell')
                    else:
                        div(cls='cell').add(img(cls='img', src=background_images.pop()))
                    if 6 not in indexes:
                        div(cls='cell').add(str_to_span(paragraphs[2]))
                    else:
                        div(cls='cell').add(img(cls='img', src=background_images.pop()))
                    if 7 not in indexes:
                        div(cls='cell')
                    else:
                        div(cls='cell').add(img(cls='img', src=background_images.pop()))
                    if 8 not in indexes:
                        div(cls='cell')
                    else:
                        div(cls='cell').add(img(cls='img', src=background_images.pop()))

                elif layout == Layout.top:
                    if 0 not in indexes:
                        div(cls='cell').add(str_to_span(paragraphs[0]))
                    else:
                        div(cls='cell').add(img(cls='img', src=background_images.pop()))
                    if 1 not in indexes:
                        div(cls='cell').add(str_to_span(paragraphs[1]))
                    else:
                        div(cls='cell').add(img(cls='img', src=background_images.pop()))
                    if 2 not in indexes:
                        div(cls='cell').add(str_to_span(paragraphs[2]))
                    else:
                        div(cls='cell').add(img(cls='img', src=background_images.pop()))
                    if 3 not in indexes:
                        div(cls='cell')
                    else:
                        div(cls='cell').add(img(cls='img', src=background_images.pop()))
                    if 4 not in indexes:
                        div(cls='cell')
                    else:
                        div(cls='cell').add(img(cls='img', src=background_images.pop()))
                    if 5 not in indexes:
                        div(cls='cell')
                    else:
                        div(cls='cell').add(img(cls='img', src=background_images.pop()))
                    if 6 not in indexes:
                        div(cls='cell')
                    else:
                        div(cls='cell').add(img(cls='img', src=background_images.pop()))
                    if 7 not in indexes:
                        div(cls='cell')
                    else:
                        div(cls='cell').add(img(cls='img', src=background_images.pop()))
                    if 8 not in indexes:
                        div(cls='cell')
                    else:
                        div(cls='cell').add(img(cls='img', src=background_images.pop()))

                elif layout == Layout.wall_of_text:
                    if 0 not in indexes:
                        div(cls='cell').add(str_to_span(paragraphs[0]))
                    else:
                        div(cls='cell').add(img(cls='img', src=background_images.pop()))
                    if 1 not in indexes:
                        div(cls='cell').add(str_to_span(paragraphs[1]))
                    else:
                        div(cls='cell').add(img(cls='img', src=background_images.pop()))
                    if 2 not in indexes:
                        div(cls='cell').add(str_to_span(paragraphs[2]))
                    else:
                        div(cls='cell').add(img(cls='img', src=background_images.pop()))
                    if 3 not in indexes:
                        div(cls='cell').add(str_to_span(paragraphs[3]))
                    else:
                        div(cls='cell').add(img(cls='img', src=background_images.pop()))
                    if 4 not in indexes:
                        div(cls='cell').add(str_to_span(paragraphs[4]))
                    else:
                        div(cls='cell').add(img(cls='img', src=background_images.pop()))
                    if 5 not in indexes:
                        div(cls='cell').add(str_to_span(paragraphs[5]))
                    else:
                        div(cls='cell').add(img(cls='img', src=background_images.pop()))
                    if 6 not in indexes:
                        div(cls='cell').add(str_to_span(paragraphs[6]))
                    else:
                        div(cls='cell').add(img(cls='img', src=background_images.pop()))
                    if 7 not in indexes:
                        div(cls='cell').add(str_to_span(paragraphs[7]))
                    else:
                        div(cls='cell').add(img(cls='img', src=background_images.pop()))
                    if 8 not in indexes:
                        div(cls='cell').add(str_to_span(paragraphs[8]))
                    else:
                        div(cls='cell').add(img(cls='img', src=background_images.pop()))

                elif layout == Layout.l_word_c_text:
                    if 0 not in indexes:
                        div(cls='cell').add(str_to_span(usernames[0]))
                    else:
                        div(cls='cell').add(img(cls='img', src=background_images.pop()))
                    if 1 not in indexes:
                        div(cls='cell').add(str_to_span(paragraphs[0]))
                    else:
                        div(cls='cell').add(img(cls='img', src=background_images.pop()))
                    if 2 not in indexes:
                        div(cls='cell')
                    else:
                        div(cls='cell').add(img(cls='img', src=background_images.pop()))
                    if 3 not in indexes:
                        div(cls='cell').add(str_to_span(usernames[1]))
                    else:
                        div(cls='cell').add(img(cls='img', src=background_images.pop()))
                    if 4 not in indexes:
                        div(cls='cell').add(str_to_span(paragraphs[1]))
                    else:
                        div(cls='cell').add(img(cls='img', src=background_images.pop()))
                    if 5 not in indexes:
                        div(cls='cell')
                    else:
                        div(cls='cell').add(img(cls='img', src=background_images.pop()))
                    if 6 not in indexes:
                        div(cls='cell').add(str_to_span(usernames[2]))
                    else:
                        div(cls='cell').add(img(cls='img', src=background_images.pop()))
                    if 7 not in indexes:
                        div(cls='cell').add(str_to_span(paragraphs[2]))
                    else:
                        div(cls='cell').add(img(cls='img', src=background_images.pop()))
                    if 8 not in indexes:
                        div(cls='cell')
                    else:
                        div(cls='cell').add(img(cls='img', src=background_images.pop()))

                elif layout == Layout.words:
                    if 0 not in indexes:
                        div(cls='cell').add(str_to_span(words[0]))
                    else:
                        div(cls='cell').add(img(cls='img', src=background_images.pop()))
                    if 1 not in indexes:
                        div(cls='cell').add(str_to_span(words[1]))
                    else:
                        div(cls='cell').add(img(cls='img', src=background_images.pop()))
                    if 2 not in indexes:
                        div(cls='cell').add(str_to_span(words[2]))
                    else:
                        div(cls='cell').add(img(cls='img', src=background_images.pop()))
                    if 3 not in indexes:
                        div(cls='cell').add(str_to_span(words[3]))
                    else:
                        div(cls='cell').add(img(cls='img', src=background_images.pop()))
                    if 4 not in indexes:
                        div(cls='cell').add(str_to_span(words[4]))
                    else:
                        div(cls='cell').add(img(cls='img', src=background_images.pop()))
                    if 5 not in indexes:
                        div(cls='cell').add(str_to_span(words[5]))
                    else:
                        div(cls='cell').add(img(cls='img', src=background_images.pop()))
                    if 6 not in indexes:
                        div(cls='cell').add(str_to_span(words[6]))
                    else:
                        div(cls='cell').add(img(cls='img', src=background_images.pop()))
                    if 7 not in indexes:
                        div(cls='cell').add(str_to_span(words[7]))
                    else:
                        div(cls='cell').add(img(cls='img', src=background_images.pop()))
                    if 8 not in indexes:
                        div(cls='cell').add(str_to_span(words[8]))
                    else:
                        div(cls='cell').add(img(cls='img', src=background_images.pop()))

            script(type='text/javascript', src=str(Path(misc_prefix).joinpath('script.js')))


        out_path: Path = self.save_directory.joinpath(path)
        Path(out_path).parent.mkdir(parents=True, exist_ok=True)
        with codecs.open(str(out_path)+'.html', 'w', 'utf-8-sig') as f:
            f.write(htmlmin.minify(doc.render(), remove_empty_space=True))

    def get_images(self) -> [str]:
        imgs: [str] = ['']

        img_count: int = random.randint(1, 8)

        for _ in range(img_count):
            imgs.append(random.choice(self.img_list))
        imgs.pop(0)
        return list(set(imgs))

    def gen_username(self) -> str:
        choice: int = random.randint(0, 3)

        username: str = ''
        # word
        if choice == 0:
            times: int = random.randint(1, 3)
            for _ in range(times):
                username += random.choice(self.word_list)

        # word + number
        elif choice == 1:
            word: str = random.choice(self.word_list)
            number: int = random.randint(0, 99999)
            username = word + str(number)

        # word with numbers
        elif choice == 2:
            word: str = random.choice(self.word_list)
            count: int = random.randint(0, len(word))
            positions: [int] = list(set(range(len(word))))
            letters: [str] = list(word)

            for _ in range(count):
                number = random.randint(0, 99)
                position = random.choice(positions)
                letters.insert(position, str(number))
                positions.remove(position)
            username = ''.join(letters)

        # random letters & numbers
        elif choice == 3:
            letters: str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
            length: int = random.randint(4, 10)
            username = ''.join(random.choice(letters) for i in range(length))

        return username

    def gen_random_word(self) -> str:
        letters: str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
        letters_count: int = random.randint(3, 13)

        word: str = ''

        for _ in range(letters_count):
            word += random.choice(list(letters))

        return word

    def gen_random_sentence(self) -> str:
        words_count: int = random.randint(3, 10)
        
        sentence: str = ''

        for _ in range(words_count):
            sentence += self.gen_random_word() + ' '

        return sentence

    def gen_random_paragraph(self) -> str:
            words_count: int = random.randint(3, 10)
            
            paragraph: str = ''

            for _ in range(words_count):
                paragraph += self.gen_random_sentence() + ' '

            return paragraph

    def prepare_imgs(self) -> [str]:
        img_list: [str] = ['']

        for path in self.img_path.rglob('*.jpg'):
            i = str(path).find('imgs')
            img_list.append(str(path)[i:])

        return img_list

def str_to_span(content: str):
    paragraph = p()
    for word in content.split():
        # non alphanumeric and alphanumeric will be in different spans
        if not word[-1:].isalnum():
            paragraph.add(span(word[:-1]))
            paragraph.add(span(word[-1:]))
        else:
            paragraph.add(span(word))
        paragraph.add(span(' '))
    return paragraph



# Creates word list from copy from '/user/share/dict/words'
def prepare_words() -> [str]:
    words: str = ''
    with open('resources/words', 'r') as f:
        words = f.read()
    return words.splitlines()

# Extracts every sentence of the Bible (King James Translation)
def prepare_bible() -> [str]:
    bible_list: [str] = ['']
    regex = r'([0-9]+\t[0-9]+\t\t[0-9]+\t)([a-zA-Z0-9.,\;\- ]*)'

    with open('resources/bible', 'r') as f:
        for line in f:
            if line.startswith('#'):
                continue
            sentence = re.findall(regex, line)[0][1]
            bible_list.append(sentence)

    del bible_list[0]
    return bible_list

if __name__ == '__main__':
    main()
