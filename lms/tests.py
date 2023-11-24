from rest_framework import status
from rest_framework.reverse import reverse

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

        response = self.client.post('/lms/lessons/create/', data, format='json')

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertTrue(
            Lesson.objects.filter(title='Test').exists()
        )

    def test_retrieve_lesson(self):
        response = self.client.get(f'/lms/lessons/retrieve/{self.lesson.pk}')

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_list_lesson(self):
        response = self.client.get(f'/lms/lessons/list/')

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_update_lesson(self):
        updated_data = {
            'title': 'Updated Lesson Title',
            'description': 'Updated Lesson description',
        }

        response = self.client.put(f'/lms/lessons/update/{self.lesson.pk}', updated_data,
                                   format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, 'Updated Lesson Title')
        self.assertEqual(self.lesson.description, 'Updated Lesson description')

    def test_destroy_lesson(self):
        self.client.delete(f'/lms/lessons/delete/{self.lesson.pk}')

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
            title='test_course',
            description='test_course',
            user=self.user
        )

    # def test_create(self):
    #     subscription = {
    #         "user": self.user.pk,
    #         "course": self.course.pk
    #     }
    #
    #     response = self.client.post(reverse('lms:sub_create'), data=subscription)
    #
    #     self.assertEqual(
    #         response.status_code,
    #         status.HTTP_201_CREATED
    #     )

    def test_delete(self):
        course = Subscription.objects.create(
            user=self.user,
            course=self.course
        )

        response = self.client.delete(
            reverse('lms:sub_delete', kwargs={'pk': course.pk})
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
