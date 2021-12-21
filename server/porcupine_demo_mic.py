#
# Copyright 2018-2021 Picovoice Inc.
#
# You may not use this file except in compliance with the license. A copy of the license is located in the "LICENSE"
# file accompanying this source.
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
#

import argparse
import os
import struct
import wave
import time
from datetime import datetime
from threading import Thread

import pvporcupine
from pvrecorder import PvRecorder
import audioListner
import textToSpeech
from pygame import mixer
from pydub import AudioSegment
from pydub.playback import play
import websocket


POR_ACCESS_KEY = 'lhkG6c+GZ0d9U35msJQM2l/9EMS4o9Otq0ITLeZZG52USLn4uqdNNA=='

class PorcupineDemo(Thread):
    """
    Microphone Demo for Porcupine wake word engine. It creates an input audio stream from a microphone, monitors it, and
    upon detecting the specified wake word(s) prints the detection time and wake word on console. It optionally saves
    the recorded audio into a file for further debugging.
    """

    def __init__(
            self,
            access_key,
            library_path,
            model_path,
            keyword_paths,
            sensitivities,
            input_device_index=None,
            output_path=None):

        """
        Constructor.

        :param library_path: Absolute path to Porcupine's dynamic library.
        :param model_path: Absolute path to the file containing model parameters.
        :param keyword_paths: Absolute paths to keyword model files.
        :param sensitivities: Sensitivities for detecting keywords. Each value should be a number within [0, 1]. A
        higher sensitivity results in fewer misses at the cost of increasing the false alarm rate. If not set 0.5 will
        be used.
        :param input_device_index: Optional argument. If provided, audio is recorded from this input device. Otherwise,
        the default audio input device is used.
        :param output_path: If provided recorded audio will be stored in this location at the end of the run.
        """

        super(PorcupineDemo, self).__init__()
        print (POR_ACCESS_KEY)

        self._access_key = access_key
        self._library_path = library_path
        self._model_path = model_path
        self._keyword_paths = keyword_paths
        self._sensitivities = sensitivities
        self._input_device_index = input_device_index

        self._output_path = output_path
        self._listener = audioListner.AudioListner()
        self._textToSpeech = textToSpeech.audioPlayer()
        #mixer.init()
        self._ws = websocket.WebSocket()
        


    def run(self):
        """
         Creates an input audio stream, instantiates an instance of Porcupine object, and monitors the audio stream for
         occurrences of the wake word(s). It prints the time of detection for each occurrence and the wake word.
         """

        keywords = list()
        for x in self._keyword_paths:
            keyword_phrase_part = os.path.basename(x).replace('.ppn', '').split('_')
            if len(keyword_phrase_part) > 6:
                keywords.append(' '.join(keyword_phrase_part[0:-6]))
            else:
                keywords.append(keyword_phrase_part[0])

        porcupine = None
        recorder = None
        wav_file = None
        try:
            
            porcupine = pvporcupine.create(
               access_key=self._access_key,
                library_path=self._library_path,
                model_path=self._model_path,
                keyword_paths=self._keyword_paths,
                sensitivities=self._sensitivities)
            
            recorder = PvRecorder(device_index=self._input_device_index, frame_length=porcupine.frame_length, buffer_size_msec=10000, log_overflow = False)
            recorder.start()

            if self._output_path is not None:
                wav_file = wave.open(self._output_path, "w")
                wav_file.setparams((1, 2, 16000, 512, "NONE", "NONE"))

            print(f'Using device: {recorder.selected_device}')

            print('Listening {')
            for keyword, sensitivity in zip(keywords, self._sensitivities):
                print('  %s (%.2f)' % (keyword, sensitivity))
            print('}')
            
            while True:
                pcm = recorder.read()

                if wav_file is not None:
                    wav_file.writeframes(struct.pack("h" * len(pcm), *pcm))

                result = porcupine.process(pcm)
                if result >= 0:
                    print('[%s] Detected %s' % (str(datetime.now()), keywords[result]))
                    reader_voice = AudioSegment.from_wav('/home/pi/yes_please.wav')
                    play(reader_voice)
#                if True:                    
                    wav_file1 = wave.open('/home/pi/test2.wav', "w")
#                    wav_file1.setnchannels(1)
#                    wav_file1.setsampwidth(16000)
#                    wav_file1.setframerate(512)

                    wav_file1.setparams((1, 2, 16000, 512, "NONE", "NONE"))
                    print("start recording")
                    time.sleep(2.5)
                    print("stop recording")
                    print("start while")
                    close = True
                    for ii in range(256):
                        try:
