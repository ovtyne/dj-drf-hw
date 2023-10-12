from django.urls import path

from lms.apps import LmsConfig
from rest_framework.routers import DefaultRouter, SimpleRouter

from lms.views import LmsViewSet, CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView

app_name = LmsConfig.name

router = DefaultRouter()
router.register(r'lms', LmsViewSet, basename='lms')

urlpatterns = [
    path('lms/create/', LessonCreateAPIView.as_view(), name='lms-create'),
    path('lms/', LessonListAPIView.as_view(), name='lms-list'),
    path('lms/detail/<int:pk>', LessonRetrieveAPIView.as_view(), name='lms-detail'),
    path('lms/update/<int:pk>', LessonUpdateAPIView.as_view(), name='lms-update'),
    path('lms/delete/<int:pk>', LessonDestroyAPIView.as_view(), name='lms-delete'),
] + router.urls

router = SimpleRouter()
router.register(r'course', CourseViewSet, basename='course')
urlpatterns += router.urls
