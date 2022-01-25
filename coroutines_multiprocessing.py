try:
    from common_libs import base_classes
except:
    import base_classes
    
import multiprocessing

class processManager(base_classes.baseManager):

    def onInit(self):
        self.active = True

    def holdForTasks(self,*tasks):
        if len(tasks) != 0:
            process = self.createProcess(*tasks)
        else:
            process = self.Managed
        for proces in process:
            proces.holdUntilDone()

    def startTasks(self,*tasks):
        process = self.createProcess(*tasks)

    def stopTasks(self,*tasks):
        process = self.stopProcess(*tasks)

    def createProcess(self,*tasks):
        process = []
        for task in tasks:
            process.append(proces(task[0],*task[1:]))
        return process

    def stopProcess(self,*tasks):
        process = []
        for proces in self.Managed:
            for task in tasks:
                if proces.func == task[0] and proces.args == task[1:]:
                    process.append(proces)
                    proces.exit()
        return process

    def onExit(self):
        self.active = False

class proces(base_classes.baseObject):

    Manager = processManager

    def onInit(self, func, *args, **keyargs):
        self.func = func
        self.args = args
        self.keyargs = keyargs
        self.t = multiprocessing.Process(target = self.func, args = self.args, kwargs = self.keyargs)
        self.t.start()

    def holdUntilDone(self):
        self.t.join()

    def hash(self):
        return (str(self.t))

