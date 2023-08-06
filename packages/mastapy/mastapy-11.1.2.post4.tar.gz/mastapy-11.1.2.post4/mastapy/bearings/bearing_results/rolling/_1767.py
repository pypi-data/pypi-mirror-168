"""_1767.py

LoadedCylindricalRollerBearingResults
"""


from mastapy._internal import constructor
from mastapy.bearings.bearing_results.rolling import _1823, _1782
from mastapy._internal.python_net import python_net_import

_LOADED_CYLINDRICAL_ROLLER_BEARING_RESULTS = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling', 'LoadedCylindricalRollerBearingResults')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadedCylindricalRollerBearingResults',)


class LoadedCylindricalRollerBearingResults(_1782.LoadedNonBarrelRollerBearingResults):
    """LoadedCylindricalRollerBearingResults

    This is a mastapy class.
    """

    TYPE = _LOADED_CYLINDRICAL_ROLLER_BEARING_RESULTS

    def __init__(self, instance_to_wrap: 'LoadedCylindricalRollerBearingResults.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def axial_load_dependent_moment(self) -> 'float':
        """float: 'AxialLoadDependentMoment' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AxialLoadDependentMoment

        if temp is None:
            return None

        return temp

    @property
    def permissible_continuous_axial_load(self) -> '_1823.PermissibleContinuousAxialLoadResults':
        """PermissibleContinuousAxialLoadResults: 'PermissibleContinuousAxialLoad' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PermissibleContinuousAxialLoad

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
