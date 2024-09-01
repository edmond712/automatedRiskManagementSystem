from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from .models import UploadedFile
from .serializers import FileUploadSerializer
from drf_yasg.utils import swagger_auto_schema

from django.shortcuts import render
from .utils.utils import FileUploadForm
from .utils.risk_calculator import calculate_impact, Risk, Requirement
import json
import pandas as pd


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


def upload_file_view(request, session_number=None):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            json_file = form.cleaned_data['project_file']
            project_data = json.load(json_file)

            excel_file = request.FILES['mitigation_matrix']
            mitigation_matrix = pd.read_excel(excel_file, index_col=0)

            services_and_requirements_list = []
            for application in project_data["applications"]:
                services_and_requirements_list.extend(application["requirements"][:])

            risks = [Risk(**risk) for risk in project_data["riskManager"]["risks"]]
            services_and_requirements = [Requirement(**requirement) for requirement in services_and_requirements_list]

            services = [r for r in services_and_requirements if r.shortName.split(".")[0].startswith("SS")]
            risk_results_services = calculate_impact(risks, services, mitigation_matrix)

            requirements = [r for r in services_and_requirements if not r.shortName.split(".")[0].startswith("SS")]
            risk_results_requirements = calculate_impact(risks, requirements, mitigation_matrix)

            return render(request, 'result.html', {
                'upload_date': timezone.now(),
                'project_id': project_data.get('project_id', 'Неизвестный ID'),
                'session_number': session_number,
                'risks_services': risk_results_services.to_html(),
                'risks_requirements': risk_results_requirements.to_html(),
            })
    else:
        form = FileUploadForm()
    return render(request, 'upload.html', {'form': form})

