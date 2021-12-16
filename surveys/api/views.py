from rest_framework import viewsets

from surveys.api.serializers import SurveySerializer
from surveys.models import Survey


class SurveyViewSet(viewsets.ModelViewSet):
    serializer_class = SurveySerializer
    queryset = Survey.objects.all()
