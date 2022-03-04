try:
    from common_libs import json_reader
    from common_libs import base_classes
    from common_libs import logger
    from common_libs import debug_manager
except:
    import json_reader
    import base_classes
    import logger
    import debug_manager

from time import sleep
import threading
import asyncio

logManager = logger.logManager()
debugManager = debug_manager.debugManager(True)

def echoHandler(id,data):
    return data

def echoJoinHandler(*args):
    pass

default_end_key = "!!end!!"
default_handlers = {"echoHandler":[echoHandler,2,echoJoinHandler],"noSpace":[None,-1,None]}
default_ip = 'localhost'
default_port = 8888

class serversideManager(base_classes.baseManager):

    def onInit(self,handlers = None,port = None,ip = None,end_key = None):
        serversideManager(handlers,port,ip,end_key)
        self.active = True
        if handlers == None:
            handlers = {}
        handlers |= default_handlers
        if end_key == None:
            end_key = default_end_key
        if ip == None:
            ip = default_ip
        if port == None:
            port = default_port
        self.handlers=handlers
        self.ip = ip
        self.port = port
        self.end_key = end_key
        self.semaphores = {}
        for item in self.handlers:
            if self.handlers[item][1] > 0 :
                self.semaphores[item] = threading.BoundedSemaphore(self.handlers[item][1])
            else:
                self.semaphores[item] = threading.BoundedSemaphore(99)
        asyncio.run(self.awaitablePrep())

    async def awaitablePrep(self):
        self.server = await asyncio.start_server(self.handlerJoin,self.ip,self.port)
        self.addr = self.server.sockets[0].getsockname()
        logManager.Current.logInfo(f'Serving on {self.addr}')
        if debugManager.Current:
            print(f'Serving on {self.addr}')
        async with self.server:
            await self.server.serve_forever()
            
    async def handlerJoin(self,reader,writer):
        data = await reader.readuntil(self.end_key.encode())
        data = json_reader.decodeJson(data.decode().removesuffix(self.end_key))
        if "Id" in data.keys():
            Id = data["Id"]
        if "Type" in data.keys():
            handler = data["Type"]
        if self.semaphores[handler].acquire(timeout=0.5):
            try:
                self.handlers[handler][2](Id)
                client_obj = serversideClient(reader,writer,Id,self.handlers[handler][0],handler)
                await client_obj.start()
            finally:
                self.semaphores[handler].release()
        else:
            with self.semaphores["noSpace"]:
                await reader.readuntil(self.end_key.encode())
                writer.write((json_reader.encodeJson({"Error":("No space in "+self.ip+":"+str(self.port)+"; Maximum of "+str(self.max)+" reached.")})+self.end_key).encode())
                await writer.drain()
                writer.close()

    def onExit(self):
        self.active = False
        logManager.Current.logInfo(f'Closed serving')
        if debugManager.Current:
            print(f'Closed Serving')

    def onDestroy(self):
        self.server.close()

class serversideClient(base_classes.baseObject):

    Manager = serversideManager

    def onInit(self,reader,writer,Id,handler,clientType):
        self.active = True
        self.reader = reader
        self.writer = writer
        self.id = Id
        self.handler = handler
        self.exit_message = ""
        self.type = clientType

    async def start(self):
        about = self.writer.get_extra_info('peername')
        self.writer.write((json_reader.encodeJson({self.id:"received"})+type(self).Manager.Current.end_key).encode())
        logManager.Current.logInfo("Conected to '"+ str(self.id) + "' on " + str(about))
        if debugManager.Current:
            print("Conected to '"+ str(self.id) + "' on " + str(about))
        while type(self).Manager.Current.active and self.active:
            await self.loop()
        self.writer.write((json_reader.encodeJson({"Exit":{"Message":self.exit_message}})+type(self).Manager.Current.end_key).encode())
        logManager.Current.logInfo("Lost conection to '"+ str(self.id) + "' on " + str(about)+". Message: "+self.exit_message)
        if debugManager.Current:
            print("Lost conection to '"+ str(self.id) + "' on " + str(about)+". Message: "+self.exit_message)

    async def loop(self):
        to_send = ""
        await self.writer.drain()
        data = await self.reader.readuntil(type(self).Manager.Current.end_key.encode())
        data = json_reader.decodeJson(data.decode().removesuffix(type(self).Manager.Current.end_key))
        if "Exit" in data.keys():
            self.exit()
            self.exit_message = data["Exit"]["Message"]
        if self.id in data.keys():
            to_send = self.handler(self.id,data[self.id])
        to_send = (json_reader.encodeJson({self.id:to_send})+type(self).Manager.Current.end_key).encode()
        self.writer.write(to_send)

    def onExit(self):
        self.exit_message = "Connection Closed"
        self.active = False
                    
class clientsideManager(base_classes.baseManager):

    def onInit(self,Id,ip,port,first_message,server_handler = None,client_handler= None,end_key = None):
        self.exit_message = ""
        self.id = Id
        if end_key == None:
            end_key = default_end_key
        self.end_key = end_key
        if client_handler == None:
            client_handler = echoHandler
        if server_handler == None:
            server_handler = "echoHandler"
        self.handler = client_handler
        self.active = True
        asyncio.run(self.start(ip,port,server_handler,first_message))
        
    async def start(self,ip,port,server_handler,message):
        self.reader,self.writer = await asyncio.open_connection(ip,port)
        self.writer.write((json_reader.encodeJson({"Id":self.id,"Type":server_handler})+self.end_key).encode())
        data = await self.reader.readuntil(self.end_key.encode())
        data = json_reader.decodeJson(data.decode().removesuffix(self.end_key))
        if self.id in data.keys():
            if data[self.id] == "received":
                self.writer.write((json_reader.encodeJson({self.id:message})+self.end_key).encode())
                while self.active:
                    await self.loop()
        elif "Error" in data.keys():
            logManager.Current.logError(data["Error"])
            self.writer.close()
            await self.writer.wait_closed()
        self.writer.write((json_reader.encodeJson({"Exit":{"Message":self.exit_message}})+self.end_key).encode())
        
    async def loop(self):
        to_send = ""
        await self.writer.drain()
        data = await self.reader.readuntil(self.end_key.encode())
        data = json_reader.decodeJson(data.decode().removesuffix(self.end_key))
        if "Exit" in data.keys():
            logManager.Current.logWarning(data["Exit"]["Message"])
            self.exit()
        if self.id in data.keys():
            to_send = self.handler(data[self.id])
        to_send = (json_reader.encodeJson({self.id:to_send})+self.end_key).encode()
        self.writer.write(to_send)

    def onExit(self):
        self.exit_message = "Connection closed"
        self.active = False
