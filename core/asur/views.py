from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

from .models import UploadedFile
from .serializers import FileUploadSerializer
from drf_yasg.utils import swagger_auto_schema

class FileUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        request_body=FileUploadSerializer,
        responses={201: 'Файл успешно загружен'},
        operation_description="Загружайте только файлы JSON"
    )
    def post(self, request, *args, **kwargs):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"message": "Файл успешно загружен"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request, *args, **kwargs):
        files = UploadedFile.objects.all()
        serializer = FileUploadSerializer(files, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
