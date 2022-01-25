try:
    from common_libs import json_reader
    from common_libs import logger
    from common_libs import base_classes
    from common_libs import settings_manager as settings
except:
    import json_reader
    import logger
    import base_classes
    import settings_manager as settings

default_lang = "default"
default_uri = "data/locales"
default_extension = "locale"
settings_file_name = "locale"

logManager = logger.logManager
logManager()
settingsManager = settings.settingsManager
settingsManager()
    
class localisationManager(base_classes.baseManager):
        
    def onInit(self,uri=None,ext=None):
        self.uri = uri if uri != None else default_uri
        self.ext = ext if ext != None else default_extension
        self.quick_dir = {}
        settingsManager.Current.addSettingsFile(self.uri,settings_file_name)
        self.addLangs(settingsManager.Current.getSetting("lang").values)
            

    def addLang(self, lang):
        if lang in self.quick_dir.keys():
            return
        exists = False
        try:
            open(self.uri+"/"+lang+"."+self.ext)
            exists = True
        except FileNotFoundError:
            logManager.Current.logError("locale file not in directory or doesn't exist "+str(lang))
        if exists:
            self.quick_dir[lang] = json_reader.read(self.uri, lang, self.ext)
        logManager.Current.logInfo("locale '"+lang+"' correctly loaded")

    def addLangs(self, langs):
        for lang in langs:
            self.addLang(lang)
    
    def getString(self,path):
        path = path.split("/")
        string = self.quick_dir[settingsManager.Current.getSetting("lang").value]
        for path_point in path:
            string = string[path_point]
        return string

