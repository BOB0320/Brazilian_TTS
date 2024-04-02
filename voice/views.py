from django.http import JsonResponse, FileResponse
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from .serializer import VoiceSerializer, MyAPISerializer
from wsgiref.util import FileWrapper
from django.http import StreamingHttpResponse

text_parameter = openapi.Parameter('text', openapi.IN_QUERY, description="text that need to be converted",
                                   type=openapi.TYPE_STRING, required=True)

class AbstractVoiceView(APIView):
    serializer_class = MyAPISerializer
    voice_id = None

    def get_voice_id(self):
        raise NotImplementedError

    @swagger_auto_schema(manual_parameters=[text_parameter])
    def get(self, request, *args, **kwargs):
        text = request.query_params.get('text')
        if text is None:
            return Response({"detail": "Query param text is missing"}, status=status.HTTP_400_BAD_REQUEST)

        voice_serializer = VoiceSerializer()
        try:
            output_path = voice_serializer.create(text=text, voice_id=self.get_voice_id())
            file = FileWrapper(open(output_path, 'rb'))
            response = StreamingHttpResponse(file, content_type='audio/wav')
            response['Content-Disposition'] = 'attachment; filename="my_file.mp3"'
            return response
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class VoiceViewElevenMale(AbstractVoiceView):
    def get_voice_id(self):
        return "2EiwWnXFnvU5JabPnv8n"

class VoiceViewElevenFemale(AbstractVoiceView):
    def get_voice_id(self):
        return "YIyfViqVCyf9GWwr0Vg6"

class VoiceViewTraconMale(AbstractVoiceView):
    def get_voice_id(self):
        return "SjOBH516c8B9Mkftrdvn"

class VoiceViewTraconFemale(AbstractVoiceView):
    def get_voice_id(self):
        return "CZD4BJ803C6T0alQxsR7"