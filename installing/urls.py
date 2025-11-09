from django.urls import path
from .views import ServerCreateView, get_available_versions, get_download_info

urlpatterns = [
    path('create/', view=ServerCreateView.as_view(), name="create_server"),
    path('api/get-versions/', view=get_available_versions, name="get_available_view"),
    path('api/get-download-info/', view=get_download_info, name="get_download_info")
]