import os

import stripe
from django_filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from lms.models import Course, Lesson, Payment, Subscription
from lms.paginators import LmsPaginator
from lms.permissions import IsOwner, IsMember, IsModerator
from lms.serializers import CourseSerializer, LessonSerializer, PaymentSerializer, SubscriptionSerializer, \
    PaymentStripeSerializer
from lms.services import StripePayment
from lms.tasks import send_description_mail
from users.models import UserRoles


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsMember]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.user = self.request.user
        new_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = LmsPaginator

    def get_queryset(self):
        user = self.request.user
        if user.role == UserRoles.MODERATOR:
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(user=user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = LmsPaginator

    def perform_create(self, serializer):
        new_course = serializer.save()
        new_course.user = self.request.user
        new_course.save()

    def perform_update(self, serializer):
        updated_course = serializer.save()
        send_description_mail.delay(
            updated_course.pk,
            updated_course.title,
            updated_course.user.email,
            updated_course.user.pk
        )


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]
    queryset = Payment.objects.all()
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['course', 'lesson']
    ordering_fields = ('date', 'method',)

    def get_queryset(self):
        user = self.request.user
        if user.role == UserRoles.MODERATOR:
            return Payment.objects.all()
        else:
            return Payment.objects.filter(user=user)


class PaymentCreateAPIView(generics.CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def create(self, request, *args, **kwargs):
        payment_data = request.data
        payment_serializer = self.get_serializer(data=payment_data)

        if payment_serializer.is_valid():
            payment_serializer.save()

            stripe_handler = StripePayment(
                paid_object=payment_data.get('course_paid', payment_data.get('lesson_paid')),
                payment_method=payment_data.get('payment_method'),
                payment_amount=payment_data.get('payment_amount')
            )
            try:
                stripe_id = stripe_handler.create()
                payment_serializer.instance.stripe_id = stripe_id
                payment_serializer.instance.save()
                return Response(payment_serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = PaymentStripeSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class SubscriptionViewSet(ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]
