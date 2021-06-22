from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _

from features.models import Feature


class FeatureSerializer(serializers.ModelSerializer):

    class Meta:
        model = Feature
        fields = '__all__'