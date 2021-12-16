from rest_framework import viewsets

from surveys.api.serializers import (
    SurveySerializer,
    UpdateSurveySerializer
)
from surveys.models import Survey


class SurveyViewSet(viewsets.ModelViewSet):
    serializer_class = SurveySerializer
    queryset = Survey.objects.all()

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.action in ("update", "partial_update"):
            return UpdateSurveySerializer
        return serializer_class

