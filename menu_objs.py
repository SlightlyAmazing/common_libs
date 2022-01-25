try:
    from common_libs import settings_manager
    from common_libs import game_manager
    from common_libs import base_classes
    from common_libs import pygame_interface
    from common_libs import Xy as Xy_
except:
    import settings_manager
    import game_manager
    import base_classes
    import pygame_interface
    import Xy as Xy_

import pygame as pyg
from time import sleep

settingsManager = settings_manager.settingsManager()
pygameManager = pygame_interface.pygameManager
gameManager = game_manager.gameManager
Xy = Xy_.Xy

normal_color = (0,0,255)    #blue
hover_color = (0,0,50)
bg_color = (255,255,0)      #yellow

class menuManager(base_classes.baseManager):

    Scene = None

    def onInit(self):
        gameManager.Current.registerObj(self)
        self.buildGUI()

    def buildGUI(self):
        pass

    def onEarlyUpdate(self):
        gameManager.Current.scenes[type(self).Scene].fill(bg_color)

    def menuInputHandler(self,events):
        for event in events:
            if event.type == pyg.MOUSEMOTION:
                with self.managed_lock:
                    indexes = pyg.Rect(Xy(event.pos)-pygameManager.Current.offset+Xy(-1),Xy(1)).collidelistall(self.Managed)
                    for index in indexes:
                        self.Managed[index].onHover()
                    for index in range(0,len(self.Managed)):
                        if index not in indexes:
                            self.Managed[index].onNoHover()
            if event.type == pyg.MOUSEBUTTONUP:
                if event.button == 1:
                    with self.managed_lock:
                        indexes = pyg.Rect(Xy(event.pos)-pygameManager.Current.offset+Xy(-1),Xy(1)).collidelistall(self.Managed)
                        for index in indexes:
                            self.Managed[index].onClick()
        for item in self.Managed:
            item.inputHandler(events)
            
    def onDestroy(self):
        gameManager.Current.unRegisterObj(self)

class menuObject(base_classes.baseObject):
    
    def onInit(self,text,xy,*args):
        self.text = text
        self.font = pygameManager.Current.font
        self.xy = xy
        self.onInitialisation(*args)
        self.surface = self.font.render(self.text,False,normal_color)
        self.rect = pyg.Rect(self.xy,self.surface.get_size())
        self.hover = False
        self.scene = type(self).Manager.Scene

    def inputHandler(self,events):
        pass
    
    def onUpdate(self):
        if self.active:
            gameManager().Current.scenes[self.scene].blit(self.surface,self.xy)

    def onHover(self):
        if not self.hover:
            self.surface = self.font.render(self.text,False,hover_color)
            self.hover = True
            
    def onNoHover(self):
        if self.hover:
            self.surface = self.font.render(self.text,False,normal_color)
            self.hover = False

    def onClick(self):
        pass
        
    def __hash__(self):
        return hash((self.xy,self.text))

class displayMenuObject(menuObject):

    def onHover(self):
        pass

    def onNoHover(self):
        pass

    def onUpdate(self):
        if self.active:
            self.updateSurface()
        super().onUpdate()

    def onInitialisation(self):
        self.updateSurface()
        
    def updateSurface(self):
        pass
    
class callBackMenuObject(menuObject):

    def onClick(self):
        sleep(0.2)
        self.call_back(*self.args)
        self.Manager.Current.exit()

    def onInitialisation(self,call_back,*args):
        self.call_back = call_back
        self.args = args

class settingsMenuObject(menuObject):

    def onInit(self,xy,setting):
        self.setting = setting
        super().onInit(self.setting.name,xy)

    def onInitialisation(self):
        self.text = self.setting.name +": "+ str(self.setting.value)
        self.surface = self.font.render(self.text,False,normal_color)

class settingsDisplayMenuObject(displayMenuObject):

    def onInit(self,xy,setting):
        self.setting = setting
        super().onInit(self.setting.name,xy)
        self.font = pygameManager.Current.small_font
        

    def onInitialisation(self):
        self.updateSurface()

    def updateSurface(self):
        self.text = self.setting.name +": "+ str(self.setting.value)
        self.surface = self.font.render(self.text,False,normal_color)

class multipleChoiceSettingsMenuObject(settingsMenuObject):

    def onClick(self):
        self.setting.increment()
        self.text = self.setting.name +": "+ str(self.setting.value)
        self.surface = self.font.render(self.text,False,hover_color)

class textSettingsMenuObject(settingsMenuObject):

    def onInitialisation(self,setting):
        self.write = False
        self.data = ""
        super().onInitialisation(setting)

    def onUpdate(self):
        if self.write:
            self.text = self.setting.name +": "+ str(self.data)
            self.surface = self.font.render(self.text,False,hover_color)
        super().onUpdate()

    def onClick(self):
        if not self.write:
            self.write = True
            self.data = ""

        else:
            self.write = False
            self.hover = True
            if self.data != "":
                if self.data not in self.setting.values:
                    self.setting.values.append(self.data)
                self.setting.value = self.data
    
    def inputHandler(self,events):
        if self.write:
            for event in events:
                if event.type == pyg.KEYDOWN:
                    if event.key == pyg.K_RETURN:
                        self.onClick()
                    else:
                        self.data = self.data + str(pyg.key.name(event.key))
