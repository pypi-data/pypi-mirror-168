from graphene import ObjectType
from netbox.graphql.types import NetBoxObjectType
from netbox.graphql.fields import ObjectField, ObjectListField
from . import filtersets, models

class ProbeType(NetBoxObjectType):

    class Meta:
        model = models.Probe
        fields = '__all__'
        filterset_class = filtersets.ProbeFilterSet

class Query(ObjectType):
    probe = ObjectField(ProbeType)
    probe_list = ObjectListField(ProbeType)

schema = Query