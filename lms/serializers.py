import stripe
from django.conf import settings
from rest_framework import serializers

from lms.models import Course, Lesson, Payment, Subscription
from lms.validators import VideoValidator


class LessonSerializer(serializers.ModelSerializer):
    video = serializers.CharField(validators=[VideoValidator], read_only=True)

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.IntegerField(source='lesson_set.all.count', read_only=True)
    lessons_list = LessonSerializer(many=True, read_only=True)
    subscription_status = serializers.SerializerMethodField(read_only=True)

    def get_subscription_status(self, obj):
        return Subscription.objects.filter(user=obj.user, course=obj)

    class Meta:
        model = Course
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class PaymentStripeSerializer(PaymentSerializer):
    stripe = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = '__all__'

    def get_stripe(self, instance):
        stripe.api_key = settings.STRIPE_API_KEY
        stripe_data = stripe.PaymentIntent.retrieve(
            instance.stripe_id,
        )
        return stripe_data


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
