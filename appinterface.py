import traceback
import time
import thread

def handle_exc(message):
    print message
    traceback.print_exc()

class appthread:
    def __init__(self, func):
        self.func = func
        self.running = False

    def Start(self,fps):
        self.fps = fps
        self.keepGoing = True
        self.running = True
        thread.start_new_thread(self.Run, ())

    def Stop(self):
        print "Stopping thread"
        self.keepGoing = False

    def IsRunning(self):
        return self.running

    def Run(self):
        print "Thread started"
        while self.keepGoing:
            try:
                self.func()
            except Exception, e:
                handle_exc("Exception in thread:")
                self.Stop()
            time.sleep(1.0/self.fps)
        self.running = False
        print "Thread stopped"

class appinterface:
    def __init__(self,appMan,panel):
        self.appMan = appMan
        self.settings = self.GetDefaultSettings()
        self.thread = appthread(self.app_FrameEvent)
        self.panel = panel
        self.locked = False

    def AppLoaded(self):
        # Get settings
        self.app_GetSettings()
        # Start thread
        self.thread.Start(self.settings["fps"])
        
    def AppUnloaded(self):
        if(self.IsRunning()):
            self.thread.Stop()

    def IsRunning(self):
        return self.thread.IsRunning()
    
    def GetDefaultSettings(self):
        settings = {"fps":30}
        return settings

    def Lock(self):
        self.locked = True

    def Unlock(self):
        self.locked = False

    def app_FrameEvent(self):
        if(not self.locked):
            try:
                dc = self.panel.GetDC()
            except:
                print "Failed to acquire DC, TODO: Figure out why and lock this function"
                return False
            dc.BeginDrawing()
            self.appMan.ExecFunction("app_FrameEvent",dc)
            dc.EndDrawing()

    def app_GetSettings(self):
        try:
            print "Loading settings"
            settings = self.appMan.ExecFunction("app_GetSettings")
            for key in settings.keys():
                print key,"=",settings[key]
                self.settings[key] = settings[key]
            print "Loaded settings"
        except Exception, e:
            print e
            print "No settings defined in this app"
