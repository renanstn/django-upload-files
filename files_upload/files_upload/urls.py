from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from core import views


router = routers.DefaultRouter()

router.register(r"files", views.FileViewSet)
router.register(r"students", views.StudentViewSet, basename="students")

urlpatterns = [
    path("", include(router.urls)),
    path("admin/", admin.site.urls),
    path("api-auth", include("rest_framework.urls")),
]
