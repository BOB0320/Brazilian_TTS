from rest_framework import serializers
from pydub import AudioSegment
from .apps import VoiceConfig
import os
from backend.settings import BASE_DIR
from django.core.files.base import ContentFile
import io
from scipy.io.wavfile import write
from datetime import datetime
import librosa
import uuid
from .textsplitter import TextSplitter
import numpy as np
import soundfile as sf


class MyAPISerializer(serializers.Serializer):
    text = serializers.CharField(help_text='Your text goes here')


class VoiceSerializer(serializers.Serializer):

    def create(self, text, voice_id):
        try:
            text_splitter = TextSplitter()
            processed_chunks = text_splitter.process(text)
            for idx, section in enumerate(processed_chunks):
                print(f"Section {idx + 1}:")
                print(section)
                print("------")

            output_file = VoiceConfig.convertTextToSpeectAndCombine.combine(processed_chunks, voice_id)
            output_file_full_path = os.path.join(BASE_DIR, output_file)
            print("output_filepath", output_file_full_path)
            return output_file_full_path
        except Exception as e:
            print("serializeer error===>", e)
