try:
    from common_libs import base_classes
except:
    import base_classes
    
import threading

class threadManager(base_classes.baseManager):

    def onInit(self):
        self.active = True

    def holdForTasks(self,*tasks):
        if len(tasks) != 0:
            threads = self.createThreads(*tasks)
        else:
            threads = self._Managed
        for thread in threads:
            thread.holdUntilDone()

    def startTasks(self,*tasks):
        threads = self.createThreads(*tasks)

    def stopTasks(self,*tasks):
        threads = self.stopThreads(*tasks)        
   
    def createThreads(self,*tasks):
        threads = []
        for task in tasks:
            threads.append(thread(task[0],*task[1:]))
        return threads

    def getThreads(self,ignore_args,*tasks):
        threads = []
        for thread in self._Managed:
            for task in tasks:
                if thread.isAlive():
                    if thread.func == task[0] and (ignore_args or thread.args == task[1:]):
                        threads.append(thread)
        return threads
        
    def stopThreads(self,*tasks):
        threads = self.getThreads(False,*tasks)
        for thread in threads:
            thread.exitOnlySelf()
        return threads

    def cleanThreads(self):
        for thread in self._Managed:
            thread.isAlive()
            
    def onExit(self):
        self.active = False

class thread(base_classes.baseObject):

    Manager = threadManager

    def onInit(self, func, *args, **keyargs):
        self.func = func
        self.args = args
        self.keyargs = keyargs
        self.t = threading.Thread(target = self.func, args = self.args, kwargs = self.keyargs)
        self.t.start()

    def holdUntilDone(self):
        self.t.join()
        self.isAlive()

    def isAlive(self):
        if not self.t.is_alive():
            self.exitOnlySelf()
            return False
        return True

    def hash(self):
        return (str(self.t))
    

    
