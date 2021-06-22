from django.db.models.query_utils import Q

from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from features.models import Feature
from features.serializers import FeatureSerializer

from utils.mixins import get_object_or_None


class FeatureViewSet(ViewSet):
    """ feature endpoints
    """
    serializer_class = FeatureSerializer

    def get(self, *args, **kwargs):
        id = self.request.GET.get('id', '')
        if id:
            instance = get_object_or_None(Feature, id=id)
            if instance:
                serializer = self.serializer_class(instance=instance)
                return Response(serializer.data, status=200)
            return Response(status=400)
        else:
            serializer = self.serializer_class(
                instance=Feature.objects.filter(is_deleted=False).order_by('-date_created'),
                many=True,
            )
            return Response(serializer.data, status=200)

    def get_values(self, *args, **kwargs):
        serializer = self.serializer_class(
            instance=Feature.objects.filter(is_deleted=False, feat_type=Feature.VALUES).order_by('-date_created'),
            many=True,
        )
        return Response(serializer.data, status=200)

    def get_principles(self, *args, **kwargs):
        serializer = self.serializer_class(
            instance=Feature.objects.filter(is_deleted=False, feat_type=Feature.PRINCIPLES).order_by('-date_created'),
            many=True,
        )
        return Response(serializer.data, status=200)

    def add(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=403)

    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            instance=Feature.objects.get(id=self.request.data.get('id')),
            data=self.request.data,
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=403)

    def delete(self, *args, **kwargs):
        try:
            feature = Feature.objects.get(id=self.request.GET.get('id'))
            feature.is_deleted = True
            feature.save()
        except:
            return Response({'status': 'Something went wrong try again'}, status=400)
        return Response({'status': 'Success'}, status=200)
