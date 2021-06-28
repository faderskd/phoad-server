import factory
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from nose.tools import eq_

from tests.factories import UserFactory


class IntegrationTest(APITestCase):

    def setUp(self):
        self.photos_url = reverse('photo-list')
        self.photos_at_location_url = reverse('photos-at-location')
        self.users_url = reverse('user-list')
        self.user_data = factory.build(dict, FACTORY_CLASS=UserFactory)
        self.user_data['token'] = self.create_user(self.user_data)

    def create_user(self, user):
        response = self.client.post(self.users_url, user)
        eq_(response.status_code, status.HTTP_201_CREATED)
        return response.data['auth_token']
