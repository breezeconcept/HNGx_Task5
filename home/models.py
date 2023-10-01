# models.py
from django.db import models

class RecordedVideo(models.Model):
    title = models.CharField(max_length=255)
    video_file = models.FileField(upload_to='videos/')
    transcription = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title
