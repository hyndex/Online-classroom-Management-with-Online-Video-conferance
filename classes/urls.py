from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'notes', NotesViewSet)
router.register(r'assignment', AssignmentViewSet)
router.register(r'submit', AssignmentSubmitViewSet)
router.register(r'room', OnlineClassRoomViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    path('notes_upload/<int:pk>/', NotesUploadView.as_view()),
    path('assignment_upload/<int:pk>/', AssignmentUploadView.as_view()),
    path('submit_upload/<int:pk>/', AssignmentSubmitUploadView.as_view()),
]
if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)