"""_1859.py

Viscosities
"""


from mastapy._internal import constructor
from mastapy.bearings.bearing_results.rolling.skf_module import _1851, _1855
from mastapy._internal.python_net import python_net_import

_VISCOSITIES = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling.SkfModule', 'Viscosities')


__docformat__ = 'restructuredtext en'
__all__ = ('Viscosities',)


class Viscosities(_1855.SKFCalculationResult):
    """Viscosities

    This is a mastapy class.
    """

    TYPE = _VISCOSITIES

    def __init__(self, instance_to_wrap: 'Viscosities.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def viscosity_ratio(self) -> 'float':
        """float: 'ViscosityRatio' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ViscosityRatio

        if temp is None:
            return None

        return temp

    @property
    def operating_viscosity(self) -> '_1851.OperatingViscosity':
        """OperatingViscosity: 'OperatingViscosity' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OperatingViscosity

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
