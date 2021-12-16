from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register('surveys', views.SurveyViewSet)

urlpatterns = router.urls
