try:
    from common_libs import base_classes
    from common_libs import logger
except:
    import base_classes
    import logger

import asyncio

logManager = logger.logManager
logManager()
    
class taskManager(base_classes.baseManager):

    def prep(self,task,*formargs):
        self.running = True
        self.tasks = []
        asyncio.run(self.controller(task,*formargs))

    def changeValues(self,*formargs):
        self.tasks.extend(self.addTasks(*formargs))
    
    def addTasks(self,task,*formargs):
        tasks = [[task[0],task[1:]]]
        for task in formargs:
            tasks.append([task[0],task[1:]])
        return tasks

    def createAsyncThreads(self, tasks):
        threads = []
        for task in tasks:
            thread = asyncio.to_thread(task[0],*task[1])
            threads.append(thread)
        return threads
        
    async def controller(self,task,*formargs):
        tasks = self.addTasks(task,*formargs)
        while self.running:
            self.currentTasks = self.createAsyncThreads(tasks)
            self.currentTasks.extend(self.createAsyncThreads(self.tasks))
            await asyncio.gather(*self.currentTasks)

    def onExit(self):
        self.running = False
    
