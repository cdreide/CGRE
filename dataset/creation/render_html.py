from optparse import OptionParser
from cefpython3 import cefpython as cef
from pathlib import Path
import sys
from PIL import Image
from typing import Dict, Tuple
import re
import codecs
import progressbar
import traceback
import time

input_dir: str = ''
output_dir: str = ''

# Main function
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

    render_html(options.in_path, options.out_path)

def render_html(in_path: str, out_path: str) -> None:
    cef_handle = CefHandle()
    cef_handle.run_cef(in_path, out_path)

class Mediator(object):
    def __init__(self, browser: cef.PyBrowser, in_path: str, out_path: str) -> None:
        self.loaded: bool = False
        self.painted: bool = False
        self.viewport_size: Tuple[int, int] = (1024, 768) # (1100, 800)
        self.browser: cef.PyBrowser = browser
        self.buffer: str = ''
        self.in_dir: str = in_path
        self.out_dir: str = out_path
        self.current_file: str = ''
        Path(self.out_dir).mkdir(parents=True, exist_ok=True)
        self.urls: [str] = ['']

        for path in Path(self.in_dir).rglob('*.html'):
            self.urls.append('file://' + str(Path(path).absolute()))
        self.urls.pop(0)
        self.bar = progressbar.ProgressBar(max_value=len(self.urls))
        self.count: int = 0

        global input_dir
        input_dir = self.in_dir
        global output_dir
        output_dir = self.out_dir

    def get_current_url(self) -> str:
        return self.urls[self.count]

    def next_url(self) -> None:
        if self.count < len(self.urls):
            self.browser.StopLoad()
            reg_ex = '(?<='+ self.in_dir + ').*'
            self.current_file = re.search(re.compile(reg_ex), self.urls[self.count]).group()[:-5]
            self.browser.LoadUrl(self.urls[self.count])
            self.browser.WasResized()

    def save_image(self) -> bool:
        if self.painted and self.loaded:
            buffer_string = self.browser.GetUserData('OnPaint.buffer_string')
            rgba_image = Image.frombytes('RGBA', self.viewport_size, buffer_string, 'raw', 'RGBA', 0, 1)
            rgb_image = rgba_image.convert('RGB')
            # Save image
            real_out_dir: str = re.search(r'(.*[\/])', self.out_dir + self.current_file).group()
            Path(real_out_dir).mkdir(parents=True, exist_ok=True)
            rgb_image.save(self.out_dir + self.current_file + '.png', 'PNG', dpi=(self.viewport_size[0], self.viewport_size[1]))
            self.painted = False
            self.loaded = False
            self.bar.update(self.count)
            self.count += 1
            if self.count >= len(self.urls):
                exit_app()
            self.next_url()


class CefHandle(object):

    def run_cef(self, in_path: str, out_path: str) -> None:

        # Setup CEF
        sys.excepthook = customExceptHook  # to shutdown all CEF processes on error
        settings: Dict[str, bool] = { 
            'windowless_rendering_enabled': True,  # offscreen-rendering
        }
        switches: Dict[str, str] = {
            # 'headless': '',
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
        browser = self.create_browser(browser_settings, in_path, out_path)

        bindings = cef.JavascriptBindings()
        bindings.SetFunction("save_data", save_data_txt)
        browser.SetJavascriptBindings(bindings)

        # Enter loop
        cef.MessageLoop()

        # Cleanup
        browser.CloseBrowser()
        cef.Shutdown()
        print('\nDone!')

    # Create a browser
    def create_browser(self, settings, in_path: str, out_path: str) -> None:

        parent_window_handle: int = 0
        window_info: cef.WindowInfo = cef.WindowInfo()
        window_info.SetAsOffscreen(parent_window_handle)
        browser: cef.PyBrowser = cef.CreateBrowserSync(window_info=window_info, settings=settings, url='')
        
        mediator: Mediator = Mediator(browser, in_path, out_path)
        mediator.next_url()

        browser.SetClientHandler(LoadHandler(mediator))
        browser.SetClientHandler(RenderHandler(mediator))

        browser.SendFocusEvent(True)
        browser.WasResized()
        return browser

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

class LoadHandler(object):
    def __init__(self, mediator: Mediator):
        self.mediator = mediator

    def OnLoadEnd(self, browser: cef.PyBrowser, frame: cef.PyFrame, **_):
            self.mediator.loaded = True
            browser.ExecuteFunction("get_data_txt")

            self.mediator.save_image()

def save_data_txt(value):
    global input_dir
    global output_dir

    path: str = value.split('\n')[0][8:]

    term = '\/' + Path(input_dir).name + '\/'
    reg = '(' + term + ')(.*)'
    found = re.search(re.compile(reg),path).groups()[1]


    # found_list = found.split('/')[0:-1]
    # found_path = '/'.join(found_list)

    # found_path_name_list = found.split('.')[0:-1]
    # found_path_name = '/'.join(found_path_name_list)

    out_path = str(Path(output_dir).joinpath(found)).replace(Path(found).suffix, '.txt')
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    with codecs.open(out_path, 'w', "utf-8") as f:
        f.write(value)

# Needed to exit the Message Loop without killing the process:
class FinishedException(Exception):
    pass

# Exit the application
def exit_app() -> None:
    raise FinishedException("Finished!") 

def customExceptHook(exc_type, exc_value, exc_trace):
    if exc_type == FinishedException:
        cef.QuitMessageLoop()
    else:
        """Global except hook to exit app cleanly on error.
        This hook does the following: in case of exception write it to
        the "error.log" file, display it to the console, shutdown CEF
        and exit application immediately by ignoring "finally" (_exit()).
        """
        print("[CEF Python] ExceptHook: catched exception, will shutdown CEF")
        msg = "".join(traceback.format_exception(exc_type, exc_value,
                                                exc_trace))
        error_file = "error.log"
        encoding = "utf-8"
        if type(msg) == bytes:
            msg = msg.decode(encoding=encoding, errors="replace")
        try:
            with codecs.open(error_file, mode="a", encoding=encoding) as fp:
                fp.write("\n[%s] %s\n" % (
                        time.strftime("%Y-%m-%d %H:%M:%S"), msg))
        except:
            print("[CEF Python] WARNING: failed writing to error file: %s" % (
                    error_file))
        # Convert error message to ascii before printing, otherwise
        # you may get error like this:
        # | UnicodeEncodeError: 'charmap' codec can't encode characters
        msg = msg.encode("ascii", errors="replace")
        msg = msg.decode("ascii", errors="replace")
        print("\n"+msg)
        # There is a strange bug on Mac. Sometimes except message is not
        # printed if QuitMessageLoop and Shutdown were called before the print
        # message above.
        cef.QuitMessageLoop()
        cef.Shutdown()
        # noinspection PyProtectedMember
        quit()


if __name__ == '__main__':
    main()
