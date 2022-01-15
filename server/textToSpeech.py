# coding=utf-8
import json
from os.path import join, dirname
from ibm_watson import TextToSpeechV1
from ibm_watson.websocket import SynthesizeCallback
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

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

done = False
class MySynthesizeCallback(SynthesizeCallback):
    def __init__(self, file_path):       
        global done 
        SynthesizeCallback.__init__(self)
        done = False
        self.fd = open(file_path, 'ab')

    def on_connected(self):
        print('Connection was successful')

    def on_error(self, error):
        print('Error received: {}'.format(error))

    def on_content_type(self, content_type):
        print('Content type: {}'.format(content_type))

    def on_timing_information(self, timing_information):
        print(timing_information)

    def on_audio_stream(self, audio_stream):
        self.fd.write(audio_stream)

    def on_close(self):
        global done
        self.fd.close()
        done = True
        print('Done synthesizing. Closing the connection')

class audioPlayer:
    def __init__(self):
        authenticator = IAMAuthenticator(TEXT_TO_SPEECH_APIKEY)
        self.service = TextToSpeechV1(authenticator=authenticator)
        self.service.set_service_url(TEXT_TO_SPEECH_URL)

        #voices = self.service.list_voices().get_result()
        #print(json.dumps(voices, indent=2))

    def playAudio(self, text, file_path):
        my_callback = MySynthesizeCallback(file_path)
        self.service.synthesize_using_websocket(text,
                                    my_callback,
                                    accept='audio/wav',
                                    voice='en-US_AllisonVoice'
                                    )
    def isDone(self):
        global done
        return done

    # voice_model = service.create_custom_model('test-customization').get_result()
    # print(json.dumps(custom_model, indent=2))

    # updated_custom_model = service.update_custom_model(
    #     'YOUR CUSTOMIZATION ID', name='new name').get_result()
    # print(updated_custom_model)

    # custom_model = service.get_custom_model('YOUR CUSTOMIZATION ID').get_result()
    # print(json.dumps(custom_model, indent=2))

    # words = service.list_words('YOUR CUSTOMIZATIONID').get_result()
    # print(json.dumps(words, indent=2))

    # words = service.add_words('YOUR CUSTOMIZATION ID', [{
    #     'word': 'resume',
    #     'translation': 'rɛzʊmeɪ'
    # }]).get_result()
    # print(words)

    # word = service.add_word(
    #     'YOUR CUSTOMIZATION ID', word='resume', translation='rɛzʊmeɪ').get_result()
    # print(word)

    # word = service.get_word('YOUR CUSTOMIZATIONID', 'resume').get_result()
    # print(json.dumps(word, indent=2))

    # response = service.delete_word('YOUR CUSTOMIZATION ID', 'resume').get_result()
    # print(response)

    # response = service.delete_voice_model('YOUR CUSTOMIZATION ID').get_result()
    # print(response)

    # Synthesize using websocket. Note: The service accepts one request per connection
        
    
if __name__ == '__main__':
    player = audioPlayer()
    player.playAudio('I like to pet dogs',file_path = '/home/pi/my_output.wav') 

