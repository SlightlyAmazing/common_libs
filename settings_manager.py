try:
    from common_libs import base_classes
    from common_libs import json_reader
except:
    import base_classes
    import json_reader

default_path = "data"
default_name = "default"
default_ext = "settings"

class settingsManager(base_classes.baseManager):

    def onInit(self, path = None, name = None, ext = None):
        self.addSettingsFile(path,name,ext)

    def addSettingsFile(self,path = None, name = None, ext = None):
        settings = json_reader.read((path if path != None else default_path), (name if name != None else default_name), (ext if ext != None else default_ext))
        for settin in settings:
            setting(settin["name"],settin["value"],settin["values"])

    def getSetting(self,name):
        for setting in self._Managed:
            if setting.name == name:
                return setting

class setting(base_classes.baseObject):

    Manager = settingsManager
    
    def onInit(self,name,value,values):
        self.name = name
        self.values = list(values)
        self.value = value
        self.original = self.value

    def increment(self):
        self.value = self.values[(self.values.index(self.value)+1)%len(self.values)]

    def reset(self):
        self.value = self.original

    def add(self,value):
        self.value = value
        self.values.append(value)
        
    def hash(self):
        return (str(self.name),str(self.original))
