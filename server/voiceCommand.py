from subprocess import call
import speech_recognition as sr
from pydub import AudioSegment
from pydub.playback import play

from web_client import WebClient

class VoiceCommand:
    def __init__(self):
        self._r= sr.Recognizer()
        self._wc = WebClient()

    def listen(self):
        with sr.Microphone(device_index = 0) as source:
            self._r.adjust_for_ambient_noise(source)
            print("Say Something");
            audio = self._r.listen(source)
            print("got it");
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
            audio1 = self.listen()
            text = self.voice(audio1)
            if text == 'hello' or text == "Americano" or text == "Bob":
                text = {}
                #reader_voice = AudioSegment.from_wav('/home/pi/yes_please.wav')
                #play(reader_voice)
                call(["espeak", "-s140  -ven+18 -z" ," Yes Please"])
                audio = self.listen()
                text = self.voice(audio, True);
                if text != 0:
                    print (text)
                    self._wc.sendMessage(text)
                    call(["espeak", "-s140 -ven+18 -z" , "Your command is " + text])
                else:
                    call(["espeak", "-s140 -ven+18 -z" , " Please repeat"])
            

if __name__ == '__main__':
    vc = VoiceCommand()
    vc.main()
        
