from rest_framework import serializers

from surveys.models import Survey, Question, Answer


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

    class Meta:
        model = Answer
        fields = (
            "id",
            "question",
            "text"
        )
