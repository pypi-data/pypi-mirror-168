"""_740.py

ConicalFlankDeviationsData
"""


from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_CONICAL_FLANK_DEVIATIONS_DATA = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Bevel', 'ConicalFlankDeviationsData')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalFlankDeviationsData',)


class ConicalFlankDeviationsData(_0.APIBase):
    """ConicalFlankDeviationsData

    This is a mastapy class.
    """

    TYPE = _CONICAL_FLANK_DEVIATIONS_DATA

    def __init__(self, instance_to_wrap: 'ConicalFlankDeviationsData.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def average_crowning_deviation(self) -> 'float':
        """float: 'AverageCrowningDeviation' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AverageCrowningDeviation

        if temp is None:
            return None

        return temp

    @property
    def average_pressure_angle_deviation(self) -> 'float':
        """float: 'AveragePressureAngleDeviation' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AveragePressureAngleDeviation

        if temp is None:
            return None

        return temp

    @property
    def average_profile_curvature_deviation(self) -> 'float':
        """float: 'AverageProfileCurvatureDeviation' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AverageProfileCurvatureDeviation

        if temp is None:
            return None

        return temp

    @property
    def average_spiral_angle_deviation(self) -> 'float':
        """float: 'AverageSpiralAngleDeviation' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AverageSpiralAngleDeviation

        if temp is None:
            return None

        return temp

    @property
    def bias_deviation(self) -> 'float':
        """float: 'BiasDeviation' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BiasDeviation

        if temp is None:
            return None

        return temp
