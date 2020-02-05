from cefpython3 import cefpython as cef
import os
import sys
import numpy as np
import cv2


def main() -> None:
    print('generate_html called.')

if __name__ == '__main__':
    main()
















    from cefpython3 import cefpython as cef
import os
import sys
import numpy as np
from PIL import Image, ImageFile

# URL = "https://www.uni-koblenz-landau.de" 
path = "./html/index.html"
URL = "file:///" + os.path.abspath(path)
VIEWPORT_SIZE = (1024, 768)
SCREEN = np.zeros((VIEWPORT_SIZE[1], VIEWPORT_SIZE[0], 4), np.uint8) # BGRA provided by CEF

def main() -> None:

    # Setup CEF
    sys.excepthook = cef.ExceptHook  # to shutdown all CEF processes on error
    settings = { "windowless_rendering_enabled": True, } # offscreen-rendering
    switches = {
        "disable-gpu": "",
        "disable-gpu-compositing": "",
        "enable-begin-frame-scheduling": "",
        "disable-surfaces": "",
        "disable-smooth-scrolling": "",
    }
    browser_settings = {
        "windowless_frame_rate": 30,
    }
    cef.Initialize(settings=settings, switches=switches)
    parent_window_handle = 0
    window_info = cef.WindowInfo()
    window_info.SetAsOffscreen(parent_window_handle)
    browser = cef.CreateBrowserSync(window_info=window_info, settings=browser_settings, url=URL)
    browser.SetClientHandler(RenderHandler())
    browser.SendFocusEvent(True)

    print('cef.MessageLoop()')
    # Enter loop
    cef.MessageLoop()

    # Cleanup
    cef.Shutdown()

# Exit the application
def exit_app(browser):
    browser.CloseBrowser()
    cef.QuitMessageLoop()
  
def save_image() -> None:


class LoadHandler(object):
    def OnLoadingStateChange(self, browser, is_loading, **_):
        """Called when the loading state has changed."""
        if not is_loading:
            # Loading is complete
            sys.stdout.write(os.linesep)
            print("[screenshot.py] Web page loading is complete")
            save_screenshot(browser)
            # See comments in exit_app() why PostTask must be used
            cef.PostTask(cef.TID_UI, exit_app, browser)
#    def OnLoadEnd(self, browser, frame, **_):
#        print('loaded')
#        # Copy screen pixels before manipulation
#        # buffer: bytes
#        # width: int
#        # height: int
#        buffer, width, height = browser.GetImage()
#        buffer_len = (width * 3 + 3) & -4
#        image = Image.frombytes("RGB", (width, height), buffer,
#                                "raw", "RGB", buffer_len, 1)
#        ImageFile.MAXBLOCK = width * height
#
#        # Save image
#        if not os.path.isdir('./dataset'):
#            os.mkdir('./dataset')
#        image.save('./dataset/test.png', 'PNG')
#        print('./dataset/test.png')

class RenderHandler(object):
    def OnPaint(self, browser, element_type, paint_buffer, **_):
        def __init__(self):
            self.OnPaint_called = False

        if self.OnPaint_called:
            sys.stdout.write(".")
            sys.stdout.flush()
        else:
            sys.stdout.write("[screenshot.py] OnPaint")
            self.OnPaint_called = True
        if element_type == cef.PET_VIEW:
            print('paint')

            buffer_string = paint_buffer.GetBytes(mode="rgba",
                                                  origin="top-left")
            browser.SetUserData("OnPaint.buffer_string", buffer_string)        

if __name__ == '__main__':
    main()