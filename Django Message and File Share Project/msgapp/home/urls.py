from django.urls import path
from .views import SearchView, ChatView, DownloadView, FileSendView
from django.views.generic import TemplateView
app_name = "home"

urlpatterns = [
    path('app.js',TemplateView.as_view(template_name='home/app.js')),
    path('',SearchView.as_view(), name='search'),
    path('chat',ChatView.as_view(), name='chat'),
    path('download',DownloadView.as_view(),  name="download"),
    path('file', FileSendView.as_view(), name="filesend" ),
]