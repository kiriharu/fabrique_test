from rest_framework import serializers

from surveys.models import (
    Survey,
    Question,
    Answer,
    StartedSurvey,
    SurveyAnswer
)


class SurveySerializer(serializers.ModelSerializer):

    def validate(self, data):
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError(
                {"start_date": "Start date is bigger then end date"}
            )
        return data

    class Meta:
        model = Survey
        fields = (
            "id",
            "name",
            "start_date",
            "end_date",
            "description"
        )


class UpdateSurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = (
            "id",
            "name",
            "end_date",
            "description"
        )


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = (
            "id",
            "text",
            "survey",
            "question_type"
        )


class AnswerSerializer(serializers.ModelSerializer):

    def validate(self, data):
        question: Question = data['question']
        if question.question_type == Question.TEXT:
            raise serializers.ValidationError(
                {"text": f'Question with type {Question.TEXT} can\'t have predefined answers'}
            )
        return data

    class Meta:
        model = Answer
        fields = (
            "id",
            "question",
            "text"
        )


class StartSurveySerializer(serializers.Serializer):
    user = serializers.IntegerField()


class SurveyAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyAnswer
        fields = (
            "answer",
            "survey",
            "text",
            "question"
        )


class StartedSurveySerializer(serializers.ModelSerializer):

    class AnswersSerializer(serializers.ModelSerializer):
        class Meta:
            model = SurveyAnswer
            fields = (
                "answer",
                "text",
                "question"
            )

    answers = AnswersSerializer(many=True, source="surveyanswer_set")

    class Meta:
        model = StartedSurvey
        fields = (
            "id",
            "survey",
            "answers",
        )


class CreateSurveyAnswerSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField()

    class Meta:
        model = SurveyAnswer
        fields = (
            "question",
            "answer",
            "text",
            "user"
        )

    def validate(self, data):

        question: Question = data.get("question")
        answer: Answer = data.get("answer")
        text = data.get("text")

        if answer and text:
            raise serializers.ValidationError(
                {"answer": "Text or answer should be defined"}
            )

        if question.question_type == Question.TEXT:
            if not text:
                raise serializers.ValidationError(
                    {"text": "Text answer is required in text question type"}
                )

        if question.question_type in (Question.SINGLE_CHOICE, Question.MULTIPLE_CHOICE):
            if not answer:
                raise serializers.ValidationError(
                    {"question": "Answer is required in single/multiple question type"}
                )

        if question and answer and question.pk != answer.question_id:
            raise serializers.ValidationError(
                {"answer": "This answer does not belong to sended question"}
            )

        return data
