from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from lms.apps import LmsConfig
from rest_framework.routers import DefaultRouter, SimpleRouter

from lms.views import CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView, PaymentListAPIView

app_name = LmsConfig.name

router = SimpleRouter()
router.register(r'course', CourseViewSet, basename='course')

urlpatterns = [
    path('create/', LessonCreateAPIView.as_view(), name='lms-create'),
    path('', LessonListAPIView.as_view(), name='lms-list'),
    path('detail/<int:pk>', LessonRetrieveAPIView.as_view(), name='lms-detail'),
    path('update/<int:pk>', LessonUpdateAPIView.as_view(), name='lms-update'),
    path('delete/<int:pk>', LessonDestroyAPIView.as_view(), name='lms-delete'),

    path('payment/', PaymentListAPIView.as_view(), name='payment-list'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + router.urls
