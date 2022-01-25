try:
    from common_libs import base_classes
except:
    import base_classes
    
class debugManager(base_classes.baseManager):
    def onInit(self,default = False):
        self.default = default
        self.debug = default

    def setDefault(self,value):
        self.default = value
        
    def setToDefault(self):
        self.debug = self.default

    def setTrue(self):
        self.debug = True

    def setFalse(self):
        self.debug = False

    def cycle(self):
        if self:
            self.setFalse()
        else:
            self.setTrue()

    def get(self):
        return bool(self)

    def __bool__(self):
        return self.debug
