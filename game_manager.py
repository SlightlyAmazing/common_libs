try:
    from common_libs import base_classes
    from common_libs import coroutines_threads as coroutines
    from common_libs import Xy as Xy_
    from common_libs import debug_manager
except:
    import base_classes
    import coroutines_threads as coroutines
    import Xy as Xy_
    import debug_manager

import math
import pygame as pyg
import sys
from threading import Timer,Lock
from time import sleep

import os

threadManager = coroutines.threadManager()
debugManager = debug_manager.debugManager()
Xy = Xy_.Xy

def defaultUserInput(events):
    pass

def defaultSceneChange():
    pass

default_fps = 20
default_scenes = {"_default":pyg.Surface(Xy(600,600))}
default_input_handler = {"_default":[defaultUserInput]}
default_scene = "_default"
default_scene_change = {"_default":defaultSceneChange}
default_bg_color = (255,255,255)

class gameManager(base_classes.baseManager):

    def onInit(self,fps = None,scenes = None,current_scene = None,user_input_handler = None,scene_change_func = None,bg_color = None):
        self.bg_color = default_bg_color
        self.delta_time = 0
        self.scenes = {}
        self.handlers = default_input_handler
        self.scene = default_scene
        self.fps = default_fps
        self.actual_fps = default_fps
        self.past_fps = []
        self.scene_change_handlers = default_scene_change
        self.changeValues(fps,scenes,current_scene,user_input_handler,scene_change_func,bg_color)
        self.clock = pyg.time.Clock()
        self.slowUpdateTimer = 0

    def changeValues(self,fps = None,scenes = None,current_scene = None,user_input_handler = None,scene_change_func = None,bg_color = None):
        if bg_color != None:
            self.bg_color = bg_color
        if fps != None:
            self.fps = fps
        if scenes == None:
            scenes = default_scenes
        self.scenes |= scenes
        if user_input_handler != None:
            if list(user_input_handler.keys())[0] in self.handlers.keys():
                self.handlers[list(user_input_handler.keys())[0]].append(list(user_input_handler.values())[0])
            else:
                self.handlers[list(user_input_handler.keys())[0]] = [list(user_input_handler.values())[0]]
        if scene_change_func != None:
            self.scene_change_handlers |= scene_change_func
        if current_scene != None:
            self.changeScene(current_scene)
        
    def changeScene(self,new_scene):
        sleep(0.25)
        self.scene = new_scene
        if self.scene in self.scene_change_handlers:
            for func in self.scene_change_handlers[self.scene]:
                func()

    def start(self):
        self.doGame()

    def doGame(self):
        self.clock.tick()
        while self._active:
            threadManager.Current.cleanThreads()
            #print(os.getpid(),self.Managed)
            self.doUpdate()
            self.delta_time = self.clock.tick(self.fps) if self.fps != -1 else self.clock.tick()
            if self.delta_time == 0:
                self.delta_time = 1
            self.past_fps.append(round(1/(self.delta_time/1000)))
            if len(self.past_fps) > (self.actual_fps)*2.5:
                self.past_fps.pop(0)
            i = 0
            for fps in self.past_fps: i+= fps
            self.actual_fps = round(i/len(self.past_fps))

    def doUpdate(self):
        self.earlyUpdate()
        self.update()
        self.lateUpdate()
        self.slowUpdateTimer +=1
        if self.slowUpdateTimer > 10:
            self.slowUpdate()
        #print(self.scene)
        #print(self._Managed)

    def userInput(self,events):
        tasks = [[self.input,events]]
        if self.scene in self.handlers:
            tasks.extend([([handler,events]) for handler in self.handlers[self.scene]])
        else:
            tasks.extend([([handler,events]) for handler in self.handlers["_default"]])
        #print(tasks)
        threadManager.Current.holdForTasks(*tasks)

    def input(self,events):
        for event in events:
            if event.type == pyg.KEYUP:
                match event.key:
                    case pyg.K_F3:
                        debugManager.Current.cycle()

    def removeInputHandler(self,scene,handler):
        if scene in self.handlers:
            if handler in self.handlers[scene]:
                self.handlers[scene].pop(self.handlers[scene].index(handler))

    def onDestroy(self):
        sys.exit()
