from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.video_upload_view, name='video_upload'),
    path('list/', views.video_list_view, name='video_list'),
    path('<int:video_id>/', views.video_detail_view, name='video_detail'),
    path('search/', views.search_subtitle, name='search_subtitle'),
]