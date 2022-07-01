import uuid
from django.db import models


class File(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    upload_datetime = models.DateTimeField(auto_now_add=True)
    comments = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to="uploaded_files/")

    def __str__(self) -> str:
        return self.name


class Student(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    ssn = models.CharField(max_length=11)

    def __str__(self) -> str:
        return self.name
