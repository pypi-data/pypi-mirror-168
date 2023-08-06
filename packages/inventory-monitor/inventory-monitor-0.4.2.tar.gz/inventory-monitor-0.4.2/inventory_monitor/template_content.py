from extras.plugins import PluginTemplateExtension
from .models import Probe
from django.db.models import OuterRef, Subquery, Count

#from django.conf import settings
#plugin_settings = settings.PLUGINS_CONFIG.get('inventory_monitor', {})

from django.db.models import CharField, Value
from django.db.models.functions import Concat

class DeviceDocumentList(PluginTemplateExtension):
    model = 'dcim.device'

    def right_page(self):
        obj = self.context['object']
        latest_inventory_pks = Probe.objects.all()\
            .distinct('serial')\
            .order_by('serial', '-time')\
            .values('pk')

        latest_inventory_pks = Probe.objects.all().order_by('serial', 'device_id', '-time').distinct('serial', 'device_id').values('pk')

        sub_count_serial = Probe.objects.filter(serial=OuterRef('serial'))\
            .values('serial')\
            .annotate(changes_count=Count('*'))

        device_probes = Probe.objects.filter(device=obj, pk__in=latest_inventory_pks)\
            .prefetch_related('tags', 'device')\
            .annotate(changes_count=Subquery(sub_count_serial.values("changes_count")))

        return self.render(
            'inventory_monitor/device_probes_include.html',
            extra_context={
                'device_probes': device_probes.order_by('-time')[:10],
                'total_device_probes_count': device_probes.count(),
            }
        )


template_extensions = [DeviceDocumentList]
