from django.urls import path

from lms.apps import LmsConfig
from rest_framework.routers import DefaultRouter, SimpleRouter

from lms.views import CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView

app_name = LmsConfig.name

# router = DefaultRouter()
# router.register(r'lms', LmsViewSet, basename='lms')

router = SimpleRouter()
router.register(r'course', CourseViewSet, basename='course')

urlpatterns = [
    path('create/', LessonCreateAPIView.as_view(), name='lms-create'),
    path('', LessonListAPIView.as_view(), name='lms-list'),
    path('detail/<int:pk>', LessonRetrieveAPIView.as_view(), name='lms-detail'),
    path('update/<int:pk>', LessonUpdateAPIView.as_view(), name='lms-update'),
    path('delete/<int:pk>', LessonDestroyAPIView.as_view(), name='lms-delete'),
] + router.urls


# urlpatterns += router.urls
