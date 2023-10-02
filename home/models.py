# ./models.py
from django.db import models

class RecordedVideo(models.Model):
    session_id = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=20, default="recording")
    # transcription = models.TextField(blank=True, null=True)
    audio_file = models.FileField(upload_to='audio/', blank=True, null=True)
    file_url = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.session_id




