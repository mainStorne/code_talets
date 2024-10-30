from django.urls import path
from .views import StreamView


urlpatterns = [
	path('stream/', StreamView.as_view(), name='stream')
]
