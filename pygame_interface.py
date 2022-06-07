try:
    from common_libs import game_manager
    from common_libs import coroutines_threads
    from common_libs import base_classes
    from common_libs import Xy as Xy_
except:
    import game_manager
    import coroutines_threads
    import base_classes
    import Xy as Xy_

import pygame as pyg

# ===== initialise libs

pyg.font.init()
gameManager = game_manager.gameManager()
threadManager = coroutines_threads.threadManager()
Xy = Xy_.Xy

# ==== default functions

def defaultInputHandler(events):
    pass

# ===== default values

default_size = Xy(1920,1080)
default_caption = "pygame interface"
default_very_small_font = pyg.font.Font(pyg.font.get_default_font(),11)
default_small_font = pyg.font.Font(pyg.font.get_default_font(),20)
default_font = pyg.font.Font(pyg.font.get_default_font(),30)
default_large_font = pyg.font.Font(pyg.font.get_default_font(),40)
default_input_handler = defaultInputHandler
default_bg_color = (255,255,255)

# ===== colours

black = 0,0,0
white = 255,255,255

class pygameManager(base_classes.baseManager):
    
    def onInit(self,size=None,caption=None,input_handler = None):
        pyg.init()
        self.very_small_font = default_very_small_font
        self.small_font = default_small_font
        self.font = default_font
        self.large_font = default_large_font
        if size == None:
            size = default_size
        if caption == None:
            caption = default_caption
        if input_handler == None:
            input_handler = default_input_handler
        self.input_handler = input_handler
        self.caption = caption
        self.size = size
        self.screen = pyg.display.set_mode(self.size,pyg.RESIZABLE)
        pyg.display.set_caption(self.caption)
        self.screen.fill(white)
        self.offset = 0 
        pyg.display.flip()
        gameManager.Current.registerObj(self)
        self.active = True
        self.exiting = False
        gameManager.Current.start()

    def onEarlyUpdate(self):
        self.size = Xy(pyg.display.get_window_size())
        
    def onUpdate(self):
        events = pyg.event.get()
        if pyg.QUIT in [event.type for event in events]:
            gameManager.Current.exit()
        else:
            threadManager.Current.holdForTasks([self.input_handler,events])

    def onLateUpdate(self):
        self.screen.fill(black)
        scene = gameManager.Current.scenes[gameManager.Current.scene]
        scene_size = Xy(scene.get_size())
        screen_size = Xy(self.screen.get_size())
        if screen_size < scene_size:
            print("scene too large for current screen")
        self.offset = (screen_size-scene_size)/2
        self.screen.blit(scene,self.offset)
        pyg.display.flip()   

    def onExit(self):
        pyg.display.quit()
        
    def onDestroy(self):
        gameManager.Current.unRegisterObj(self)
        pyg.quit()
        
if __name__ == "__main__":
    pygameManager()
