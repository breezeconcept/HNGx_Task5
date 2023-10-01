# urls.py
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import RecordedVideoListView, RecordedVideoCreateView, RecordedVideoDetailView, RecordedVideoDeleteView, RecordedVideoUpdateView


urlpatterns = [
    path('api/videos/', RecordedVideoListView.as_view(), name='recordedvideo-list'),
    path('api/videos/upload/', RecordedVideoCreateView.as_view(), name='recordedvideo-create'),
    path('api/videos/<int:pk>/', RecordedVideoDetailView.as_view(), name='recordedvideo-detail'),
    path('api/videos/delete/<int:pk>/', RecordedVideoDeleteView.as_view(), name='recordedvideo-delete'),
    path('api/videos/edit/<int:pk>/', RecordedVideoUpdateView.as_view(), name='recordedvideo-update'),
]



# urlpatterns = [
#     # Video Upload, Compression, and Transcription
#     path('api/video/upload/', views.upload_compress_transcribe_video, name='upload_compress_transcribe_video'),

#     # Get All Videos
#     path('api/videos/', views.get_all_videos, name='get_all_videos'),

#     # Get Video by ID
#     path('api/video/<int:video_id>/', views.get_video_by_id, name='get_video_by_id'),

#     # Delete Video by ID
#     path('api/video/delete/<int:video_id>/', views.delete_video_by_id, name='delete_video_by_id'),

#     # Update Video by ID
#     path('api/video/edit/<int:video_id>/', views.update_video_by_id, name='update_video_by_id'),
# ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)