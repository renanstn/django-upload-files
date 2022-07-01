import csv
from io import StringIO

from rest_framework import serializers

from core import models


class FileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.File
        fields = "__all__"


class StudentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Student
        fields = "__all__"


class ProcessUploadedFileSerializer(serializers.Serializer):
    """
    Process a CSV file, extract the needed fields, and store it
    """

    file = serializers.FileField()

    def create(self, validated_data):
        file_content = validated_data["file"].read().decode("utf-8")
        reader = csv.DictReader(StringIO(file_content), skipinitialspace=True)
        content_to_save = []
        for row in reader:
            content_to_save.append(
                models.Student(
                    name=f"{row['First name']} {row['Last name']}",
                    ssn=row["SSN"],
                )
            )
        objects = models.Student.objects.bulk_create(content_to_save)
        return objects
