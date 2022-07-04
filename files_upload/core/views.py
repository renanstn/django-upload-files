import uuid
import datetime

from django.http import FileResponse
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from core import models, serializers


class FileViewSet(viewsets.ModelViewSet):
    """
    This first example, is a simple view used to upload, list and serve files
    """

    queryset = models.File.objects.all()
    serializer_class = serializers.FileSerializer

    @action(methods=["get"], detail=True)
    def download_file(self, request, pk=None):
        instance = self.get_object()
        file_handle = instance.file.open()
        response = FileResponse(file_handle, content_type="text/csv")
        return response


class StudentViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """
    In this second example, we can populate a Student model by sent a CSV file
    """

    queryset = models.Student.objects.all()
    serializer_class = serializers.StudentSerializer

    @action(detail=False, methods=["post"])
    def create_students_from_csv(self, request):
        """
        The expected CSV must be in a form field called "file", and must
        contain this columns:
        - First name
        - Last name
        - SSN
        """
        file = request.FILES.get("file", False)
        if not file:
            return Response("Where is the file?", status.HTTP_400_BAD_REQUEST)

        # Use file data to populate Student model
        student_serializer = serializers.ProcessUploadedFileSerializer(
            data={"file": file}
        )
        student_serializer.is_valid(raise_exception=True)
        student_serializer.save()

        # Save file too
        file_name, file_extension = file.name.split(".")
        full_file_name = f"{file_name}{uuid.uuid4().hex[:8]}.{file_extension}"
        file_serializer = serializers.FileSerializer(
            data={
                "name": full_file_name,
                "upload_datetime": datetime.datetime.now(),
                "comments": "file saved automatically",
                "file": file,
            }
        )
        file_serializer.is_valid(raise_exception=True)
        file_serializer.save()

        return Response("file processed with success", status.HTTP_201_CREATED)
