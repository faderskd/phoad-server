from math import inf

from django.conf import settings
from rest_framework import mixins, viewsets, generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from phoad.photosmap.models import Photo
from phoad.photosmap.serializers import PhotoSerializer
from photosmap.dto import LocationDiff, LocationValidator, LocationThresholdValidator
from photosmap.permissions import IsOwner


class PhotosViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Photo.objects.all().order_by("-timestamp")
    serializer_class = PhotoSerializer
    permission_classes = (IsAuthenticated, IsOwner,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def filter_queryset(self, queryset):
        return queryset.filter(owner=self.request.user)


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 200


class PhotosListBasedOnLocation(generics.ListAPIView):
    serializer_class = PhotoSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        latitude = self.request.query_params.get('latitude')
        longitude = self.request.query_params.get('longitude')
        threshold = self.request.query_params.get('location-threshold', inf)

        location = LocationValidator.validate(latitude, longitude)
        validated_threshold = LocationThresholdValidator.validate(threshold)
        validated_threshold.threshold = min(validated_threshold.threshold, settings.MAX_LOCATION_DIFF)

        location_diff = LocationDiff.from_location(location, validated_threshold)
        return Photo.objects.filter(owner=self.request.user,
                                    latitude__gte=location_diff.min_latitude,
                                    latitude__lte=location_diff.max_latitude,
                                    longitude__gte=location_diff.min_longitude,
                                    longitude__lte=location_diff.max_longitude).order_by("-timestamp")
