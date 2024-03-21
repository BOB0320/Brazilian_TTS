from django.http import JsonResponse
import asyncio

from rest_framework.decorators import api_view
from asgiref.sync import sync_to_async
from .serializer import VoiceSerializer
from rest_framework.views import APIView
from rest_framework import renderers
from .models import VoiceModel
import base64
import os
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


class VoiceView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request,pk):
        try:

        # Get all the results from the request
            user = request.user
            serializer = VoiceSerializer(data = {"session_id":pk,'user_id': user.pk})
            if serializer.is_valid():
                serializer.save()
                serializer_data = serializer.data
                file_path = os.path.join(os.getcwd(),str(serializer_data["voice"])[1:])
                file = open(file_path, "rb")
                return HttpResponse(file, content_type='audio/wav', status=status.HTTP_200_OK)
            else:
                return HttpResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return HttpResponse(f"An error occurred: {str(e)}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def voice_view(request):
        return JsonResponse({'status': 'Voice Endpoint'})