from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework.viewsets import ViewSet

from asur import urls

from asur.views import FileUploadView

schema_view = get_schema_view(
    openapi.Info(
        title="API",
        default_version='v2',
        description="Выгрузка JSON файлов",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('upload/', FileUploadView.as_view(), name='upload'),
    path('up/', include(urls)),
]
