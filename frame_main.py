import wx
import os
import traceback
import time
import pysge_globals
from appmanager import appmanager
from appinterface import appinterface
from panel_dc import panel_dc
from dialog_load import dialog_load

ID_MENU_FILE_LOAD = wx.NewId()
ID_MENU_FILE_UNLOAD = wx.NewId()
ID_MENU_FILE_ABOUT = wx.NewId()
ID_MENU_FILE_EXIT = wx.NewId()
ID_FRAME_MAIN = wx.NewId()
filewildcard = "Python source (*.py)|*.py|"     \
               "Compiled Python (*.pyc)|*.pyc|" \
               "All files (*.*)|*.*"

def handle_exc(message):
    print message
    traceback.print_exc()

class frame_main(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,ID_FRAME_MAIN,"PySGE",wx.DefaultPosition,(800,600),wx.DEFAULT_FRAME_STYLE)

        self.CreateMainStatusBar()
        self.CreateMainMenu()
        self.CreateDrawingPanel()

        self.appMan = appmanager()
        self.appInt = appinterface(self.appMan,self.panelDC)

        wx.EVT_CLOSE(self, self.evt_close)
        wx.EVT_SIZE(self, self.evt_size)

    def CreateMainStatusBar(self):
        self.CreateStatusBar()
        #self.SetStatusText("Welcome to " + pysge_globals.appname + " version " + pysge_globals.version + " (" + pysge_globals.tag + ")")
        
    def CreateMainMenu(self):

        # File
        menu_file = wx.Menu()
        menu_file.Append(ID_MENU_FILE_ABOUT, "&About", "About " + pysge_globals.appname)
        menu_file.AppendSeparator()
        menu_file.Append(ID_MENU_FILE_LOAD, "&Load", "Load app")
        menu_file.Append(ID_MENU_FILE_UNLOAD, "&Unload", "Unload app")
        menu_file.AppendSeparator()
        menu_file.Append(ID_MENU_FILE_EXIT, "E&xit", "Exit " + pysge_globals.appname)
        
        menuBar = wx.MenuBar() 
        menuBar.Append(menu_file, "&File");
        
        self.SetMenuBar(menuBar)

        # Events
        # Events - File
        wx.EVT_MENU(self, ID_MENU_FILE_ABOUT, self.evt_menu_About)
        wx.EVT_MENU(self, ID_MENU_FILE_LOAD, self.evt_menu_Load)
        wx.EVT_MENU(self, ID_MENU_FILE_UNLOAD, self.evt_menu_Unload)
        wx.EVT_MENU(self, ID_MENU_FILE_EXIT, self.evt_menu_Exit)        

    def CreateDrawingPanel(self):
        #self.panelTop = wx.Panel(self,-1,wx.DefaultPosition,wx.DefaultSize,wx.SUNKEN_BORDER)
        self.panelDC = panel_dc(self)

    def LoadApp(self,filename):
        self.UnloadApp()
        if(self.appMan.LoadApp(filename)):
            # Start the thread
            self.appInt.AppLoaded()

    def UnloadApp(self):
        if(self.appMan.appLoaded):
            print "Unloading app"
            self.appInt.AppUnloaded()
            self.appMan.UnloadApp()
            print "Waiting for threads to stop running"
            running = True
            while running:
                running = self.appInt.IsRunning()
                time.sleep(0.1)
            print "App unloaded"
            self.panelDC.InitBuffer()

    def evt_close(self,event):
        self.UnloadApp()
        print "Destroying window"
        self.Destroy()

    def evt_size(self,event):
        self.appInt.Lock()
        self.panelDC.SetSize(self.GetClientSize())
        self.panelDC.InitBuffer()
        self.appInt.Unlock()
    
    def evt_menu_Load(self,event):
        #self.LoadApp("test.py")
        dlg = wx.FileDialog(self,"Choose a file",os.getcwd(),"", filewildcard, wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.LoadApp(dlg.GetPath())

    def evt_menu_Unload(self,event):
        self.UnloadApp()
    
    def evt_menu_About(self,event):            
        wx.MessageBox(pysge_globals.appname + " version " + pysge_globals.version + " (" + pysge_globals.tag + ")\n" + pysge_globals.description,"About")

    def evt_menu_Exit(self,event):
        self.Close()
