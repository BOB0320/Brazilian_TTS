from django.urls import path
from . import views

urlpatterns = [
    path('', views.VoiceView.voice_view, name='voice_view'),
    path('<int:pk>/', views.VoiceView.as_view(), name='home')
]