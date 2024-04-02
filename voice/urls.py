from django.urls import path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from . import views

schema_view = get_schema_view(
    openapi.Info(
        title="My API",
        default_version='v1',
        description="Test description",
    ),
    public=True,
)
urlpatterns = [
    path('elevenlabs/male/', views.VoiceViewElevenMale.as_view(), name='my-api-eleven-male'),
    path('elevenlabs/female/', views.VoiceViewElevenFemale.as_view(), name='my-api-eleven-female'),
    path('tracon/male/', views.VoiceViewTraconMale.as_view(), name='my-api-tracon-male'),
    path('tracon/female/', views.VoiceViewTraconFemale.as_view(), name='my-api-tracon-female'),
]