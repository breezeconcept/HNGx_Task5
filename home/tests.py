from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

class VideoUploadTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_upload_video_with_transcript(self):
        # Assuming you have a valid video file and transcript
        video_data = {
            'title': 'Test Video',
            'video_file': open('path/to/video.mp4', 'rb'),
            'transcript': 'This is a test transcript.'
        }
        response = self.client.post('/api/upload/', video_data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('message' in response.data)

        # Add more assertions as needed to check the response content
