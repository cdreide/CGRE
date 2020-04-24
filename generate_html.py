from cefpython3 import cefpython as cef
import os
from pathlib import Path
import sys
import numpy as np
import cv2
import htmlmin
import dominate
from dominate.tags import *
import lorem
import re
from enum import Enum
import progressbar
import codecs
import random

# html/font_family/font_size/font_style/layout

prints: bool = True

def main() -> None:
    print('generate_html called.')
    generator: Generator = Generator()
    for i in progressbar.progressbar(range(0, 10)):
        generator.save_directory: str = './html/' + str(i) + '/'
        generator.generate_html()

class Layout(Enum):
    center = 1
    left = 2
    top = 3
    wall_of_text = 4
    l_word_c_text = 5
    words = 6

class Generator(object):
    def __init__(self):
        self.save_directory: str = './html/'
        if not os.path.isdir(self.save_directory):
            os.mkdir(self.save_directory)

        self.font_families: [str] = ['arial', 'verdana', 'georgia']
        self.font_sizes: [str] = ['six', 'ten', 'sixteen']
        self.font_styles: [str] = ['normal', 'italic', 'bold', 'underline']
        self.layouts = [e for e in Layout]
        self.types = ['bible', 'lorem', 'random'] # all of them use usernames

        self.word_list: [str] = prepare_words()
        self.bible_list: [str] = prepare_bible()


    def generate_html(self):

        for font_family in self.font_families:
            for font_size in self.font_sizes:
                for font_style in self.font_styles:
                    for layout in self.layouts:
                        for t in self.types:
                            # Generate path
                            file_path: str = self.save_directory + font_family + '/' + font_size + '/' + font_style + '/' + layout.name + '/' + t
                            
                            # Generate content
                            words: [str] = ['']
                            sentences: [str] = ['']
                            paragraphs: [str] = ['']
                            usernames: [str] = ['']

                            # Get words, sentences, paragraphs and usernames
                            if t == 'lorem':
                                for _ in range(10):
                                    words.append(lorem.get_word())
                                    sentences.append(lorem.get_sentence())
                                    paragraphs.append(lorem.get_paragraph())
                                    usernames.append(gen_username(self.word_list))
                            elif t == 'bible':
                                for _ in range(10):
                                    words.append(random.choice(self.word_list))
                                    sentences.append(random.choice(self.bible_list))
                                    temp_paragraph = ''
                                    for _ in range(random.randint(2, 5)):
                                        temp_paragraph += random.choice(self.bible_list) + ' '
                                    paragraphs.append(temp_paragraph)
                                    usernames.append(gen_username(self.word_list))
                            elif t == 'random':
                                for _ in range(10):
                                    words.append(random.choice(self.word_list))
                                    sentences.append(lorem.get_sentence())
                                    paragraphs.append(lorem.get_paragraph())
                                    usernames.append(gen_username(self.word_list))

                            words.pop(0)
                            sentences.pop(0)
                            paragraphs.pop(0)
                            usernames.pop(0)

                            # Generate and save document
                            self.generate_file(
                                path=file_path,
                                words=words,
                                sentences=sentences,
                                paragraphs=paragraphs,
                                usernames=usernames,
                                font_family=font_family,
                                font_size=font_size,
                                font_style=font_style,
                                layout=layout
                                )

    def generate_file(self, 
        path: str,
        words: [str]=[''],
        sentences: [str]=[''],
        paragraphs: [str]=[''],
        usernames: [str]=[''],
        font_family: str='',
        font_size: str='',
        font_style: str='',
        layout: Layout=Layout.center
        ):
        doc = dominate.document(title='generated')

        with doc.head:
            link(rel='stylesheet', href=os.path.abspath('style.css'))
            script(type='text/javascript', src=os.path.abspath('script.js'))

        with doc.body:
            with div(cls='grid' + ' ' + font_family + ' ' + font_size + ' ' + font_style):
                if layout == Layout.center:
                            div(cls='cell')
                            str_to_span(paragraphs[0])
                            div(cls='cell')
                            div(cls='cell')
                            str_to_span(paragraphs[1])
                            div(cls='cell')
                            div(cls='cell')
                            str_to_span(paragraphs[2])
                            div(cls='cell')
                elif layout == Layout.left:
                            str_to_span(paragraphs[0])
                            div(cls='cell')
                            div(cls='cell')
                            str_to_span(paragraphs[1])
                            div(cls='cell')
                            div(cls='cell')
                            str_to_span(paragraphs[2])
                            div(cls='cell')
                            div(cls='cell')

                elif layout == Layout.top:
                            str_to_span(paragraphs[0])
                            str_to_span(paragraphs[1])
                            str_to_span(paragraphs[2])
                            div(cls='cell')
                            div(cls='cell')
                            div(cls='cell')
                            div(cls='cell')
                            div(cls='cell')
                            div(cls='cell')

                elif layout == Layout.wall_of_text:
                            str_to_span(paragraphs[0])
                            str_to_span(paragraphs[1])
                            str_to_span(paragraphs[2])
                            str_to_span(paragraphs[3])
                            str_to_span(paragraphs[4])
                            str_to_span(paragraphs[5])
                            str_to_span(paragraphs[6])
                            str_to_span(paragraphs[7])
                            str_to_span(paragraphs[8])
                            
                elif layout == Layout.l_word_c_text:
                            str_to_span(usernames[0])
                            str_to_span(paragraphs[0])
                            div(cls='cell')
                            str_to_span(usernames[1])
                            str_to_span(paragraphs[1])
                            div(cls='cell')
                            str_to_span(usernames[2])
                            str_to_span(paragraphs[2])
                            div(cls='cell')

                elif layout == Layout.words:
                            str_to_span(words[0])
                            str_to_span(words[1])
                            str_to_span(words[2])
                            str_to_span(words[3])
                            str_to_span(words[4])
                            str_to_span(words[5])
                            str_to_span(words[6])
                            str_to_span(words[7])
                            str_to_span(words[8])

        out_path: str = ''

        try:
            out_path = re.search(r'(.*[\/])', path).group()
        except AttributeError:
            out_path = path
        Path(out_path).mkdir(parents=True, exist_ok=True)
        with codecs.open(path + '.html', 'w', 'utf-8-sig') as f:
            f.write(htmlmin.minify(doc.render(), remove_empty_space=True))
        global prints
        if prints: print('CREATED:  ' + path + '.html')



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
    return div(cls='cell').add(paragraph)

def gen_username(possibilities: [str]):

    choice: int = random.randint(0, 3)

    username: str = ''
    # word
    if choice == 0:
        times: int = random.randint(1, 3)
        for _ in range(times):
            username += random.choice(possibilities)

    # word + number
    elif choice == 1:
        word: str = random.choice(possibilities)
        number: int = random.randint(0, 99999)
        username = word + str(number)

	# word with numbers
    elif choice == 2:
        word: str = random.choice(possibilities)
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
        letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
        length: int = random.randint(4, 10)
        username = ''.join(random.choice(letters) for i in range(length))


    return username

# Extracts every sentence of the Bible (King James Translation)
def prepare_bible():
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

# Creates word list from copy from '/user/share/dict/words'
def prepare_words():
    words: str = ''
    with open('resources/words', 'r') as f:
        words = f.read()
    return words.splitlines()


if __name__ == '__main__':
    main()
