from extras.plugins import PluginConfig


class NetBoxInventoryMonitorConfig(PluginConfig):
    name = 'inventory_monitor'
    verbose_name = ' Inventory Monitor'
    description = 'Manage inventory discovered by SNMP'
    version = '0.4.0'
    base_url = 'inventory-monitor'

config = NetBoxInventoryMonitorConfig
