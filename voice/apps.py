from django.apps import AppConfig
import re
import os
from openai import OpenAI
from django.conf import settings
import librosa
import io
import numpy as np


class CONFIG:
    # load the environment
    # Set up the client
    client = OpenAI(api_key=settings.OPENAI_API_KEY)


class PreprocessText():
    def __init__(self,nums_stops_inside_paragraph = 3,nums_stops_end_paragraph = 4):
        self.nums_stops_inside_paragraph = nums_stops_inside_paragraph
        self.nums_stops_end_paragraph = nums_stops_end_paragraph

    def process(self,text):
        processes = [self._handleCommas,self._handleFullStops]
        for process in processes:
            text = process(text)
        return text

    def _handleFullStops(self,text):

        # handle the full stops inside the paragraph
        pattern = r"([^.])(\.)([^\n\.])"
        replacement = " [pause]." * self.nums_stops_inside_paragraph
        text = re.sub(pattern,r'\1' + replacement + r'\3', text)


        # handle the full stops at the end of the paragraph
        pattern = r"([^.])(\.)([\n])"
        replacement = " [pause]." * self.nums_stops_end_paragraph
        text = re.sub(pattern,r'\1' + replacement + r'\3', text)

        return text

    def _handleCommas(self,text):
        return text

class ConvertTextToSpeech():
    '''
    Convert the text to speech using the openai api
    '''
    def __init__(self):
        pass

    def convert(self,text):
        # Make the api call to get the response
        speech_file_path = os.path.join(os.path.abspath('') ,"speech.mp3")
        response = CONFIG.client.audio.speech.create(
                    model="tts-1-hd",
                    voice="onyx",
                    input= text
                )

        audio_bytes = response.response.iter_bytes()
        audio_io = io.BytesIO(b''.join(audio_bytes))

        speech, sample_rate = librosa.load(audio_io, sr=None)

        return speech,sample_rate

class ConvertTextToSpeechAndCombine():

    def __init__(self, speech_weightage, music_weightage):
        self.convertTextToSpeech  = ConvertTextToSpeech()
        self.speech_weightage = speech_weightage
        self.music_weightage = music_weightage


    def combine(self,text,music_file_path = None):
        # Convert from text to speech
        speech, speech_sampe_rate = self.convertTextToSpeech.convert(text)

        if music_file_path is None:
            return speech, speech_sampe_rate

        # load the music file
        music, music_sample_rate = librosa.load(music_file_path, sr=None)

        # Check if sampling rates match, if not, resample one of the files
        if speech_sampe_rate != music_sample_rate:
            music = librosa.resample(music,  orig_sr=music_sample_rate, target_sr=speech_sampe_rate)
            music_sample_rate = speech_sampe_rate

        number_of_loops = (len(speech) // len(music)) + 1
        music = np.array(list(music) * number_of_loops)

        # # Take th minimum of the length
        min_len = min(len(speech), len(music))
        speech = speech[:min_len]
        music = music[:min_len]

        # Combine the audio arrays
        y_combined = self.speech_weightage * speech + self.music_weightage * music


        return y_combined, speech_sampe_rate

    # def convertIntoAudioFile(self,combined_audio,sample_rate,file_name):
    #     # Save
    #     sf.write(file_name,combined_audio.T,sample_rate)



class VoiceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'voice'
    convertTextToSpeectAndCombine = ConvertTextToSpeechAndCombine(speech_weightage=0.8,music_weightage=0.12)
