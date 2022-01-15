from subprocess import call
import speech_recognition as sr
from pydub import AudioSegment
from pydub.playback import play

from web_client import WebClient
from WolfAssistant import BotAssistant
import subprocess
import pyttsx3
import pyaudio
import logging
from datetime import datetime



class VoiceCommand:
    def __init__(self):
        now = datetime.now()

        current_time = now.strftime("%H_%M_%S")
        logging.basicConfig(filename='/home/pi/logs/voiceCommand.log' + "_" + current_time, encoding='utf-8', level=logging.DEBUG, 
                            format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        self._r= sr.Recognizer()
        self._wc = WebClient()
        self._assist = BotAssistant()
        self._engine = pyttsx3.init()
        rate = self._engine.getProperty('rate')   # getting details of current speaking rate        
        self._engine.setProperty('rate', 125)     # setting up new voice rate
        self._device_index = 1
        audio = pyaudio.PyAudio() # create pyaudio instantiation
        # create pyaudio stream
        for ii in range(audio.get_device_count()):
            logging.debug (ii)
            dev_name = audio.get_device_info_by_index(ii).get('name')
            logging.debug(dev_name)
            if ("USB PnP Sound Device: Audio" in dev_name):
                self._device_index = ii
        logging.debug("device index = " + str(self._device_index))
     
    # Function to convert text to
    # speech
    def SpeakText(self, command):
        logging.debug(command);

        self._engine.say(command) 
        self._engine.runAndWait();

    def listen(self, timeLimit=None):
        while True:
            with sr.Microphone(device_index=self._device_index) as source:
                try:
                    self._r.adjust_for_ambient_noise(source)
                    logging.debug("Say Something");
                    audio = self._r.listen(source, phrase_time_limit=timeLimit, timeout = (timeLimit+2))
                    logging.debug("got it");                    
                except Exception as e:
                    logging.error ("error got exception" + str(e))
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
                self.SpeakText("Bob could not understand")
                #call(["espeak", "-s140  -ven+18 -z" , "Bob could not understand"])
                logging.warning("Bob could not understand")
            return 0
        except sr.RequestError as e:
            if (notify_error):
                self.SpeakText("Could not request results from Bob");
                #call(["espeak", "-s140  -ven+18 -z" , "Could not request results from Bob"])
                logging.warning("Could not request results from Bob")
            return 0

    def parse_text(self):

        for i in range(5):
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

                if ("what" in text_lower or
                    "why" in text_lower or 
                    "who" in text_lower or 
                    "where" in text_lower or
                    "when" in text_lower or
                    "do you" in text_lower):
                    self.SpeakText("Your command is " + text)
                    #call(["espeak", "-s140 -ven+18 -z" , "Your command is " + text])
                    try:
                        answer = self._assist.answerQ(text_lower)
                        self.SpeakText("Bob know master, the answer is " + answer);
                        logging.debug("Bob know master, the answer is " + answer);
                        #call(["espeak", "-s100 -ven+18 -z" , "Bob know master, the answer is:" + answer])
                    except:
                        self.SpeakText("Bob does not know");
                        #call(["espeak", "-s140 -ven+18 -z" , "Bob does not know"])
                        pass
                elif 'play music' in text or "play song" in text:
                    self.SpeakText("Here you go with music");
                    #call(["espeak", "-s140 -ven+18 -z" ,"Here you go with music"])
                    # music_dir = "G:\\Song"
                    #music_dir = "C:\\Users\\GAURAV\\Music"
                    #songs = os.listdir(music_dir)
                    #print(songs)

                    #random = os.startfile(os.path.join(music_dir, songs[1]))
                else:
                    self._wc.sendMessage(text)
                    self.SpeakText("Your command is " + text);
                    #call(["espeak", "-s140 -ven+18 -z" , "Your command is " + text])
                return
            else:
                self.SpeakText("Please repeat");
                #call(["espeak", "-s140 -ven+18 -z" , " Please repeat"])
            
    def main(self):
        #call(["espeak", "-s140  -ven+18 -z" ,"Bob is ready to serve"])
        self.SpeakText("Bob is ready to serve");
        while(True):            
            audio1 = self.listen(2)
            text = self.voice(audio1)
            if (text == 0):
                continue
            if 'hello' in text or "Americano" in text or "Bob" in text or "bob" in text or "bub" in text:
                self.parse_text()
                
                
            

if __name__ == '__main__':
    vc = VoiceCommand()
    vc.main()
        
