from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register('surveys', views.SurveyViewSet)
router.register('questions', views.QuestionViewSet)
router.register('answers', views.AnswerViewSet)
router.register('started', views.StartedSurveyView)


urlpatterns = router.urls
