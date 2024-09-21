from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Video, Subtitle
from .forms import VideoUploadForm
import subprocess
import os

def home(request):
    return render(request, 'base.html')

def video_upload_view(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save()

            # Extract subtitles using ffmpeg
            video_path = video.video_file.path
            subtitle_path = os.path.join(os.path.dirname(video_path), f"{video.id}_subtitles.srt")
            command = f"ffmpeg -i {video_path} -map 0:s:0 {subtitle_path}"
            subprocess.run(command, shell=True, check=True)

            # Save the extracted subtitles
            with open(subtitle_path, 'r') as f:
                subtitles = f.read()
                Subtitle.objects.create(video=video, language='English', subtitle_file=subtitles)

            return JsonResponse({'message': 'Video uploaded successfully'})
    else:
        form = VideoUploadForm()
    return render(request, 'upload.html', {'form': form})


def video_list_view(request):
    videos = Video.objects.all()
    return render(request, 'list.html', {'videos': videos})


def video_detail_view(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    subtitles = video.subtitles.all()
    return render(request, 'detail.html', {'video': video, 'subtitles': subtitles})


def search_subtitle(request):
    query = request.GET.get('q')
    subtitles = Subtitle.objects.filter(subtitle_file__icontains=query)
    results = [{'video': subtitle.video.title, 'language': subtitle.language} for subtitle in subtitles]
    return JsonResponse({'results': results})