#                            print("in while")
                            pcm = recorder.read()
 #                           print (len(pcm))
  #                          print("end recording")
                            if wav_file1 is not None:
                               wav_file1.writeframes(struct.pack("h" * len(pcm), *pcm))
                        except:
                            print ("read error")
                            close = False
                            wav_file1.close()
                            break
                    if close:
                         wav_file1.close()
                    SLEEP_TIME = 1
                    self._listener.parse_output('/home/pi/test2.wav', "audio/l16; rate=16000")
                    out_text = self._listener.wait_for_output()
                    print(out_text)
                    if out_text == "":
                        continue 
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
                            time.sleep(SLEEP_TIME)
                            self._ws.connect("ws://localhost:8888")
                            self._ws.send("admin:123456")
                            self._ws.send("stop")
                        elif ("backward" in out_text) or (("move" in out_text) and ("back" in out_text)):
                            self._ws.connect("ws://localhost:8888")
                            self._ws.send("admin:123456")
                            self._ws.send("backward")
                            time.sleep(SLEEP_TIME)
                            self._ws.connect("ws://localhost:8888")
                            self._ws.send("admin:123456")
                            self._ws.send("stop")
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
                        else:
                            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    except:
                        pass
                    
                    file_name = '/home/pi/my_output1.wav'
                    try:
                        os.remove(file_name)
                    except:
                        pass
                    self._textToSpeech.playAudio(out_text, file_name) 
                    print ("self._textToSpeech.isDone()" + str(self._textToSpeech.isDone()))
                    while self._textToSpeech.isDone() == False:
                        time.sleep(0.5)
                        print ("waiting...")
                    reader_voice = AudioSegment.from_wav(file_name)
                    play(reader_voice)
                    #sound = mixer.Sound(file_name)
                    #sound.play()



 

        except KeyboardInterrupt:
            print('Stopping ...')
        finally:
            if porcupine is not None:
                porcupine.delete()

            if recorder is not None:
                recorder.delete()

            if wav_file is not None:
                wav_file.close()

    @classmethod
    def show_audio_devices(cls):
        devices = PvRecorder.get_audio_devices()

        for i in range(len(devices)):
            print(f'index: {i}, device name: {devices[i]}')


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--access_key',
                        help='AccessKey obtained from Picovoice Console (https://picovoice.ai/console/)')

    parser.add_argument(
        '--keywords',
        nargs='+',
        help='List of default keywords for detection. Available keywords: %s' % ', '.join(sorted(pvporcupine.KEYWORDS)),
        choices=sorted(pvporcupine.KEYWORDS),
        metavar='')

    parser.add_argument(
        '--keyword_paths',
        nargs='+',
        help="Absolute paths to keyword model files. If not set it will be populated from `--keywords` argument")

    parser.add_argument('--library_path', help='Absolute path to dynamic library.', default=pvporcupine.LIBRARY_PATH)

    parser.add_argument(
        '--model_path',
        help='Absolute path to the file containing model parameters.',
        default=pvporcupine.MODEL_PATH)

    parser.add_argument(
        '--sensitivities',
        nargs='+',
        help="Sensitivities for detecting keywords. Each value should be a number within [0, 1]. A higher " +
             "sensitivity results in fewer misses at the cost of increasing the false alarm rate. If not set 0.5 " +
             "will be used.",
        type=float,
        default=None)

    parser.add_argument('--audio_device_index', help='Index of input audio device.', type=int, default=-1)

    parser.add_argument('--output_path', help='Absolute path to recorded audio for debugging.', default=None)

    parser.add_argument('--show_audio_devices', action='store_true')

    args = parser.parse_args()

    if args.show_audio_devices:
        PorcupineDemo.show_audio_devices()
    else:
        if args.access_key is None:
            args.access_key = POR_ACCESS_KEY
#            raise ValueError("AccessKey (--access_key) is required")
        if args.keyword_paths is None:
            if args.keywords is None:
                args.keywords = ['americano']
#                raise ValueError("Either `--keywords` or `--keyword_paths` must be set.")

            keyword_paths = [pvporcupine.KEYWORD_PATHS[x] for x in args.keywords]
        else:
            keyword_paths = args.keyword_paths

        if args.sensitivities is None:
            args.sensitivities = [0.5] * len(keyword_paths)

        if len(keyword_paths) != len(args.sensitivities):
            raise ValueError('Number of keywords does not match the number of sensitivities.')

        PorcupineDemo(
            access_key=args.access_key,
            library_path=args.library_path,
            model_path=args.model_path,
            keyword_paths=keyword_paths,
            sensitivities=args.sensitivities,
            output_path=args.output_path,
            input_device_index=args.audio_device_index).run()


if __name__ == '__main__':
    main()
