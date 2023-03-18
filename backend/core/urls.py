from django.urls import path
from .views import Home,upload_display_video
urlpatterns = [
    path("",Home),
    path("home/",upload_display_video)
]
