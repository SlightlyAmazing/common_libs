try:
    from common_libs import base_classes
    from common_libs import coroutines_threads as coroutines
    from common_libs import Xy as Xy_
except:
    import base_classes
    import coroutines_threads as coroutines
    import Xy as Xy_

import math
import pygame as pyg
import sys
from threading import Timer,Lock
from time import sleep

import os

threadManager = coroutines.threadManager()
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
        self.instructs = {}
        self.instructs_pos = {}
        self.inputs = {}
        self.delta_time = 0
        self.instructs_lock = Lock()
        self.inputs_lock = Lock()
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
        #print("hi "+new_scene)
        sleep(0.25)
        self.scene = new_scene
        if self.scene in self.scene_change_handlers:
            for func in self.scene_change_handlers[self.scene]:
                func()

    def start(self):
        #print("start")
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
        tasks = [[self.updateInput,events]]
        if self.scene in self.handlers:
            tasks.extend([([handler,events]) for handler in self.handlers[self.scene]])
        else:
            tasks.extend([([handler,events]) for handler in self.handlers["_default"]])
        #print(tasks)
        threadManager.Current.holdForTasks(*tasks)

    def updateInput(self,events):
        with self.inputs_lock:
            if self.scene not in self.inputs.keys():
                self.inputs.update({self.scene:{"Keys":[],"MouseClick":[]}})
            for event in events:
                if event.type == pyg.KEYDOWN:
                    self.inputs[self.scene]["Keys"].append({"Key":event.key})
                elif event.type == pyg.MOUSEBUTTONDOWN:
                    self.inputs[self.scene]["MouseClick"].append({"Pos":Xy(event.pos),"Button":event.button})

    def getInput(self,scene):
        with self.inputs_lock:
            return self.inputs.pop(scene,{"Keys":[{"Key":""}],"MouseClick":[{"Pos":"","Button":""}]})

    def updateScene(self,scene,color,rect):
        with self.instructs_lock:
            if scene not in self.instructs.keys():
                self.instructs.update({scene:{"Rects":[]}})
                self.instructs_pos.update({scene:[]})
            self.updateSceneUnSafe(scene,color,rect)
            
    def updateSceneUnSafe(self,scene,color,rect):
        self.scenes[scene].fill(color,rect)
        xy =Xy(rect.left,rect.top)
        if xy not in self.instructs_pos[scene]:
            self.instructs_pos[scene].append(xy)
            self.instructs[scene]["Rects"].append({"Pos":xy,"Size":Xy(rect.width,rect.height),"Color":color})

    def getInstructions(self,scene):
        with self.instructs_lock:
            self.instructs_pos.pop(scene,[])
            return self.instructs.pop(scene,{"Rects":[{"Pos":Xy(0),"Size":Xy(0),"Color":(0,0,0)}]})

    def removeInputHandler(self,scene,handler):
        with self.inputs_lock:
            if scene in self.handlers:
                if handler in self.handlers[scene]:
                    self.handlers[scene].pop(self.handlers[scene].index(handler))

    def onDestroy(self):
        sys.exit()
