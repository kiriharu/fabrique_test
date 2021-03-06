from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.request import Request
from rest_framework.serializers import ValidationError
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
    CreateSurveyAnswerSerializer, StartSurveySerializer
)
from surveys.models import (
    Survey,
    Question,
    Answer,
    StartedSurvey,
    SurveyAnswer
)
from surveys.services import check_question_belong_to_survey, check_only_one_answer


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
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "description"]

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
        methods=['POST'],
        permission_classes=[],
        queryset=Survey.get_active(),
        serializer_class=StartSurveySerializer
    )
    def start(self, request, pk=None):
        survey = self.get_object()

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get("user")
        started_survey_id = StartedSurvey.start_passing(
            survey_id=survey.pk, user=user
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
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ["question_type", "survey"]
    search_fields = ["text"]


class AnswerViewSet(AdminModelViewSet):
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["text"]
    filterset_fields = ["question"]


class StartedSurveyView(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    queryset = StartedSurvey.objects.prefetch_related(
        "surveyanswer_set",
    ).all()
    serializer_class = StartedSurveySerializer

    def list(self, request: Request, *args, **kwargs):
        user = request.query_params.get("user")
        if not user:
            raise ValidationError("Provide user argument in query")
        queryset = self.filter_queryset(
            StartedSurvey.objects.prefetch_related(
                "surveyanswer_set",
            ).filter(
                user=int(user)
            ))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(
        detail=True,
        methods=["POST"],
        serializer_class=CreateSurveyAnswerSerializer,
        queryset=StartedSurvey.objects.select_related("survey")
    )
    def answer(self, request, pk=None):
        started_survey: StartedSurvey = self.get_object()
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data.get("user")
        question = serializer.validated_data.get("question")
        answer = serializer.validated_data.get("answer")
        text = serializer.validated_data.get("text")

        if not user == started_survey.user:
            raise ValidationError({"user": "This user is not started this survey"})

        if not check_question_belong_to_survey(started_survey, question):
            raise ValidationError({"question": "Selected question does not belong to survey"})

        if check_only_one_answer(started_survey, question):
            raise ValidationError({"answer": "Only one answer allowed in text/single choose question type"})

        result = SurveyAnswer.add(question, started_survey, answer, text)
        return Response({"ok": result.id})
