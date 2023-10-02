# videorecording/utils.py
from django.core.files.base import ContentFile
from django.conf import settings
import os

# videorecording/utils.py
from moviepy.editor import VideoFileClip


def process_and_save_recording(recording):
    # Save the video chunk data directly
    recording.video_file.save(f"{recording.session_id}.mp4", ContentFile(recording.video_data))

# Note: You may need to adjust the file name and storage location as needed.





def retrieve_recorded_data(recording):
    # Define the path to the recorded data file
    data_file_path = os.path.join(settings.MEDIA_ROOT, f"{recording.session_id}.mp4")

    try:
        with open(data_file_path, 'rb') as data_file:
            return data_file.read()
    except FileNotFoundError:
        return None  # Handle the case where the file is not found




def extract_and_save_audio(video_path, audio_path):
    try:
        video = VideoFileClip(video_path)
        audio = video.audio
        audio.write_audiofile(audio_path)
        video.close()
        audio.close()
    except Exception as e:
        # Handle any exceptions that may occur during audio extraction
        print(f"Audio extraction failed: {str(e)}")
