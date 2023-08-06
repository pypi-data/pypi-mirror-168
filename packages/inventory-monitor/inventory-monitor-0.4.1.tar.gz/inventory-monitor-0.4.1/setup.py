from setuptools import find_packages, setup

setup(
    name = 'inventory-monitor',
    version='0.4.1',
    description = 'Manage inventory discovered by SNMP',
    install_requires=[],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
