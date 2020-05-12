from cefpython3 import cefpython as cef
import os
from pathlib import Path
import sys
from multiprocessing import Process, Queue
from PIL import Image
from typing import Dict, Tuple
import asyncio
import re
import json
import csv
import codecs
import progressbar

data_list: str = 'path,word,left,top,width,height\n'

prints: bool = False
mk_csv: bool = False

# Main function
def main() -> None:

    cef_handle = CefHandle()
    cef_handle.run_cef()

class Mediator(object):
    def __init__(self, browser: cef.PyBrowser) -> None:
        self.loaded: bool = False
        self.painted: bool = False
        self.viewport_size: Tuple[int, int] = (1100, 800)
        self.browser: cef.PyBrowser = browser
        self.buffer: str = ''
        self.lock: asyncio.Lock = asyncio.Lock()
        self.in_dir: str = 'html/'
        self.out_dir: str = './dataset/'
        self.current_file: str = 'index.html'
        Path(self.out_dir).mkdir(parents=True, exist_ok=True)
        self.urls: [str] = ['']

        for path in Path(self.in_dir).rglob('*.html'):
            self.urls.append('file://' + os.path.abspath(path))
        self.urls.pop(0)
        self.bar = progressbar.ProgressBar(max_value=len(self.urls))
        self.count: int = 0

    def get_current_url(self) -> str:
        return self.urls[self.count]

    def next_url(self) -> None:
        #print('count: ' + str(self.count))
        if self.count < len(self.urls):
            self.browser.StopLoad()
            global prints
            if prints: print('RENDER:  "' + self.urls[self.count] + '"')
            reg_ex = '(?<='+ self.in_dir + ').*'
            self.current_file = re.search(re.compile(reg_ex), self.urls[self.count]).group()[:-5]
            self.browser.LoadUrl(self.urls[self.count])
            self.browser.WasResized()

    def save_image(self) -> bool:
        if self.painted and self.loaded:
            global prints
            global mk_csv

            buffer_string = self.browser.GetUserData('OnPaint.buffer_string')
            rgba_image = Image.frombytes('RGBA', self.viewport_size, buffer_string, 'raw', 'RGBA', 0, 1)
            rgb_image = rgba_image.convert('RGB')
            # Save image
            real_out_dir: str = re.search(r'(.*[\/])', self.out_dir + self.current_file).group()
            Path(real_out_dir).mkdir(parents=True, exist_ok=True)
            rgb_image.save(self.out_dir + self.current_file + '.png', 'PNG', dpi=(self.viewport_size[0], self.viewport_size[1]))
            if prints: print('SAVE:    "' + self.out_dir + self.current_file + '.png"')   # relative to self.real_out_dir
            self.painted = False
            self.loaded = False
            self.bar.update(self.count)
            self.count += 1
            if self.count >= len(self.urls) and mk_csv:
                with codecs.open(self.out_dir + 'data.csv', 'w', "utf-8") as f:
                    f.write(data_list)
                if prints: print('SAVED:  ' + 'data.csv')
                if prints: print('Finished without error! (ignore the following output)')
                if prints: print()
                sys.exit()
            self.next_url()

class CefHandle(object):

    def run_cef(self) -> None:

        # Setup CEF
        sys.excepthook = cef.ExceptHook  # to shutdown all CEF processes on error
        settings: Dict[str, bool] = { 
            'windowless_rendering_enabled': True,  # offscreen-rendering
        }
        switches: Dict[str, str] = {
            'disable-gpu': '',
            'disable-gpu-compositing': '',
            'enable-begin-frame-scheduling': '',
            'disable-surfaces': '',
            'disable-smooth-scrolling': '',
        }
        browser_settings: Dict[str, int] = {
            'windowless_frame_rate': 30,
        }
        cef.Initialize(settings=settings, switches=switches)
        print()
        browser = self.create_browser(browser_settings)

        bindings = cef.JavascriptBindings()
        bindings.SetFunction("save_data", save_data_txt)
        browser.SetJavascriptBindings(bindings)

        # Enter loop
        cef.MessageLoop()

        # Cleanup
        cef.Shutdown()

    # Create a browser
    def create_browser(self, settings) -> None:

        parent_window_handle: int = 0
        window_info: cef.WindowInfo = cef.WindowInfo()
        window_info.SetAsOffscreen(parent_window_handle)
        browser: cef.PyBrowser = cef.CreateBrowserSync(window_info=window_info, settings=settings, url='')
        
        mediator: Mediator = Mediator(browser)
        mediator.next_url()

        browser.SetClientHandler(LoadHandler(mediator))
        browser.SetClientHandler(RenderHandler(mediator))

        browser.SendFocusEvent(True)
        browser.WasResized()
        return browser

    # Exit the application
    def exit_app(self, browser: cef.PyBrowser) -> None:
        browser.CloseBrowser()
        cef.QuitMessageLoop()

# Handle the rendering
class RenderHandler(object):
    def __init__(self, mediator: Mediator):
        self.mediator = mediator

    def GetViewRect(self, rect_out: [int], **_) -> bool:
        rect_out.extend([0, 0, self.mediator.viewport_size[0], self.mediator.viewport_size[1]])
        return True

    def OnPaint(self, browser: cef.PyBrowser, element_type, dirty_rects, paint_buffer, width, height) -> None:
        #print('dirty_rects: ')
        #print(dirty_rects)
        if element_type == cef.PET_VIEW:
            #print('OnPaint: ' + browser.GetUrl())
            # retrieve the image bytes
            buffer_string: str = paint_buffer.GetBytes(mode='rgba', origin='top-left')
            # initiate the image creation
            browser.SetUserData('OnPaint.buffer_string', buffer_string)
            self.mediator.painted = True
            self.mediator.save_image()

# TODO:     save only when truly the whole page was loaded
# Problem:  sometimes it's loaded before 'OnPaint' gets called the last time
#       ==> we cannot know when it was called the last time
# **** Maybe okay considering the small html pages ****

class LoadHandler(object):
    def __init__(self, mediator: Mediator):
        self.mediator = mediator

    def OnLoadEnd(self, browser: cef.PyBrowser, frame: cef.PyFrame, **_):
            self.mediator.loaded = True
            browser.ExecuteFunction("get_data_txt")

            self.mediator.save_image()


    # def OnLoadingStateChange(self, browser: cef.PyBrowser, **_):
    #     print('OnLoad')
    #     self.mediator.loaded = True
    #     if self.mediator.save_image():
    #         self.mediator.next_url()

def save_data_csv(data) -> None:
    global data_list
    data_list += data

def save_data_txt(value):
    path: str = value.split('\n')[0][8:]
    os.path.abspath('./')
    term = 'OCROnWebpages\/html\/'
    reg = '(' + term + ')(.*)'
    found = re.search(re.compile(reg),path).groups()[1]

    found_list = found.split('/')[0:-1]
    found_path = '/'.join(found_list)

    found_path_name_list = found.split('.')[0:-1]
    found_path_name = '/'.join(found_path_name_list)

    out_dir = os.path.abspath('dataset/' + found_path + '/')
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    with codecs.open('dataset/' + found_path_name + '.txt', 'w', "utf-8") as f:
        f.write(value)
    global prints
    if prints: print('SAVE:    ' + out_dir + '.txt')

if __name__ == '__main__':
    main()
