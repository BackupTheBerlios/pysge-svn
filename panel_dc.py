import wx

class panel_dc(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self,parent,-1,wx.DefaultPosition,wx.DefaultSize,wx.SUNKEN_BORDER)
        self.InitBuffer()
        #self.Bind(wx.EVT_PAINT, self.OnPaint)

    def GetDC(self):
        return wx.BufferedDC(wx.ClientDC(self),self.buffer)

    def InitBuffer(self):
        size = self.GetClientSize()
        self.buffer = wx.EmptyBitmap(size.width, size.height)
        #self.buffer = wx.EmptyBitmap(800, 600)
        #dc = wx.BufferedDC(None, self.buffer)
        dc = self.GetDC()
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()
