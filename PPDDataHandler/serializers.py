from .models import PPDRecord
from rest_framework import serializers


class PPDRecordSelializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        FIELDS = [
            'transaction_unique_id',
            'price',
            'date_of_transfer',
            'postcode',
            'property_type',
            'old_new',
            'duration',
            'paon',
            'saon',
            'street',
            'locality',
            'town_city',
            'district',
            'county',
            'ppd_category_type',
            'record_status',
        ]
        model = PPDRecord
        fields = FIELDS
