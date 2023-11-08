from rest_framework import serializers

from lms.models import Course, Lesson, Payment, Subscription
from lms.validators import VideoValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [
            VideoValidator(field='video')
        ]


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.IntegerField(source='lesson_set.all.count')
    lesson = LessonSerializer(many=True)

    class Meta:
        model = Course
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = '__all__'
