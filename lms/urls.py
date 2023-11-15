from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from lms.apps import LmsConfig
from rest_framework.routers import DefaultRouter, SimpleRouter

from lms.views import CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView, PaymentListAPIView, SubscriptionViewSet, PaymentCreateAPIView, \
    PaymentRetrieveAPIView

app_name = LmsConfig.name

router = SimpleRouter()
router.register(r'course', CourseViewSet, basename='course')
router.register(r'subscriptions', SubscriptionViewSet, basename='subscriptions')

urlpatterns = [
    path('lessons/create/', LessonCreateAPIView.as_view(), name='lessons_create'),
    path('lessons/', LessonListAPIView.as_view(), name='lessons_list'),
    path('lessons/detail/<int:pk>', LessonRetrieveAPIView.as_view(), name='lessons_detail'),
    path('lessons/update/<int:pk>', LessonUpdateAPIView.as_view(), name='lessons_update'),
    path('lessons/delete/<int:pk>', LessonDestroyAPIView.as_view(), name='lessons_delete'),

    path('payment/', PaymentListAPIView.as_view(), name='payment_list'),
    path('payment/create', PaymentCreateAPIView.as_view(), name='payment_create'),
    path('payment/<int:pk>', PaymentRetrieveAPIView.as_view(), name='payment_get'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

] + router.urls
