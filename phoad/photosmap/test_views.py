import datetime

from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from nose.tools import eq_
from rest_framework import status

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

    def create_js_file(self):
        image_path = "%s/tests/resources/file.js" % settings.BASE_DIR
        with open(image_path, 'rb') as f:
            image = SimpleUploadedFile(name='cat-mask.js', content=f.read(),
                                       content_type='image/jpg')
        return image


class PhotosListBasedOnLocationTestCase(IntegrationTest):
    def test_should_throw_401_when_getting_photos_without_credentials(self):
        # when
        response = self.client.get(self.photos_at_location_url)

        # then
        eq_(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_throw_400_when_getting_photos_with_invalid_location_threshold(self):
        # given
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_data["token"]}')

        # when
        response = self.client.get(self.photos_at_location_url_with_params(location_threshold="threshold",
                                                                           latitude=1, longitude=2))

        # then
        self.assertContains(response, text="Threshold must be float number", status_code=status.HTTP_400_BAD_REQUEST)

        # when
        response = self.client.get(self.photos_at_location_url_with_params(latitude="aa", longitude=2))

        # then
        self.assertContains(response, text="Latitude and longitude must be float numbers",
                            status_code=status.HTTP_400_BAD_REQUEST)

        # when
        response = self.client.get(self.photos_at_location_url_with_params(latitude=1, longitude="aa"))

        # then
        self.assertContains(response, text="Latitude and longitude must be float numbers",
                            status_code=status.HTTP_400_BAD_REQUEST)

        # when
        response = self.client.get(self.photos_at_location_url_with_params(longitude=2))

        # then
        self.assertContains(response, text="Latitude and longitude must not be null",
                            status_code=status.HTTP_400_BAD_REQUEST)

        # when
        response = self.client.get(self.photos_at_location_url_with_params(latitude=1))

        # then
        self.assertContains(response, text="Latitude and longitude must not be null",
                            status_code=status.HTTP_400_BAD_REQUEST)

    def test_should_return_images_at_locations_within_reactangle_area_bordered_by_thresholds(self):
        # given
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_data["token"]}')
        image = self.create_image()
        post_data = {
            'latitude': 37.785834,
            'longitude': -122.406417,
            'image': image,
            'timestamp': datetime.datetime.now(),
            'name': 'myimage'
        }
        eq_(self.client.post(self.photos_url, post_data, 'multipart').status_code, status.HTTP_201_CREATED)

        # when
        response = self.client.get(self.photos_at_location_url_with_params(latitude=37.79, longitude=-122.41))

        # then
        eq_(response.status_code, status.HTTP_200_OK)
        eq_(response.json()['count'], 1)

        # when
        response = self.client.get(self.photos_at_location_url_with_params(latitude=39, longitude=-123))

        # then
        eq_(response.status_code, status.HTTP_200_OK)
        eq_(response.json()['count'], 0)

    def photos_at_location_url_with_params(self, **kwargs):
        return self.photos_at_location_url + "?" + "&".join(
            "%s=%s" % (k.replace('_', '-'), v) for k, v in kwargs.items())
