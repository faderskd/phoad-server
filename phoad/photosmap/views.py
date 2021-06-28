from math import inf

from django.conf import settings
from rest_framework import mixins, viewsets, status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from phoad.photosmap.models import Photo
from phoad.photosmap.serializers import PhotoSerializer
from phoad.users.permissions import IsUserOrReadOnly
from photosmap.dto import LocationDiff, LocationValidator, LocationThresholdValidator


class PhotosViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Photo.objects.all().order_by("-timestamp")
    serializer_class = PhotoSerializer
    permission_classes = (IsAuthenticated, IsUserOrReadOnly,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class PhotosListBasedOnLocation(generics.ListAPIView):
    serializer_class = PhotoSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        latitude = self.kwargs.get('latitude')
        longitude = self.kwargs.get('longitude')
        threshold = self.kwargs.get('location-threshold', inf)

        location = LocationValidator.validate(latitude, longitude)
        validated_threshold = LocationThresholdValidator.validate(threshold)
        validated_threshold.threshold = min(validated_threshold.threshold, settings.MAX_LOCATION_DIFF)

        location_diff = LocationDiff.from_location(location, validated_threshold)
        return Photo.objects.filter(latitude__gte=location_diff.min_latitude,
                                    latitude__lte=location_diff.max_latitude,
                                    longitude__gte=location_diff.min_longitude,
                                    longitude__lte=location_diff.max_longitude)
