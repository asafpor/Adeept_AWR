import websocket
import time

class WebClient:
    def __init__(self):
        self._ws = websocket.WebSocket()
        pass

    def sendMessage(self, out_text):
        SLEEP_TIME = 1

        try:
            if ("police" in out_text and "on" in out_text):
                self._ws.connect("ws://localhost:8888")
                self._ws.send("admin:123456")
                self._ws.send("police")
            elif ("police" in out_text and "off" in out_text):
                self._ws.connect("ws://localhost:8888")
                self._ws.send("admin:123456")
                self._ws.send("policeOff")
            elif ("forward" in out_text) or (("move" in out_text) and ("straight" in out_text)):
                self._ws.connect("ws://localhost:8888")
                self._ws.send("admin:123456")
                self._ws.send("forward")
                #time.sleep(SLEEP_TIME)
                #self._ws.connect("ws://localhost:8888")
                #self._ws.send("admin:123456")
                #self._ws.send("stop")
            elif ("backward" in out_text) or (("move" in out_text) and ("back" in out_text)):
                self._ws.connect("ws://localhost:8888")
                self._ws.send("admin:123456")
                self._ws.send("backward")
                #time.sleep(SLEEP_TIME)
                #self._ws.connect("ws://localhost:8888")
                #self._ws.send("admin:123456")
                #self._ws.send("stop")
            elif ("left" in out_text):
                self._ws.connect("ws://localhost:8888")
                self._ws.send("admin:123456")
                self._ws.send("left")
                time.sleep(SLEEP_TIME)
                self._ws.connect("ws://localhost:8888")
                self._ws.send("admin:123456")
                self._ws.send("stop")
            elif ("right" in out_text):
                self._ws.connect("ws://localhost:8888")
                self._ws.send("admin:123456")
                self._ws.send("rightt")
                time.sleep(SLEEP_TIME)
                self._ws.connect("ws://localhost:8888")
                self._ws.send("admin:123456")
                self._ws.send("stop")
            elif ("stop" in out_text):
                self._ws.connect("ws://localhost:8888")
                self._ws.send("admin:123456")
                self._ws.send("stop")
            else:
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                return False
        except:
            return False
        return True


