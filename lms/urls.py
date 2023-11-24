from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from lms.apps import LmsConfig
from rest_framework.routers import DefaultRouter, SimpleRouter

from lms.views import CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView, PaymentListAPIView, PaymentCreateAPIView, \
    PaymentRetrieveAPIView, SubscriptionCreateAPIView, SubscriptionDestroyAPIView

app_name = LmsConfig.name

router = SimpleRouter()
router.register(r'course', CourseViewSet, basename='course')

urlpatterns = [
    path('lessons/create/', LessonCreateAPIView.as_view(), name='lessons_create'),
    path('lessons/list/', LessonListAPIView.as_view(), name='lessons_list'),
    path('lessons/retrieve/<int:pk>', LessonRetrieveAPIView.as_view(), name='lessons_retrieve'),
    path('lessons/detail/<int:pk>', LessonRetrieveAPIView.as_view(), name='lessons_detail'),
    path('lessons/update/<int:pk>', LessonUpdateAPIView.as_view(), name='lessons_update'),
    path('lessons/delete/<int:pk>', LessonDestroyAPIView.as_view(), name='lessons_delete'),

    path('payment/', PaymentListAPIView.as_view(), name='payment_list'),
    path('payment/create', PaymentCreateAPIView.as_view(), name='payment_create'),
    path('payment/<int:pk>', PaymentRetrieveAPIView.as_view(), name='payment_get'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('subscription/create/', SubscriptionCreateAPIView.as_view(), name='sub_create'),
    path('subscription/delete/<int:pk>/', SubscriptionDestroyAPIView.as_view(), name='sub_delete'),

] + router.urls
