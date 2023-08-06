"""_497.py

ToothFlankFractureAnalysisRowN1457
"""


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.gears.rating.cylindrical.iso6336 import _496, _494
from mastapy._internal.python_net import python_net_import

_TOOTH_FLANK_FRACTURE_ANALYSIS_ROW_N1457 = python_net_import('SMT.MastaAPI.Gears.Rating.Cylindrical.ISO6336', 'ToothFlankFractureAnalysisRowN1457')


__docformat__ = 'restructuredtext en'
__all__ = ('ToothFlankFractureAnalysisRowN1457',)


class ToothFlankFractureAnalysisRowN1457(_494.ToothFlankFractureAnalysisContactPointN1457):
    """ToothFlankFractureAnalysisRowN1457

    This is a mastapy class.
    """

    TYPE = _TOOTH_FLANK_FRACTURE_ANALYSIS_ROW_N1457

    def __init__(self, instance_to_wrap: 'ToothFlankFractureAnalysisRowN1457.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def maximum_fatigue_damage(self) -> 'float':
        """float: 'MaximumFatigueDamage' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumFatigueDamage

        if temp is None:
            return None

        return temp

    @property
    def analysis_point_with_maximum_fatigue_damage(self) -> '_496.ToothFlankFractureAnalysisPointN1457':
        """ToothFlankFractureAnalysisPointN1457: 'AnalysisPointWithMaximumFatigueDamage' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AnalysisPointWithMaximumFatigueDamage

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def watch_points(self) -> 'List[_496.ToothFlankFractureAnalysisPointN1457]':
        """List[ToothFlankFractureAnalysisPointN1457]: 'WatchPoints' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WatchPoints

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
