from rest_framework import serializers

from phoad.photosmap.models import Photo


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('name', 'image', 'latitude', 'longitude', 'timestamp')