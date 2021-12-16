from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register('surveys', views.SurveyViewSet)
router.register('questions', views.QuestionViewSet)
router.register('answers', views.AnswerViewSet)

urlpatterns = router.urls
