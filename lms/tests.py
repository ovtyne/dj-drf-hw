from rest_framework import status

from lms.models import Subscription, Course, Lesson
from users.models import User
from rest_framework.test import APITestCase


class LessonTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            email='testuser@gmail.com',
            password='testpassword'
        )
        self.client.force_authenticate(user=self.user)

        self.lesson = Lesson.objects.create(
            title='Test Lesson',
            description='Test description',
            user=self.user
        )

    def test_create_lesson(self):
        data = {
            'title': 'Test',
            'description': 'Test',
        }

        response = self.client.post('/lessons/create/', data, format='json')

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertTrue(
            Lesson.objects.filter(title='Test').exists()
        )

    def test_retrieve_lesson(self):
        response = self.client.get(f'/lessons/list/{self.lesson.pk}')

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_list_lesson(self):
        response = self.client.get(f'/lessons/')

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_update_lesson(self):
        updated_data = {
            'title': 'Updated Lesson Title',
            'description': 'Updated Lesson description',
        }

        response = self.client.put(f'/lessons/update/{self.lesson.pk}', updated_data,
                                   format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, 'Updated Lesson Title')
        self.assertEqual(self.lesson.description, 'Updated Lesson description')

    def test_destroy_lesson(self):
        self.client.delete(f'/lessons/delete/{self.lesson.pk}')

        self.assertFalse(
            Lesson.objects.filter(title='Test Lesson').exists()
        )


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email='testuser@gmail.com',
            password='testpassword'
        )
        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(
            title='Test Course',
            description='Test description',
            user=self.user
        )

        self.course_for_sub_view = Course.objects.create(
            title='Test View',
            description='Test description',
            user=self.user
        )

        self.course_for_sub_del = Course.objects.create(
            title='Del Course',
            description='Test description',
            user=self.user
        )

        self.sub_for_del = Subscription.objects.create(
            course=self.course_for_sub_del
        )

    def test_create_subscription(self):
        data = {
            'course': self.course.pk
        }

        response = self.client.post('/subscription/create/', data, format='json')

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertTrue(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )

    def test_sub_on_course_view(self):
        data = {
            'course': self.course_for_sub_view.pk
        }
        self.client.post('/subscription/create/', data, format='json')

        response = self.client.get('/course/')

        self.assertEqual(
            response.json(),
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": 8,
                        "lesson_count": 0,
                        "lessons_list": [],
                        "subscription_status": True,
                        "title": "Test View",
                        "preview": None,
                        "description": "Test description",
                        "user": 8
                    }
                ]
            }
        )

    def test_destroy_subscription(self):
        self.client.delete(f'/subscription/delete/{self.sub_for_del.pk}')

        self.assertFalse(
            Subscription.objects.filter(user=self.user, course=self.course_for_sub_del).exists()
        )

