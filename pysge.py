import wx
import traceback
from frame_main import frame_main

def handle_exc(message):
    print message
    traceback.print_exc()

class pySgeApp(wx.App):
    def OnInit(self):
        try:
            self.mainFrame = frame_main()
            self.mainFrame.Show()
            self.SetTopWindow(self.mainFrame)
        except:
            handle_exc("Error on application init:")
        return True

if __name__ == '__main__':
    app = pySgeApp(0)
    app.MainLoop()
