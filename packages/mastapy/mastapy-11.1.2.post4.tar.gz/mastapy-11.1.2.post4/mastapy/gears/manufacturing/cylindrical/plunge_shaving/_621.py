"""_621.py

ShaverPointCalculationError
"""


from mastapy._internal import constructor
from mastapy.gears.manufacturing.cylindrical.plunge_shaving import _608
from mastapy._internal.python_net import python_net_import

_SHAVER_POINT_CALCULATION_ERROR = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.PlungeShaving', 'ShaverPointCalculationError')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaverPointCalculationError',)


class ShaverPointCalculationError(_608.CalculationError):
    """ShaverPointCalculationError

    This is a mastapy class.
    """

    TYPE = _SHAVER_POINT_CALCULATION_ERROR

    def __init__(self, instance_to_wrap: 'ShaverPointCalculationError.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def achieved_shaver_radius(self) -> 'float':
        """float: 'AchievedShaverRadius' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AchievedShaverRadius

        if temp is None:
            return None

        return temp

    @property
    def achieved_shaver_z_plane(self) -> 'float':
        """float: 'AchievedShaverZPlane' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AchievedShaverZPlane

        if temp is None:
            return None

        return temp

    @property
    def shaver_radius(self) -> 'float':
        """float: 'ShaverRadius' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ShaverRadius

        if temp is None:
            return None

        return temp

    @property
    def shaver_z_plane(self) -> 'float':
        """float: 'ShaverZPlane' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ShaverZPlane

        if temp is None:
            return None

        return temp

    @property
    def total_error(self) -> 'float':
        """float: 'TotalError' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TotalError

        if temp is None:
            return None

        return temp
