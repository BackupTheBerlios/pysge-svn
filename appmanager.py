import traceback

def handle_exc(message):
    print message
    traceback.print_exc()

class appmanager:
    """A dynamic module loader for a single module"""
    def __init__(self):
        self.currentApp = {}
        self.appLoaded = False
    
    def ExecFunction(self,name,*params):
        if(self.appLoaded):
            #print "Executing function: %s with parameters: %s" % (name,params)
            try:
                return self.currentApp[name](*params)
            except Exception, e:
                handle_exc("Function '%s' with parameters '%s' could not be executed:" % (name,params))
                raise
        
    def LoadApp(self,filename):
        try:
            execfile(filename,self.currentApp)
            print "Loaded app:",filename
            self.appLoaded = True
            return True
        except Exception, e:
            handle_exc("App '" + filename + "' could not be loaded:")
            return False

    def UnloadApp(self):
        if(self.appLoaded):
            self.currentApp = {}
            self.appLoaded = False
