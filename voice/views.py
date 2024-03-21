# from django.http import JsonResponse
# import asyncio
# from drf_yasg.utils import swagger_auto_schema
# from rest_framework.decorators import api_view
# from asgiref.sync import sync_to_async
# from .serializer import VoiceSerializer, MyAPISerializer
# from rest_framework.views import APIView
# from rest_framework import renderers
# from django.http import HttpResponse
# from rest_framework.permissions import IsAuthenticated
# from rest_framework import status
# from rest_framework import serializers
# from rest_framework.response import Response

# from django.http import FileResponse
# from django.http import FileResponse

# class VoiceView(APIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = MyAPISerializer 

#     @swagger_auto_schema(request_body=MyAPISerializer)
#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             text = serializer.validated_data.get('text')
#             voice_serializer = VoiceSerializer()
#             try:
#                 output_full_path = voice_serializer.create(text=text)
#                 # Here I'm assuming create method is returning absolute path
#                 file = open(output_full_path, "rb")
#                 print(file)
#                 # Create a django FileResponse
#                 response = FileResponse(file, content_type='audio/wav')

#             except Exception as e:
#                 # It's better to return JsonResponse instead of print
#                 return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
#             return response

#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from django.http import JsonResponse
import asyncio
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from asgiref.sync import sync_to_async
from .serializer import VoiceSerializer, MyAPISerializer
from rest_framework.views import APIView
from rest_framework import renderers
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework import serializers
from rest_framework.response import Response

from django.http import FileResponse
from drf_yasg import openapi


class VoiceView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MyAPISerializer 

    @swagger_auto_schema(manual_parameters=[openapi.Parameter('text', openapi.IN_QUERY, description="text that need to be converted", type=openapi.TYPE_STRING, required=True)])
    def get(self, request, *args, **kwargs):
        text = request.query_params.get('text')
        if text:
            voice_serializer = VoiceSerializer()
            try:
                output_full_path = voice_serializer.create(text=text)
                file = open(output_full_path, "rb")

                # Create a django FileResponse
                response = FileResponse(file, content_type='audio/wav')

            except Exception as e:
                # It's better to return JsonResponse instead of print
                return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
            return response

        else:
            return Response({"detail": "Query param text is missing"}, status=status.HTTP_400_BAD_REQUEST)