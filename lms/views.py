from django_filters import OrderingFilter
from rest_framework import generics, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet

from lms.models import Course, Lesson, Payment
from lms.serializers import CourseSerializer, LessonSerializer, CourseLessonSerializer, PaymentSerializer


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class CourseLessonListAPIView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = CourseLessonSerializer


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['cource_or_lesson']
    ordering_fields = ['payment_date']
