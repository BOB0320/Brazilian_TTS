import re
import os
import io
from io import BytesIO
import requests
import librosa
import numpy as np
import soundfile as sf
import concurrent.futures
from openai import OpenAI
from django.apps import AppConfig
from django.conf import settings
from pydub import AudioSegment
import uuid


class CONFIG:
    # load the environment
    # Set up the client
    client = OpenAI(api_key=settings.OPENAI_API_KEY)


class ConvertTextToSpeech():
    '''
    Convert the text to speech using the openai api
    '''

    def __init__(self):
        pass

    def call_api(self, text_chunk, voice_id):
        # voice_id = settings.ELEVEN_VOICE_MODEL_ID
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        querystring = {"output_format": "mp3_22050_32"}
        headers = {
            "Accept": "audio/mp3",
            "Content-Type": "application/json",
            "xi-api-key": settings.ELEVEN_LABS_API_KEY
        }
        data = {
            "text": text_chunk,
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }

        response = requests.post(url, json=data, headers=headers, params=querystring)
        if response.status_code == 200:
            return response.content
        else:
            response.raise_for_status()

    def convert_using_elevenlabs(self, processed_chunks, voice_id):
        try:
            audio_segments_with_index = []

            # Call the API concurrently and store the audio segments along with their indices
            with concurrent.futures.ThreadPoolExecutor() as executor:
                # Submit tasks to the executor, storing the index and the task's future
                futures_and_indices = [(executor.submit(self.call_api, chunk, voice_id), i) for i, chunk in
                                       enumerate(processed_chunks)]

                # Retrieve results as they complete
                for future, index in futures_and_indices:
                    try:
                        # Get the audio content from the API response
                        audio_content = future.result()
                        # Store the audio content with the index to maintain order
                        audio_segments_with_index.append((index, audio_content))
                    except Exception as exc:
                        print(f"An error occurred on chunk {index}: {exc}")

            # Sort the audio segments by index to ensure they are in the correct order
            audio_segments_with_index.sort(key=lambda x: x[0])

            # Initialize an empty AudioSegment object
            combined_audio = AudioSegment.empty()

            # Concatenate the audio chunks in the correct order
            for index, audio_content in audio_segments_with_index:
                # Wrap the binary audio content in a BytesIO object
                audio_buffer = BytesIO(audio_content)
                # Parse the BytesIO object using AudioSegment
                audio_segment = AudioSegment.from_file(audio_buffer, format="mp3")
                # Concatenate audio segments
                combined_audio += audio_segment
            # After combining all chunks, export the result to a single MP3 file
            output_file = "output" + str(uuid.uuid4()) + ".mp3"
            combined_audio.export(output_file, format="mp3")

            return output_file
        except Exception as e:
            print("convert error:", e)

    def convert(self, text):
        response = CONFIG.client.audio.speech.create(
            model="tts-1-hd",
            voice="onyx",
            input=text
        )

        audio_bytes = response.response.iter_bytes()
        audio_io = io.BytesIO(b''.join(audio_bytes))

        speech, sample_rate = librosa.load(audio_io, sr=None)

        return speech, sample_rate


class ConvertTextToSpeechAndCombine():

    def __init__(self, speech_weightage, music_weightage):
        self.convertTextToSpeech = ConvertTextToSpeech()
        self.speech_weightage = speech_weightage
        self.music_weightage = music_weightage

    def combine(self, chunks, voice_id):
        try:
            output_file = self.convertTextToSpeech.convert_using_elevenlabs(chunks, voice_id)
            return output_file
        except Exception as e:
            print("combine error:", e)


class VoiceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'voice'
    convertTextToSpeectAndCombine = ConvertTextToSpeechAndCombine(speech_weightage=0.8, music_weightage=0.12)
