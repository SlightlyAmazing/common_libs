from threading import Thread,Timer,Lock

Exit_Timer = 0.1

class baseClass():
    pass

class baseObject(baseClass):

    Manager = None

    def __new__(cls,*formargs,**keyargs):
        self = super().__new__(cls)
        self.init(*formargs,**keyargs)
        return self

    def init(self,*formargs,**keyargs):
        self._active = False
        type(self).Manager().Current.registerObj(self)
        self.onInit(*formargs,**keyargs)
        self._exiting = False
        self._active = True

    def onInit(self,*formargs,**keyargs):
        pass

    def earlyUpdate(self):
        if self._active:
            self.onEarlyUpdate()

    def onEarlyUpdate(self):
        pass
    
    def update(self):
        if self._active:
            self.onUpdate()

    def onUpdate(self):
        pass

    def lateUpdate(self):
        if self._active:
            self.onLateUpdate()

    def onLateUpdate(self):
        pass

    def slowUpdate(self):
        if self._active:
            self.onSlowUpdate()

    def onSlowUpdate(self):
        pass

    def exitonlySelf(self): # here for compatibility; use 'exitOnlySelf()' instead
        self.exitOnlySelf()

    def exitOnlySelf(self):
        self.exit()
        Thread(target=type(self).Manager.Current.unRegisterObj,args=(self,)).start()
        Timer(Exit_Timer,self.destroy).start()
        
    def exit(self):
        self._exiting = True
        self._active = False
        self.onExit()

    def onExit(self):
        pass

    def destroy(self):
        if type(self).Manager.Current != None:
            type(self).Manager.Current.unRegisterObj(self)
        self.onDestroy()

    def onDestroy(self):
        pass

    #must define a __hash__ method
    
class baseManager(baseClass):

    Current = None
    
    def __new__(cls,*formargs,**keyargs):
        if cls.Current == None:
            self = super().__new__(cls)
            cls.Current = self
            self.init(*formargs,**keyargs)
        cls.Current.changeValues(*formargs,**keyargs)
        return cls

    def __init__():
        #Never use __init__
        pass

    def init(self,*formargs,**keyargs):
        self._active = False
        self._Managed = []
        self._managed_lock = Lock() 
        self.onInit(*formargs,**keyargs)
        self._active = True
        self._exiting = False
        
    def onInit(self,*formargs,**keyargs):
        pass

    def changeValues(self,*formargs,**keyargs):
        pass

    def registerObj(self, obj):
        if obj not in self._Managed:
            with self._managed_lock:
                self._Managed.append(obj)

    def unRegisterObj(self, obj):
        if obj in self._Managed:
            with self._managed_lock:
                for index in range(0,len(self._Managed)):
                    if self._Managed[index] == obj:
                        self._Managed.pop(index)
                        break

    def earlyUpdate(self):
        if self._active:
            for obj in self._Managed:
                obj.earlyUpdate()
            self.onEarlyUpdate()

    def onEarlyUpdate(self):
        pass

    def update(self):
        if self._active:
            for obj in self._Managed:
                obj.update()
            self.onUpdate()

    def onUpdate(self):
        pass

    def lateUpdate(self):
        if self._active:
            for obj in self._Managed:
                obj.lateUpdate()
            self.onLateUpdate()

    def onLateUpdate(self):
        pass

    def slowUpdate(self):
        if self._active:
            for obj in self._Managed:
                obj.slowUpdate()
            self.onSlowUpdate()

    def onSlowUpdate(self):
        pass

    def exit(self):
        self._active = False
        self._exiting = True
        for obj in self._Managed:
            obj.exit()
        self.onExit()
        Timer(Exit_Timer,self.destroy).start()

    def onExit(self):
        pass

    def destroy(self):
        for obj in self._Managed:
            obj.destroy()
        self.onDestroy()
        type(self).Current = None

    def onDestroy(self):
        pass
    
class baseException(baseClass,Exception):
    pass

class baseStruct(baseClass):
    pass
    
