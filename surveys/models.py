from datetime import datetime

from django.db import models


class Survey(models.Model):

    name = models.CharField(max_length=200)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    description = models.TextField()

    def __str__(self):
        return self.name

    @classmethod
    def get_active(cls):
        return cls.objects.filter(
            start_date__lte=datetime.now()
        ).filter(
            end_date__gte=datetime.now()
        )


class Question(models.Model):
    TEXT = "TEXT"
    SINGLE_CHOICE = "SINGLE_CHOICE"
    MULTIPLE_CHOICE = "MULTIPLE_CHOICE"

    QUESTION_TYPE = (
        (TEXT, "Text question"),
        (SINGLE_CHOICE, "Question with one choice"),
        (MULTIPLE_CHOICE, "Question with multiple choices")
    )
    survey = models.ForeignKey('Survey', on_delete=models.CASCADE)
    text = models.TextField()
    question_type = models.CharField(choices=QUESTION_TYPE, max_length=15)

    def __str__(self):
        return f"{self.text} : {self.question_type}"


class Answer(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return self.text
