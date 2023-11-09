import os

import stripe
from django_filters import OrderingFilter
from rest_framework import generics, viewsets, status
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from lms.models import Course, Lesson, Payment, Subscription
from lms.paginators import LmsPaginator
from lms.serializers import CourseSerializer, LessonSerializer, PaymentSerializer, SubscriptionSerializer, \
    PaymentStripeSerializer
from lms.services import StripePayment


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    # permission_classes = [IsAuthenticated]


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = LmsPaginator


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    queryset = Payment.objects.all()
    filter_backends = [SearchFilter, OrderingFilter]
    filterset_fields = ['course', 'lesson']
    ordering_fields = ('payment_date',)


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
    permission_classes = [IsAuthenticated]


class SubscriptionViewSet(ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]





