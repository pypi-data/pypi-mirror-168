from rest_framework import serializers

from netbox.api.serializers import NetBoxModelSerializer
from ..models import Probe
from dcim.api.serializers import NestedDeviceSerializer, NestedSiteSerializer, NestedLocationSerializer
from netbox.api.serializers import WritableNestedSerializer

class ProbeSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:inventory_monitor-api:probe-detail'
    )
    device = NestedDeviceSerializer()
    site = NestedSiteSerializer(allow_null=True)
    location = NestedLocationSerializer(allow_null=True)

    class Meta:
        model = Probe
        fields = [
            'id',
            'url',
            'display',
            'name',
            'time',
            'serial',
            'part',
            'device_descriptor',
            'device',
            'site_descriptor',
            'site',
            'location_descriptor',
            'location',
            'description',
            'category',
            'discovered_data',
            'tags',
            'comments',
            'custom_fields',
        ]

class NestedProbeSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:inventory_monitor-api:probe-detail'
    )

    class Meta:
        model = Probe
        fields = ['id', 'url', 'display', 'name', 'serial', 'time']