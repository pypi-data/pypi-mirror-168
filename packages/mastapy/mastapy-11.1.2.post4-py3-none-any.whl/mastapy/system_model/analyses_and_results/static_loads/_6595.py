"""_6595.py

ElectricMachineDetailDatabase
"""


from mastapy.utility.databases import _1604
from mastapy.system_model.analyses_and_results.static_loads import _6594
from mastapy._internal.python_net import python_net_import

_ELECTRIC_MACHINE_DETAIL_DATABASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'ElectricMachineDetailDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('ElectricMachineDetailDatabase',)


class ElectricMachineDetailDatabase(_1604.NamedDatabase['_6594.ElectricMachineDetail']):
    """ElectricMachineDetailDatabase

    This is a mastapy class.
    """

    TYPE = _ELECTRIC_MACHINE_DETAIL_DATABASE

    def __init__(self, instance_to_wrap: 'ElectricMachineDetailDatabase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
