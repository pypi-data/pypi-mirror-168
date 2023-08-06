"""_741.py

ConicalGearManufacturingAnalysis
"""


from mastapy.gears.analysis import _1171
from mastapy._internal.python_net import python_net_import

_CONICAL_GEAR_MANUFACTURING_ANALYSIS = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Bevel', 'ConicalGearManufacturingAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalGearManufacturingAnalysis',)


class ConicalGearManufacturingAnalysis(_1171.GearImplementationAnalysis):
    """ConicalGearManufacturingAnalysis

    This is a mastapy class.
    """

    TYPE = _CONICAL_GEAR_MANUFACTURING_ANALYSIS

    def __init__(self, instance_to_wrap: 'ConicalGearManufacturingAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
