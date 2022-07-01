from django.http import FileResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from core import models, serializers


class SimpleUploadFileViewSet(viewsets.ModelViewSet):
    """
    This first example, is a simple view used to upload and serve files
    """

    queryset = models.File.objects.all()
    serializer_class = serializers.FileSerializer

    @action(methods=["get"], detail=True)
    def download_file(self, request, pk=None):
        instance = self.get_object()
        file_handle = instance.file.open()
        response = FileResponse(file_handle, content_type="text/csv")
        return response


class ProcessUploadedFileViewSet(viewsets.ViewSet):
    """
    In this second example, we receive a file, proccess it, and save only a few
    values on Student model.
    The expected CSV must be in a form field called "file", and must contain
    this columns:
    - First name
    - Last name
    - SSN
    """

    def create(self, request):
        file = request.FILES.get("file", False)
        if not file:
            return Response("Where is the file?", status.HTTP_400_BAD_REQUEST)

        serializer = serializers.ProcessUploadedFileSerializer(
            data={"file": file}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response("file processed with success", status.HTTP_201_CREATED)
