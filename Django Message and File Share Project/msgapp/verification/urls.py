from django.urls import path
from .views import Startup, Verify, NameView
app_name = 'verification'
urlpatterns = [
    path('', Startup.as_view(), name='start'),
    path('verify', Verify.as_view(), name = 'verify'),
    path('name',NameView.as_view(), name='name'),
]