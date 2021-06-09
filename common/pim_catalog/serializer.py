from .models import *
from rest_framework import serializers, fields


class PimPropSerializer(serializers.ModelSerializer):

    class Meta:
        model = PimProp
        fields = ('site_name', 'group_by_parent')


