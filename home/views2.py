# For the second view
# views.py
from rest_framework import status
from rest_framework.response import Response
# from rest_framework.decorators import api_view
from .models import RecordedVideo
from .serializers import RecordedVideoSerializer

import subprocess
from rest_framework.parsers import MultiPartParser
from rest_framework.decorators import api_view, parser_classes


# from google.cloud import speech_v1p1beta1 as speech     
# from google.cloud import speech
# from google.cloud.speech import enums
# from google.cloud.speech import types







@api_view(['GET'])
def get_all_videos(request):
    videos = RecordedVideo.objects.all()
    serializer = RecordedVideoSerializer(videos, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)






@api_view(['POST'])
@parser_classes([MultiPartParser])
def upload_compress_transcribe_video(request):
    if request.method == 'POST':
        serializer = RecordedVideoSerializer(data=request.data)
        if serializer.is_valid():
            title = serializer.validated_data.get('title')
            video_file = serializer.validated_data.get('video_file')
            transcript = request.data.get('transcript')  # Get the transcript from the request

            # Save the uploaded video
            video = RecordedVideo(title=title, video_file=video_file)
            video.save()

            # Save the transcript to the video record
            video.transcription = transcript
            video.save()

            # Specify compression parameters to maintain quality (adjust as needed)
            compression_params = ['-c:v', 'copy', '-c:a', 'copy']

            # Compress the video without losing quality
            input_path = video.video_file.path
            compressed_path = input_path.replace('.mp4', '_compressed.mp4')

            # Construct the FFmpeg command for compression
            ffmpeg_cmd = ['ffmpeg', '-i', input_path] + compression_params + [compressed_path]

            # Run FFmpeg command for compression
            try:
                subprocess.run(ffmpeg_cmd, check=True)
            except subprocess.CalledProcessError as e:
                # Handle the compression error
                video.delete()  # Delete the record if compression fails
                return Response({'message': 'Video compression failed: ' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Update the video file path to the compressed file
            video.video_file.name = compressed_path.split('/')[-1]
            video.save()

            return Response({'message': 'Video uploaded, compressed, and transcript saved successfully.'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response({'message': 'Method not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)




# @api_view(['POST'])
# @parser_classes([MultiPartParser])
# def upload_compress_transcribe_video(request):
#     if request.method == 'POST':
#         serializer = RecordedVideoSerializer(data=request.data)
#         if serializer.is_valid():
#             title = serializer.validated_data.get('title')
#             video_file = serializer.validated_data.get('video_file')

#             # Save the uploaded video
#             video = RecordedVideo(title=title, video_file=video_file)
#             video.save()

#             # Specify compression parameters to maintain quality (adjust as needed)
#             compression_params = ['-c:v', 'libx264', '-crf', '18', '-preset', 'fast']

#             # Compress the video
#             input_path = video.video_file.path
#             compressed_path = input_path.replace('.mp4', '_compressed.mp4')

#             # Construct the FFmpeg command for compression
#             ffmpeg_cmd = ['ffmpeg', '-i', input_path] + compression_params + [compressed_path]

#             # Run FFmpeg command for compression
#             try:
#                 subprocess.run(ffmpeg_cmd, check=True)
#             except subprocess.CalledProcessError as e:
#                 # Handle the compression error
#                 video.delete()  # Delete the record if compression fails
#                 return Response({'message': 'Video compression failed: ' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#             # Update the video file path to the compressed file
#             video.video_file.name = compressed_path.split('/')[-1]
#             video.save()

#             # Transcribe the video
#             video_path = video.video_file.path
#             client = speech.SpeechClient()

#             with open(video_path, 'rb') as video_file:
#                 content = video_file.read()

#             audio = types.RecognitionAudio(content=content)
#             config = types.RecognitionConfig(
#                 encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
#                 sample_rate_hertz=16000,  # Adjust to match your video's audio settings
#                 language_code='en-US',  # Adjust for the language of your videos
#             )

#             response = client.recognize(config=config, audio=audio)
#             transcript = ""

#             for result in response.results:
#                 transcript += result.alternatives[0].transcript + " "

#             # Update the video record with the transcript
#             video.transcription = transcript
#             video.save()

#             return Response({'message': 'Video uploaded, compressed, and transcribed successfully.'}, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     return Response({'message': 'Method not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)







@api_view(['GET'])
def get_video_by_id(request, video_id):
    try:
        video = RecordedVideo.objects.get(id=video_id)
    except RecordedVideo.DoesNotExist:
        return Response({'message': 'Video not found.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = RecordedVideoSerializer(video)
    return Response(serializer.data, status=status.HTTP_200_OK)








@api_view(['GET','DELETE'])
def delete_video_by_id(request, video_id):
    try:
        video = RecordedVideo.objects.get(id=video_id)
    except RecordedVideo.DoesNotExist:
        return Response({'message': 'Video not found.'}, status=status.HTTP_404_NOT_FOUND)

    video.delete()
    return Response({'message': 'Video deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)












@api_view(['GET','PUT'])
def update_video_by_id(request, video_id):
    try:
        video = RecordedVideo.objects.get(id=video_id)
    except RecordedVideo.DoesNotExist:
        return Response({'message': 'Video not found.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = RecordedVideoSerializer(video, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Video updated successfully.'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
