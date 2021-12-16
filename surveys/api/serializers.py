from rest_framework import serializers

from surveys.models import Survey


class SurveySerializer(serializers.ModelSerializer):

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
