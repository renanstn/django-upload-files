from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from core import views


router = routers.DefaultRouter()
router.register(r"simple-upload-files", views.SimpleUploadFileViewSet)
router.register(
    r"process-file-upload",
    views.ProcessUploadedFileViewSet,
    basename="process_file_upload",
)

urlpatterns = [
    path("", include(router.urls)),
    path("admin/", admin.site.urls),
    path("api-auth", include("rest_framework.urls")),
]
