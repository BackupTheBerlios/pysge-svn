import math
import wx

frames = 0
posx = 100
posy = 100
count = 10
space = 20
factor = 10.0
strtext = "PySGE"
strlen = len(strtext)

def app_Name():
    return "Sample App - Text"

def app_GetSettings():
    settings = {"fps":100}
    return settings

def app_FrameEvent(dc):
    global frames
    frames = frames + 1
    dc.SetBackground(wx.Brush("BLACK"))
    dc.SetTextForeground("RED")
    dc.Clear()
    i = frames/factor
    dc.DrawText("Frame %i" % frames, 10, 10)
    for c in range(0,count):
        l = int(math.fmod(i+c,strlen+1))
        dc.DrawText(strtext[:l], posx, posy+(space*c))
