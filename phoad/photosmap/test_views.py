import datetime

from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from nose.tools import eq_
from rest_framework import status
from rest_framework.test import APITestCase

from tests.utils import IntegrationTest


class PhotosTestCase(IntegrationTest):
    """
    Tests /photos list operations.
    """

    def test_should_throw_401_when_uploading_photo_without_credentials(self):
        # given
        image = self.create_image()
        post_data = {
            'latitude': 37.785834,
            'longitude': -122.406417,
            'image': image,
            'timestamp': datetime.datetime.now()
        }

        # when
        response = self.client.post(self.photos_url, post_data, 'multipart')

        # then
        eq_(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_throw_400_when_sending_not_complete_data(self):
        # given
        post_data = {
            'latitude': 37.785834,
            'longitude': -122.406417,
            'timestamp': datetime.datetime.now()
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_data["token"]}')

        # when
        response = self.client.post(self.photos_url, post_data, 'multipart')

        # then
        eq_(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_should_upload_photo(self):
        # given
        post_data = {
            'latitude': 37.785834,
            'longitude': -122.406417,
            'image': self.create_image(),
            'timestamp': datetime.datetime.now(),
            'name': 'testfile'
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_data["token"]}')

        # when
        response = self.client.post(self.photos_url, post_data, 'multipart')

        # then
        eq_(response.status_code, status.HTTP_201_CREATED)

    def test_should_throw_400_when_sending_file_not_being_photo(self):
        # given
        post_data = {
            'latitude': 37.785834,
            'longitude': -122.406417,
            'image': self.create_js_file(),
            'timestamp': datetime.datetime.now()
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_data["token"]}')

        # when
        response = self.client.post(self.photos_url, post_data, 'multipart')

        # then
        eq_(response.status_code, status.HTTP_400_BAD_REQUEST)

    def create_image(self):
        image_path = "%s/tests/resources/cat-mask.jpg" % settings.BASE_DIR
        with open(image_path, 'rb') as f:
            image = SimpleUploadedFile(name='cat-mask.jpg', content=f.read(),
                                       content_type='image/jpg')
        return image

    def create_js_file(self):
        image_path = "%s/tests/resources/file.js" % settings.BASE_DIR
        with open(image_path, 'rb') as f:
            image = SimpleUploadedFile(name='cat-mask.js', content=f.read(),
                                       content_type='image/jpg')
        return image


class PhotosListBasedOnLocationTestCase(IntegrationTest):
    def test_should_throw_401_in_case_of_getting_location_without_credentials(self):
        # when
        response = self.client.get(self.photos_at_location_url)

        # then
        eq_(response.status_code, status.HTTP_401_UNAUTHORIZED)
