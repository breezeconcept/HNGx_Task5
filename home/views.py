# videorecording/views.py
import uuid
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import RecordedVideo
from .serializers import RecordedVideoSerializer
from .utils import process_and_save_recording, retrieve_recorded_data, extract_and_save_audio

# Function to generate a unique session ID
def generate_session_id():
    return str(uuid.uuid4())

@api_view(['POST'])
@parser_classes([JSONParser])
def start_recording(request):
    # Generate a unique session ID
    session_id = generate_session_id()
    
    # Create a new recording session
    recording = RecordedVideo(session_id=session_id)
    recording.save()
    
    return Response({'session_id': session_id}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@parser_classes([JSONParser])
def receive_video_chunk(request):
    session_id = request.data.get('session_id')
    video_chunk = request.data.get('video_chunk')
    
    try:
        recording = RecordedVideo.objects.get(session_id=session_id)
        recording.video_data += video_chunk
        recording.save()
        return Response({'message': 'Video chunk received successfully.'}, status=status.HTTP_200_OK)
    except RecordedVideo.DoesNotExist:
        return Response({'message': 'Recording session not found.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@parser_classes([JSONParser])
def finalize_recording(request):
    session_id = request.data.get('session_id')
    video_chunk = request.data.get('video_chunk')
    is_final = request.data.get('is_final', False)
    
    try:
        recording = RecordedVideo.objects.get(session_id=session_id)
        recording.video_data += video_chunk
        if is_final:
            # Save the video data
            recording.save()
            
            # Extract and save audio
            video_path = recording.video_file.path
            audio_path = 'path_to_save_extracted_audio.mp3'  # Specify your desired audio path
            extract_and_save_audio(video_path, audio_path)
            
            # Process and save the recording (if needed)
            process_and_save_recording(recording)  # Implement this function
        else:
            recording.save()
        return Response({'message': 'Video chunk received successfully.'}, status=status.HTTP_200_OK)
    except RecordedVideo.DoesNotExist:
        return Response({'message': 'Recording session not found.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_recorded_data(request, session_id):
    try:
        recording = RecordedVideo.objects.get(session_id=session_id)
        
        # Use the serializer to retrieve recorded data
        serializer = RecordedVideoSerializer(recording)
        
        return Response({'recorded_data': serializer.data}, status=status.HTTP_200_OK)
    except RecordedVideo.DoesNotExist:
        return Response({'message': 'Recording session not found.'}, status=status.HTTP_404_NOT_FOUND)
