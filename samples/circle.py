import math
import wx

frames = 0
posx = 300
posy = 300
radius = 100
factor = 100.0

def app_Name():
    return "Sample App - Circle"

def app_GetSettings():
    settings = {"fps":30}
    return settings

def app_FrameEvent(dc):
    #global frames, posx, posy, radius, factor
    global frames
    frames = frames + 1
    dc.SetBackground(wx.Brush("SEA GREEN"))
    dc.Clear()
    i = frames/factor
    r = math.sin(i)*radius
    x = (math.sin(i)*radius)+posx
    y = (math.cos(i)*radius)+posy
    dc.DrawCircle(x,y,r)
    dc.DrawText("Frame %i" % frames, 10, 10)
