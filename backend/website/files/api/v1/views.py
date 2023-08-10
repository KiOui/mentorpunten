from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from files import models, services
from files.api.v1 import serializers
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from files.models import File
from mentorpunten.api.openapi import CustomAutoSchema


class TemporaryFileUploadListCreateAPIView(ListCreateAPIView):
    """Temporary File Upload List Create API View."""

    serializer_class = serializers.TemporaryFileUploadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Get Queryset."""
        return models.TemporaryFileUpload.objects.filter(created_by=self.request.user)

    def create(self, request, *args, **kwargs):
        """Create a Temporary File Upload."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        temporary_file = services.create_temporary_file_upload_data(
            request.user,
            serializer.validated_data.get("original_file_name"),
            serializer.validated_data.get("file_type"),
        )
        output_serializer = self.get_serializer(temporary_file, many=False)
        headers = self.get_success_headers(output_serializer.data)
        return Response(
            output_serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class TemporaryFileUploadRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """Temporary File Upload Retrieve Update Destroy API View."""

    serializer_class = serializers.TemporaryFileUploadSerializer
    permission_classes = [IsAuthenticated]

    schema = CustomAutoSchema(
        request_schema={
            "type": "object",
            "properties": {
                "finished_at": {"type": "string", "format": "date-time"},
            },
        }
    )

    def get_queryset(self):
        """Get Queryset."""
        return models.TemporaryFileUpload.objects.filter(created_by=self.request.user)

    def update(self, request, *args, **kwargs):
        """Update method."""
        finished_at = request.data.get("finished_at")
        instance = self.get_object()
        if instance.finished_at is not None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        instance.finished_at = finished_at
        instance.save()
        output_serializer = self.get_serializer(instance, many=False)
        return Response(output_serializer.data, status=status.HTTP_200_OK)


class FileListCreateAPIView(ListCreateAPIView):
    """File List Create API View."""

    serializer_class = serializers.FileSerializer
    permission_classes = [IsAuthenticated]

    schema = CustomAutoSchema(
        request_schema={
            "type": "object",
            "properties": {
                "temporary_file_upload": {"type": "string"},
            },
        }
    )

    def get_queryset(self):
        """Get Queryset."""
        return models.File.objects.filter(created_by=self.request.user)

    def create(self, request, *args, **kwargs):
        """Create a Temporary File Upload."""
        temporary_file_upload_id = request.data.get("temporary_file_upload", None)
        if temporary_file_upload_id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            temporary_file_upload = models.TemporaryFileUpload.objects.get(
                id=temporary_file_upload_id, created_by=request.user
            )
        except models.TemporaryFileUpload.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if not temporary_file_upload.finished:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if File.objects.filter(temporary_file_upload=temporary_file_upload).count() > 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        file = services.create_file_from_temporary_file_upload(temporary_file_upload)

        output_serializer = self.get_serializer(file, many=False)
        headers = self.get_success_headers(output_serializer.data)
        return Response(
            output_serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
