from netbox.views import generic
from . import filtersets, forms, models, tables
from django.db.models import OuterRef, Subquery, Count


class ProbeView(generic.ObjectView):
    queryset = models.Probe.objects.all()

    def get_extra_context(self, request, instance):
        sub_count_serial = models.Probe.objects.filter(serial=OuterRef('serial')).values(
            'serial').annotate(changes_count=Count('*'))
        table = tables.ProbeTable(models.Probe.objects.filter(serial=instance.serial).annotate(
            changes_count=Subquery(sub_count_serial.values("changes_count"))))

        table.configure(request)

        return {'probe_table': table}


class ProbeListView(generic.ObjectListView):
    sub_count_serial = models.Probe.objects.filter(serial=OuterRef('serial')).values(
        'serial').annotate(changes_count=Count('*'))
    queryset = models.Probe.objects.prefetch_related('tags', 'device').annotate(
        changes_count=Subquery(sub_count_serial.values("changes_count")))

    table = tables.ProbeTable
    filterset = filtersets.ProbeFilterSet
    filterset_form = forms.ProbeFilterForm


class ProbeEditView(generic.ObjectEditView):
    queryset = models.Probe.objects.all()
    form = forms.ProbeForm


class ProbeDeleteView(generic.ObjectDeleteView):
    queryset = models.Probe.objects.all()


class ProbeBulkDeleteView(generic.BulkDeleteView):
    queryset = models.Probe.objects.all()
    filterset = filtersets.ProbeFilterSet
    table = tables.ProbeTable
