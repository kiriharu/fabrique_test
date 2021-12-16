from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from surveys.api.serializers import (
    SurveySerializer,
    UpdateSurveySerializer,
    QuestionSerializer,
    AnswerSerializer
)
from surveys.models import (
    Survey,
    Question,
    Answer
)


class AdminModelViewSet(viewsets.ModelViewSet):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAdminUser, IsAuthenticated]


class SurveyViewSet(AdminModelViewSet):
    serializer_class = SurveySerializer
    queryset = Survey.objects.all()

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.action in ("update", "partial_update"):
            return UpdateSurveySerializer
        return serializer_class


class QuestionViewSet(AdminModelViewSet):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()


class AnswerViewSet(AdminModelViewSet):
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()
