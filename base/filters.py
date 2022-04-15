import django_filters

from .models import *

class RecordsFilter(django_filters.FilterSet):
    class Meta:
        model = record
        fields = '__all__'