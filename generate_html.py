from cefpython3 import cefpython as cef
import os
import sys
import numpy as np
import cv2
import htmlmin
import dominate
from dominate.tags import *
import lorem
import re
from enum import Enum


def main() -> None:
    print('generate_html called.')
    generator: Generator = Generator()
    generator.generate_dataset()

class Layout(Enum):
    center = 1
    left = 2
    top = 3
    wall_of_text = 4
    l_word_c_text = 5
    words = 6

class Generator(object):
    def __init__(self):
        self.save_directory: str = './test_html/'
        self.count: int = 0
        if not os.path.isdir(self.save_directory):
            os.mkdir(self.save_directory)

        self.font_families: [str] = ['arial', 'verdana', 'georgia']
        self.font_sizes: [str] = ['six', 'ten', 'sixteen']
        self.font_styles: [str] = ['normal', 'italic', 'bold', 'underline']
        self.layouts = [e for e in Layout]


    def generate_dataset(self):


        while self.count < len(self.layouts):
            words: [str] = [""]
            sentences: [str] = [""]
            paragraphs: [str] = [""]
            layout: [Layout] = self.layouts[self.count]
            file_name: str = layout.name
            for i in range(0, 9):
                words.append(lorem.get_word())
                sentences.append(lorem.get_sentence())
                paragraphs.append(lorem.get_paragraph())
            words.pop(0)
            sentences.pop(0)
            paragraphs.pop(0)

            self.generate_file(
                name=file_name,
                words=words,
                sentences=sentences,
                paragraphs=paragraphs,
                font_family=self.font_families[2],
                font_size=self.font_sizes[0],
                font_style=self.font_styles[2],
                layout=layout
                )
            self.count += 1

    def generate_html(self, 
        name: str,
        words: [str]=[''],
        sentences: [str]=[''],
        paragraphs: [str]=[''],
        font_family: str='',
        font_size: str='',
        font_style: str='',
        layout: str=''
        ):

        file_name: str = 'index' + str(self.count)
        some_word: str = lorem.get_word()
        some_sentence: str = lorem.get_sentence()
        some_paragraph: str = lorem.get_paragraph()
        some_layout: str = self.layouts[0]

        self.generate_file(
            name=file_name,
            words=some_word,
            sentences=some_sentence,
            paragraphs=some_paragraph,
            font_family=self.font_families[2],
            font_size=self.font_sizes[0],
            font_style=self.font_styles[2],
            layout=some_layout
            )
        self.count += 1
        #self.generate_file(name='index', paragraph=' ', word=' ', sentence=' ')


    def generate_file(self, 
        name: str,
        words: [str]=[''],
        sentences: [str]=[''],
        paragraphs: [str]=[''],
        font_family: str='',
        font_size: str='',
        font_style: str='',
        layout: Layout=Layout.center
        ):
        doc = dominate.document(title='generated')

        with doc.head:
            link(rel='stylesheet', href=os.path.abspath('style.css'))
            script(type='text/javascript', src='script.js')

        if layout == Layout.center:
            with doc.body:
                with div(cls='grid'):
                    div(cls='cell')
                    if paragraphs[0]:
                        with div(cls='cell'):
                            p(paragraphs[0])
                    div(cls='cell')
                    div(cls='cell')
                    if paragraphs[1]:
                        with div(cls='cell'):
                            p(paragraphs[1])
                    div(cls='cell')
                    div(cls='cell')
                    if paragraphs[2]:
                        with div(cls='cell'):
                            p(paragraphs[2])
                    div(cls='cell')
        elif layout == Layout.left:
            with doc.body:
                with div(cls='grid'):
                    if paragraphs[0]:
                        with div(cls='cell'):
                            p(paragraphs[0])
                    div(cls='cell')
                    div(cls='cell')
                    if paragraphs[1]:
                        with div(cls='cell'):
                            p(paragraphs[1])
                    div(cls='cell')
                    div(cls='cell')
                    if paragraphs[2]:
                        with div(cls='cell'):
                            p(paragraphs[2])
                    div(cls='cell')
                    div(cls='cell')
        elif layout == Layout.top:
            with doc.body:
                with div(cls='grid'):
                    if paragraphs[0]:
                        with div(cls='cell'):
                            p(paragraphs[0])
                    if paragraphs[1]:
                        with div(cls='cell'):
                            p(paragraphs[1])
                    if paragraphs[2]:
                        with div(cls='cell'):
                            p(paragraphs[2])
                    div(cls='cell')
                    div(cls='cell')
                    div(cls='cell')
                    div(cls='cell')
                    div(cls='cell')
                    div(cls='cell')
        elif layout == Layout.wall_of_text:
            with doc.body:
                with div(cls='grid'):
                    if paragraphs[0]:
                        with div(cls='cell'):
                            p(paragraphs[0])
                    if paragraphs[1]:
                        with div(cls='cell'):
                            p(paragraphs[1])
                    if paragraphs[2]:
                        with div(cls='cell'):
                            p(paragraphs[2])
                    if paragraphs[3]:
                        with div(cls='cell'):
                            p(paragraphs[3])
                    if paragraphs[4]:
                        with div(cls='cell'):
                            p(paragraphs[4])
                    if paragraphs[5]:
                        with div(cls='cell'):
                            p(paragraphs[5])
                    if paragraphs[6]:
                        with div(cls='cell'):
                            p(paragraphs[6])
                    if paragraphs[7]:
                        with div(cls='cell'):
                            p(paragraphs[7])
                    if paragraphs[8]:
                        with div(cls='cell'):
                            p(paragraphs[8])
        elif layout == Layout.l_word_c_text:
            with doc.body:
                with div(cls='grid'):
                    if words[0]:
                        with div(cls='cell'):
                            p(words[0])
                    if paragraphs[0]:
                        with div(cls='cell'):
                            p(paragraphs[0])
                    div(cls='cell')
                    if words[1]:
                        with div(cls='cell'):
                            p(words[1])
                    if paragraphs[1]:
                        with div(cls='cell'):
                            p(paragraphs[1])
                    div(cls='cell')
                    if words[2]:
                        with div(cls='cell'):
                            p(words[2])
                    if paragraphs[2]:
                        with div(cls='cell'):
                            p(paragraphs[2])
                    div(cls='cell')                    
        elif layout == Layout.words:
            with doc.body:
                with div(cls='grid'):
                    if words[0]:
                        with div(cls='cell'):
                            p(words[0])
                    if words[1]:
                        with div(cls='cell'):
                            p(words[1])
                    if words[2]:
                        with div(cls='cell'):
                            p(words[2])
                    if words[3]:
                        with div(cls='cell'):
                            p(words[3])
                    if words[4]:
                        with div(cls='cell'):
                            p(words[4])
                    if words[5]:
                        with div(cls='cell'):
                            p(words[5])
                    if words[6]:
                        with div(cls='cell'):
                            p(words[6])
                    if words[7]:
                        with div(cls='cell'):
                            p(words[7])
                    if words[8]:
                        with div(cls='cell'):
                            p(words[8])

        self.save_file(htmlmin.minify(doc.render(pretty=False), remove_empty_space=True), name)

    def save_file(self, document: dominate.document, name: str) -> None:
        with open(self.save_directory + name + '.html', 'w') as f:
            f.write(document)
        print('CREATED:  ' + name + '.html')



if __name__ == '__main__':
    main()
