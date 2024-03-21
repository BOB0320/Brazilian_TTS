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
    path('my-api/', views.VoiceView.as_view(), name='my-api'),
]