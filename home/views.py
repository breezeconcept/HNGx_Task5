
from .models import RecordedVideo
from .serializers import RecordedVideoSerializer
from rest_framework import generics, status, serializers
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
import subprocess





class RecordedVideoListView(generics.ListAPIView):
    queryset = RecordedVideo.objects.all()
    serializer_class = RecordedVideoSerializer



class RecordedVideoCreateView(generics.CreateAPIView):
    serializer_class = RecordedVideoSerializer
    parser_classes = (MultiPartParser,)

    def perform_create(self, serializer):
        # Extract transcript from request data (if provided)
        transcript = self.request.data.get('transcript', '')

        # Create the video instance without compression
        instance = serializer.save()

        # Save the transcript to the video record
        instance.transcript = transcript
        instance.save()



# class RecordedVideoCreateView(generics.CreateAPIView):
#     serializer_class = RecordedVideoSerializer
#     parser_classes = (MultiPartParser,)

#     def perform_create(self, serializer):
#         # Extract transcript from request data (if provided)
#         transcript = self.request.data.get('transcript', '')

#         # Create the video instance without the transcript
#         instance = serializer.save()

#         # Perform the video compression in a separate method
#         self.compress_video(instance, transcript)

    # def compress_video(self, instance, transcript):
    #     # Specify compression parameters to maintain quality (adjust as needed)
    #     compression_params = ['-c:v', 'copy', '-c:a', 'copy']

    #     # Compress the video without losing quality
    #     input_path = instance.video_file.path
    #     compressed_path = input_path.replace('.mp4', '_compressed.mp4')

    #     # Construct the FFmpeg command for compression
    #     ffmpeg_cmd = ['ffmpeg', '-i', input_path] + compression_params + [compressed_path]

    #     # Run FFmpeg command for compression
    #     try:
    #         subprocess.run(ffmpeg_cmd, check=True)
    #     except subprocess.CalledProcessError as e:
    #         # Handle the compression error
    #         instance.delete()  # Delete the record if compression fails
    #         raise serializers.ValidationError({'message': 'Video compression failed: ' + str(e)})

    #     # Update the video file path to the compressed file
    #     instance.video_file.name = compressed_path.split('/')[-1]
    #     instance.save()

    #     # Save the transcript to the video record
    #     instance.transcript = transcript
    #     instance.save()



class RecordedVideoDetailView(generics.RetrieveAPIView):
    queryset = RecordedVideo.objects.all()
    serializer_class = RecordedVideoSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)



class RecordedVideoDeleteView(generics.DestroyAPIView):
    queryset = RecordedVideo.objects.all()
    serializer_class = RecordedVideoSerializer

    def perform_destroy(self, instance):
        instance.delete()



class RecordedVideoUpdateView(generics.UpdateAPIView):
    queryset = RecordedVideo.objects.all()
    serializer_class = RecordedVideoSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Video updated successfully.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

