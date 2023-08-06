"""_1627.py

CustomTableAndChart
"""


from mastapy.math_utility import _1295
from mastapy._internal import constructor
from mastapy.math_utility.measured_ranges import _1372
from mastapy._internal.cast_exception import CastException
from mastapy.utility.report import _1559
from mastapy._internal.python_net import python_net_import

_CUSTOM_TABLE_AND_CHART = python_net_import('SMT.MastaAPI.UtilityGUI.Charts', 'CustomTableAndChart')


__docformat__ = 'restructuredtext en'
__all__ = ('CustomTableAndChart',)


class CustomTableAndChart(_1559.CustomTable):
    """CustomTableAndChart

    This is a mastapy class.
    """

    TYPE = _CUSTOM_TABLE_AND_CHART

    def __init__(self, instance_to_wrap: 'CustomTableAndChart.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def primary_axis_range(self) -> '_1295.Range':
        """Range: 'PrimaryAxisRange' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PrimaryAxisRange

        if temp is None:
            return None

        if _1295.Range.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast primary_axis_range to Range. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
