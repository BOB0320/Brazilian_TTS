from personal_sessions.models import Sessions
from rest_framework import serializers
from .apps import VoiceConfig
from .models import VoiceModel, Status
from personal_sessions.models import Sessions
from backend.settings import BASE_DIR
import os
from django.core.files.base import ContentFile
import io
from scipy.io.wavfile import write
from datetime import datetime
import librosa
import json


class VoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoiceModel
        fields = '__all__'

    def create(self, validated_data):
        try:
            session_id = validated_data.get("session_id")

            if isinstance(session_id, Sessions):
                session_id = session_id.pk

            if not Sessions.objects.filter(pk=session_id).exists():
                raise serializers.ValidationError("Invalid session_id")

            session = Sessions.objects.get(pk=session_id).session_generated_text
            wav_file_name = os.path.join("media", f"{session_id}" + '.wav')

            if os.path.exists(wav_file_name):
                audio,sample_rate = librosa.load(wav_file_name, sr=None)
            else:
                # Make the API request
                audio, sample_rate = VoiceConfig.convertTextToSpeectAndCombine.combine(session,
                                                                                    os.path.join(BASE_DIR, "voice",
                                                                                                    "customMedia", "TestMusic1.wav"))

            output_file = io.BytesIO()
            write(output_file, sample_rate, audio.T)
            output_content = output_file.getvalue()
            voice_model = VoiceModel.objects.create(**validated_data)

            voice_model.voice.save(wav_file_name, ContentFile(output_content, name=wav_file_name))
            voice_model.save()

            validated_data["voice"] = voice_model.voice.path

            return voice_model
        except Exception as e:
            print("serializeer error===>",e)