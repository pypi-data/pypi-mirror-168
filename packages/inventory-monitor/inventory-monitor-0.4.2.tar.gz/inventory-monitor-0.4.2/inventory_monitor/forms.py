from dcim.models import Device, Site, Location
from .models import Probe
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm
from utilities.forms.fields import CommentField, DynamicModelChoiceField
from django import forms
from django.utils.translation import gettext as _
from utilities.forms import DynamicModelMultipleChoiceField, DateTimePicker
from utilities.forms import BOOLEAN_WITH_BLANK_CHOICES, StaticSelect


class ProbeForm(NetBoxModelForm):
    comments = CommentField()

    site = DynamicModelChoiceField(
        queryset=Site.objects.all(),
        required=False
    )
    location = DynamicModelChoiceField(
        queryset=Location.objects.all(),
        required=False
    )

    class Meta:
        model = Probe
        fields = ('name', 'serial', 'time',  'category', 'part', 'device_descriptor', 'device',
                  'site_descriptor', 'site', 'location_descriptor', 'location', 'description', 'tags', 'comments',)


class ProbeFilterForm(NetBoxModelFilterSetForm):
    model = Probe

    device_id = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        required=False,
        label=_('Device')
    )
    serial = forms.CharField(
        required=False
    )
    device_descriptor = forms.CharField(
        required=False
    )
    category = forms.CharField(
        required=False
    )
    description = forms.CharField(
        required=False
    )
    time__gte = forms.DateTimeField(
        required=False,
        label=('Time From'),
        widget=DateTimePicker()
    )
    time__lte = forms.DateTimeField(
        required=False,
        label=('Time Till'),
        widget=DateTimePicker()
    )
    latest_only = forms.NullBooleanField(
        required=False,
        label='Latest inventory only',
        widget=StaticSelect(
            choices=BOOLEAN_WITH_BLANK_CHOICES
        )
    )
