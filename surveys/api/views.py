from rest_framework import viewsets

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


class SurveyViewSet(viewsets.ModelViewSet):
    serializer_class = SurveySerializer
    queryset = Survey.objects.all()

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.action in ("update", "partial_update"):
            return UpdateSurveySerializer
        return serializer_class


class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()


class AnswerViewSet(viewsets.ModelViewSet):
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()
