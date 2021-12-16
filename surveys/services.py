from surveys.models import Question, StartedSurvey, SurveyAnswer


def check_question_belong_to_survey(started_survey: StartedSurvey, question: Question) -> bool:
    survey_questions = Question.objects.filter(survey=started_survey.survey)
    if question in survey_questions:
        return True


def check_only_one_answer(started_survey: StartedSurvey, question: Question) -> bool:
    user_answers = SurveyAnswer.objects.filter(
        question=question, survey=started_survey
    )
    if question.question_type in (question.TEXT, question.SINGLE_CHOICE) and user_answers.count() > 0:
        return True
