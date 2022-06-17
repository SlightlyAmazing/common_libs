try:
    from common_libs import base_classes
except:
    import base_classes

import time
from threading import Timer

class callbackManager(base_classes.baseManager):

    def onInit(self):
        pass

    def call(self,Id):
        with self._managed_lock:
            for obj in self._Managed:
                if obj.Id == Id:
                    obj.call()

class callback(base_classes.baseObject):

    Manager = callbackManager

    def onInit(self,Id,callback,*args):
        self.Id = Id
        self.callback = callback
        self.args = args
        self.call()

    def call(self):
        self.callback(*self.args)

class timedCallback(callback):

    def onInit(self,Id,time,callback,*args):
        self.interval = time
        self.active = False
        super().onInit(Id,callback,*args)

    def startTimer(self):
        if self.active:
            self.callback(*self.args)
            self.timer = Timer(self.interval,self.startTimer)
            self.timer.start()

    def call(self):
        if self.active:
            self.timer.cancel()
            self.active = False
        else:
            self.timer = Timer(self.interval,self.startTimer)
            self.timer.start()
            self.active = True
