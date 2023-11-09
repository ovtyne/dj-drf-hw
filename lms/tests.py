from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from lms.models import Lesson, Course, Subscription
from users.models import User


class LessonTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            email='user@gmail.com',
            password='password'
        )
        self.client.force_authenticate(user=self.user)

        self.lesson = Lesson.objects.create(
            title='Lesson',
            description='description',
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
            'title': 'Updated Title',
            'description': 'Updated Lesson',
        }

        response = self.client.put(f'/lessons/update/{self.lesson.pk}', updated_data,
                                   format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, 'Updated Title')
        self.assertEqual(self.lesson.overview, 'Updated Lesson')

    def test_destroy_lesson(self):
        self.client.delete(f'/lessons/delete/{self.lesson.pk}')

        self.assertFalse(
            Lesson.objects.filter(title='Test Lesson').exists()
        )


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email='user@gmail.com',
            password='password'
        )
        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(
            title='Test Course',
            description='Test Overview',
            user=self.user
        )

        self.course_for_sub_view = Course.objects.create(
            title='Test View',
            description='Test Overview',
            user=self.user
        )

        self.course_for_sub_del = Course.objects.create(
            title='Del Course',
            description='Test Overview',
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
                        "description": "Test Overview",
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
