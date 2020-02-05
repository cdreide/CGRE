from cefpython3 import cefpython as cef
import os
import platform
import subprocess
import sys
import cv2
import numpy as np
import re
from multiprocessing import Process
from PIL import Image
from typing import Dict, Tuple

# Config
VIEWPORT_SIZE: Tuple[int, int] = (1024, 768)
#path: str = "./html/index.html"
#URL: str = "file:///" + os.path.abspath(path)

# Main function
def main() -> None:

    # Setup CEF
    sys.excepthook = cef.ExceptHook  # to shutdown all CEF processes on error
    settings: Dict[str, bool] = { 
        "windowless_rendering_enabled": True,  # offscreen-rendering
    }
    switches: Dict[str, str] = {
        "disable-gpu": "",
        "disable-gpu-compositing": "",
        "enable-begin-frame-scheduling": "",
        "disable-surfaces": "",
        "disable-smooth-scrolling": "",
    }
    browser_settings: Dict[str, int] = {
        "windowless_frame_rate": 60,
    }
    cef.Initialize(settings=settings, switches=switches)
    create_browser(browser_settings)

    # Enter loop
    cef.MessageLoop()

    # Cleanup
    cef.Shutdown()

# Create a browser
def create_browser(settings) -> None:

    # just for testing purposes
    path: str = "./html/index.html"
    URL: str = "file:///" + os.path.abspath(path)

    parent_window_handle = 0
    window_info = cef.WindowInfo()
    window_info.SetAsOffscreen(parent_window_handle)
    browser = cef.CreateBrowserSync(window_info=window_info, settings=settings)
    browser.SetClientHandler(RenderHandler())
    browser.SendFocusEvent(True)
    browser.WasResized() # tell CEF that viewport size is available and OnPaint may be called

# Exit the application
def exit_app(browser) -> None:
    browser.CloseBrowser()
    cef.QuitMessageLoop()

# Compose viewport for display (collect screen pixels, blacken censored term)
def save(buffer: str) -> None:
    image = Image.frombytes("RGBA", VIEWPORT_SIZE, buffer,
                        "raw", "RGBA", 0, 1)
    # Save image
    if not os.path.isdir('./dataset'):
        os.mkdir('./dataset')
    image.save('./dataset/test.png', 'PNG')
    print('./dataset/test.png')

# Handle the rendering
class RenderHandler(object):
    def GetViewRect(self, rect_out: [int], **_) -> None:
        global VIEWPORT_SIZE

        rect_out.extend([0, 0, VIEWPORT_SIZE[0], VIEWPORT_SIZE[1]])
        return True

    def OnPaint(self, browser, element_type, paint_buffer, **_) -> None:

        if element_type == cef.PET_VIEW:
            buffer: str = paint_buffer.GetBytes(mode="bgra", origin="top-left")

            # Tell CEF to redraw
            #cef.PostTask(cef.TID_UI, save)
            save(buffer)

# Python voodoo
if __name__ == '__main__':
    main()