import django_filters
from django.db.models import Q
from .models import Probe
from extras.filters import TagFilter
from dcim.models import Device


class ProbeFilterSet(django_filters.FilterSet):
    q = django_filters.CharFilter(
        method='search',
        label='Search',
    )
    tag = TagFilter()

    serial = django_filters.CharFilter(lookup_expr="icontains")
    time__gte = django_filters.DateTimeFilter(
        field_name='time',
        lookup_expr='gte'
    )
    time__lte = django_filters.DateTimeFilter(
        field_name='time',
        lookup_expr='lte'
    )
    latest_only = django_filters.BooleanFilter(
        method='_latest_only', label='Only latest inventory')

    device_id = django_filters.ModelMultipleChoiceFilter(
        field_name='device__id',
        queryset=Device.objects.all(),
        to_field_name='id',
        label='Device (ID)',
    )
    device = django_filters.ModelMultipleChoiceFilter(
        field_name='device__name',
        queryset=Device.objects.all(),
        to_field_name='name',
        label='Device (name)',
    )

    class Meta:
        model = Probe
        fields = ('id', 'device_descriptor', 'site_descriptor', 'location_descriptor', 'part', 'name',
                  'serial', 'device', 'site', 'location', 'description', 'category')

    def search(self, queryset, name, value):
        device_descriptor = Q(device_descriptor__icontains=value)
        site_descriptor = Q(site_descriptor__icontains=value)
        location_descriptor = Q(location_descriptor__icontains=value)
        part = Q(part__icontains=value)
        name = Q(name__icontains=value)
        serial = Q(serial__icontains=value)
        description = Q(description__icontains=value)
        return queryset.filter(device_descriptor | part | name | serial | description | site_descriptor | location_descriptor)

    def _latest_only(self, queryset, name, value):
        if value == True:
            latest_inventory_pks = Probe.objects.all().order_by(
                'serial', 'device_id', '-time').distinct('serial', 'device_id').values('pk')
            #latest_inventory_pks = Probe.objects.all().distinct('serial').order_by('serial', '-time').values('pk')
            return queryset.filter(pk__in=latest_inventory_pks)

        else:
            return queryset
