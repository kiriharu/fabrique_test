from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from surveys.api.serializers import (
    SurveySerializer,
    UpdateSurveySerializer,
    QuestionSerializer,
    AnswerSerializer,
    StartedSurveySerializer,
    CreateSurveyAnswerSerializer
)
from surveys.models import (
    Survey,
    Question,
    Answer,
    StartedSurvey, SurveyAnswer
)


class AdminModelViewSet(viewsets.ModelViewSet):
    authentication_classes = [BasicAuthentication]

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            self.permission_classes = []
        elif self.action in ("create", "update", "partial_update", "destroy"):
            self.permission_classes = [IsAdminUser, IsAuthenticated]
        return super().get_permissions()


class SurveyViewSet(AdminModelViewSet):
    serializer_class = SurveySerializer
    queryset = Survey.objects.all()

    def get_permissions(self):
        if self.action == "list":
            self.permission_classes = [IsAdminUser, IsAuthenticated]
            return [permission() for permission in self.permission_classes]
        return super().get_permissions()

    @action(detail=False, methods=['GET'], permission_classes=[])
    def active(self, request, pk=None):
        active_surveys = Survey.get_active()
        serializer = self.get_serializer(active_surveys, many=True)
        return Response(serializer.data)

    @action(
        detail=True,
        methods=['GET'],
        permission_classes=[],
        queryset=Survey.get_active()
    )
    def start(self, request, pk=None):
        survey = self.get_object()
        started_survey_id = StartedSurvey.start_passing(
            survey_id=survey.pk, user_id=request.user.id
        )
        return Response({"started": started_survey_id})

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


class StartedSurveyView(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    queryset = StartedSurvey.objects.prefetch_related(
        "surveyanswer_set",
    ).all()
    serializer_class = StartedSurveySerializer

    @action(
        detail=True,
        methods=["POST"],
        serializer_class=CreateSurveyAnswerSerializer
    )
    def answer(self, request, pk=None):
        started_survey: StartedSurvey = self.get_object()
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        question = serializer.validated_data.get("question")
        answer = serializer.validated_data.get("answer")
        text = serializer.validated_data.get("text")

        result = SurveyAnswer.add(question, started_survey, answer, text)
        return Response({"ok": result.id})
