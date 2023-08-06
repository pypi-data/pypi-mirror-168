"""_833.py

ConicalGearLoadDistributionAnalysis
"""


from mastapy.gears.ltca import _806
from mastapy._internal.python_net import python_net_import

_CONICAL_GEAR_LOAD_DISTRIBUTION_ANALYSIS = python_net_import('SMT.MastaAPI.Gears.LTCA.Conical', 'ConicalGearLoadDistributionAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalGearLoadDistributionAnalysis',)


class ConicalGearLoadDistributionAnalysis(_806.GearLoadDistributionAnalysis):
    """ConicalGearLoadDistributionAnalysis

    This is a mastapy class.
    """

    TYPE = _CONICAL_GEAR_LOAD_DISTRIBUTION_ANALYSIS

    def __init__(self, instance_to_wrap: 'ConicalGearLoadDistributionAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
