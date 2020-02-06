from cefpython3 import cefpython as cef
import os
import sys
import numpy as np
import cv2
import htmlmin
import dominate
from dominate.tags import *
import lorem

def main() -> None:
    print('generate_html called.')
    generator: Generator = Generator()
    generator.generate_html()

class Generator(object):
    def __init__(self):
        self.save_directory: str = './test_html/'
        if not os.path.isdir(self.save_directory):
            os.mkdir(self.save_directory)


    # top
    # middle
    # bottom
    # left
    # center
    # right








    def generate_html(self):

        some_word: str = lorem.get_word()
        some_sentence: str = lorem.get_sentence()
        some_paragraph: str = lorem.get_paragraph()
        self.generate_file(name='index', paragraph=some_paragraph, word=some_word, sentence=some_sentence)
        #self.generate_file(name='index', paragraph=' ', word=' ', sentence=' ')


    def generate_file(self, name: str, word: str='', sentence: str='', paragraph: str=''):
        doc = dominate.document(title='generated')

        with doc.head:
            link(rel='stylesheet', href='../style.css')
            script(type='text/javascript', src='script.js')

        with doc.body:
            with div(cls='grid'):
                if word:
                    with div(cls='cell'):
                        p(word)
                if sentence:
                    with div(cls='cell'):
                        p(sentence)
                if paragraph:
                    with div(cls='cell'):
                        p(paragraph)

                if word:
                    with div(cls='cell'):
                        p(word)
                if sentence:
                    with div(cls='cell'):
                        p(sentence)
                if paragraph:
                    with div(cls='cell'):
                        p(paragraph)

                if word:
                    with div(cls='cell'):
                        p(word)
                if sentence:
                    with div(cls='cell'):
                        p(sentence)
                if paragraph:
                    with div(cls='cell'):
                        p(paragraph)

        self.save_file(htmlmin.minify(doc.render(pretty=False), remove_empty_space=True), name)

    def save_file(self, document: dominate.document, name: str) -> None:
        with open(self.save_directory + name + '.html', 'w') as f:
            f.write(document)
        print('CREATED:  ' + name + '.html')



if __name__ == '__main__':
    main()