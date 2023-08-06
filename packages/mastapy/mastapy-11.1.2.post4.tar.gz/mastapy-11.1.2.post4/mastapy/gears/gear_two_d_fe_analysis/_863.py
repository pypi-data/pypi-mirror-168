"""_863.py

CylindricalGearSetTIFFAnalysisDutyCycle
"""


from typing import List

from mastapy.gears.gear_two_d_fe_analysis import _865
from mastapy._internal import constructor, conversion
from mastapy.gears.analysis import _1178
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_SET_TIFF_ANALYSIS_DUTY_CYCLE = python_net_import('SMT.MastaAPI.Gears.GearTwoDFEAnalysis', 'CylindricalGearSetTIFFAnalysisDutyCycle')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearSetTIFFAnalysisDutyCycle',)


class CylindricalGearSetTIFFAnalysisDutyCycle(_1178.GearSetDesignAnalysis):
    """CylindricalGearSetTIFFAnalysisDutyCycle

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_GEAR_SET_TIFF_ANALYSIS_DUTY_CYCLE

    def __init__(self, instance_to_wrap: 'CylindricalGearSetTIFFAnalysisDutyCycle.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def gears(self) -> 'List[_865.CylindricalGearTIFFAnalysisDutyCycle]':
        """List[CylindricalGearTIFFAnalysisDutyCycle]: 'Gears' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Gears

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
