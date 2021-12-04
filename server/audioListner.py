import json
from os.path import join, dirname
import sys
sys.path.append("/home/pi/proj/tjbot_py/python-sdk")

from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource
import threading
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import pyaudio
import wave
import time



SPEECH_TO_TEXT_APIKEY='I7Y2iGojqvT2_uSdEuG3kmNZLGk7ukXi-4bNsmchiKyl'
SPEECH_TO_TEXT_IAM_APIKEY='I7Y2iGojqvT2_uSdEuG3kmNZLGk7ukXi-4bNsmchiKyl'
SPEECH_TO_TEXT_URL='https://api.eu-gb.speech-to-text.watson.cloud.ibm.com/instances/57375813-c4cd-4854-92e5-0488220f92d2'
SPEECH_TO_TEXT_AUTH_TYPE='iam'
TEXT_TO_SPEECH_APIKEY='0O2IC4fdwP7FS5mZCAjAse7llGbDraMYOXrW61kCVjzp'
TEXT_TO_SPEECH_IAM_APIKEY='0O2IC4fdwP7FS5mZCAjAse7llGbDraMYOXrW61kCVjzp'
TEXT_TO_SPEECH_URL='https://api.eu-gb.text-to-speech.watson.cloud.ibm.com/instances/3269041f-c51f-4afd-b0a4-f547aabecafc'
TEXT_TO_SPEECH_AUTH_TYPE='iam'
ASSISTANT_APIKEY='aOh5wfE4uEp5w3UsKFbpXoen-WhEJEKD4MDajjMZGIcS'
ASSISTANT_IAM_APIKEY='aOh5wfE4uEp5w3UsKFbpXoen-WhEJEKD4MDajjMZGIcS'
ASSISTANT_URL='https://api.eu-gb.assistant.watson.cloud.ibm.com/instances/c493187f-e2b3-41f3-95e8-ebb01df50ada'
ASSISTANT_AUTH_TYPE='iam'

data = ""
done = False
# Example using websockets
class MyRecognizeCallback(RecognizeCallback):
    def __init__(self):
        global done,data
        RecognizeCallback.__init__(self)
        done = False
        data = ""

    def on_transcription(self, transcript):
        global done, data
        print(transcript)
        data = transcript[0][0]['transcript']
        print(data)
        if ("light" in data):
            data = "lights"
        elif ("forward" in data):
            data = "forward"
        elif ("backward" in data):
            data = "backward"
        elif ("left" in data):
            data = "left"
        done = True


    def on_connected(self):
        print('Connection was successful')

    def on_error(self, error):
        print('Error received: {}'.format(error))

    def on_inactivity_timeout(self, error):
        print('Inactivity timeout: {}'.format(error))

    def on_listening(self):
        print('Service is listening')

    def on_hypothesis(self, hypothesis):       
        print("on hypo" + hypothesis)
        pass
    
    def on_data(self, data):
        global done
        print("on data" + str(data))
        done = True
        data = ""
        pass

class AudioListner():
    def __init__(self):
        #threading.Thread.__init__(self)
        self.authenticator = IAMAuthenticator(SPEECH_TO_TEXT_APIKEY)
        self.service = SpeechToTextV1(authenticator=self.authenticator)
        self.service.set_service_url(SPEECH_TO_TEXT_URL)

    def parse_output(self, file):
        # Example using threads in a non-blocking way
        mycallback = MyRecognizeCallback()
        audio_file = open(join(dirname(__file__), file), 'rb')
        audio_source = AudioSource(audio_file)
        recognize_thread = threading.Thread(
        target=self.service.recognize_using_websocket,
        args=(audio_source, "audio/l16; rate=44100", mycallback))
        recognize_thread.start()

    #def run(self):
    #    while True:
    #        time.sleep(10)

    def wait_for_output(self):
        while (done == False):
            print ("Listening")
            time.sleep(0.5)
        print ("voice output = " + data)
        return data

    def record(self):
        global done,data
        done = False
        data = ""
        form_1 = pyaudio.paInt16 # 16-bit resolution
        chans = 1 # 1 channel
        samp_rate = 44100 # 44.1kHz sampling rate
        chunk = 48000 # 2^12 samples for buffer
        record_secs = 3 # seconds to record
        dev_index = -1   # device index found by p.get_device_info_by_index(ii)
        wav_output_filename = '/home/pi/test1.wav' # name of .wav file

        
        
        audio = pyaudio.PyAudio() # create pyaudio instantiation
        # create pyaudio stream
        for ii in range(audio.get_device_count()):
            print (ii)
            dev_name = audio.get_device_info_by_index(ii).get('name')
            print(dev_name)
            if ("Plantronics Blackwire 5220 Seri" in dev_name):
                dev_index = ii

        assert(dev_index != -1)
        print("dev_index = " + str(dev_index))
        samp_rate = int(audio.get_device_info_by_index(dev_index).get('defaultSampleRate'))
        print(samp_rate)
        chunk = 4000

        print("chunk = " + str(chunk))
        stream = audio.open(format = form_1,rate = samp_rate,channels = chans, \
                    input_device_index = dev_index,input = True, \
                    frames_per_buffer=chunk)
        print("recording")
        frames = []

        # loop through stream and append audio chunks to frame array
        for ii in range(0,int((samp_rate/chunk)*record_secs)):
            print(ii)
            data = stream.read(chunk, exception_on_overflow=False)
            frames.append(data)

        print("finished recording")

        # stop the stream, close it, and terminate the pyaudio instantiation
        stream.stop_stream()
        stream.close()
        

        # save the audio frames as .wav file
        wavefile = wave.open(wav_output_filename,'wb')
        wavefile.setnchannels(chans)
        wavefile.setsampwidth(audio.get_sample_size(form_1))
        wavefile.setframerate(samp_rate)
        wavefile.writeframes(b''.join(frames))
        wavefile.close()
        self.parse_output(wav_output_filename)
        audio.terminate()
        while (done == False):
            print ("Listening")
            time.sleep(0.5)
        print ("voice output = " + data)
        return data

if __name__ == '__main__':
    listner = AudioListner()
    listner.record() 
