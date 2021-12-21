from subprocess import call
import speech_recognition as sr
from pydub import AudioSegment
from pydub.playback import play

from web_client import WebClient
from WolfAssistant import BotAssistant
import subprocess

class VoiceCommand:
    def __init__(self):
        self._r= sr.Recognizer()
        self._wc = WebClient()
        self._assist = BotAssistant()

    def listen(self, timeLimit=None):
        while True:
            with sr.Microphone(device_index = 0) as source:
                try:
                    self._r.adjust_for_ambient_noise(source)
                    print("Say Something");
                    audio = self._r.listen(source, phrase_time_limit=timeLimit, timeout = (timeLimit+2))
                    print("got it");                    
                except:
                    print ("error got exception")
                    continue
            return audio
            



    def voice(self, audio1, notify_error = False):
        try:
            text1 = self._r.recognize_google(audio1)
##     call('espeak '+text, shell=True)
            print ("you said: " + text1);
            return text1;
        except sr.UnknownValueError:
            if (notify_error):
                call(["espeak", "-s140  -ven+18 -z" , "Bob could not understand"])
                print("Bob could not understand")
            return 0
        except sr.RequestError as e:
            if (notify_error):
                call(["espeak", "-s140  -ven+18 -z" , "Could not request results from Bob"])
                print("Could not request results from Bob")
            return 0


    def main(self):
        while(True):
            audio1 = self.listen(2)
            text = self.voice(audio1)
            if (text == 0):
                continue
            if text == 'hello' or text == "Americano" or "Bob" in text or "bob" in text or "bub" in text:
                text = {}
                #reader_voice = AudioSegment.from_wav('/home/pi/yes_please.wav')
                #play(reader_voice)
                output = subprocess.Popen(["espeak", "-s140  -ven+18 -z" ," Yes Please"])
                #output.communicate()
                #call(["espeak", "-s140  -ven+18 -z" ," Yes Please"])
                audio = self.listen(10)
                text = self.voice(audio, True);
                
                if text != 0:
                    print (text)
                    text_lower = text.lower()

                    if "what" in text_lower or "why" in text_lower or "who" in text_lower or "where" in text_lower:
                        call(["espeak", "-s140 -ven+18 -z" , "Your command is " + text])
                        try:
                            answer = self._assist.answerQ(text_lower)                        
                            call(["espeak", "-s140 -ven+18 -z" , answer])
                        except:
                            call(["espeak", "-s140 -ven+18 -z" , "Bob does not know"])
                            pass

                    else:
                        self._wc.sendMessage(text)
                        call(["espeak", "-s140 -ven+18 -z" , "Your command is " + text])
                else:
                    call(["espeak", "-s140 -ven+18 -z" , " Please repeat"])
            

if __name__ == '__main__':
    vc = VoiceCommand()
    vc.main()
        
