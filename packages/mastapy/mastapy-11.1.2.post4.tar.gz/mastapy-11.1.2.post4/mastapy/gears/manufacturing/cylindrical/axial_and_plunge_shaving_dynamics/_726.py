"""_726.py

PlungeShavingDynamicsViewModel
"""


from mastapy._internal import constructor
from mastapy.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics import _722, _736, _721
from mastapy._internal.python_net import python_net_import

_PLUNGE_SHAVING_DYNAMICS_VIEW_MODEL = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.AxialAndPlungeShavingDynamics', 'PlungeShavingDynamicsViewModel')


__docformat__ = 'restructuredtext en'
__all__ = ('PlungeShavingDynamicsViewModel',)


class PlungeShavingDynamicsViewModel(_736.ShavingDynamicsViewModel['_721.PlungeShaverDynamics']):
    """PlungeShavingDynamicsViewModel

    This is a mastapy class.
    """

    TYPE = _PLUNGE_SHAVING_DYNAMICS_VIEW_MODEL

    def __init__(self, instance_to_wrap: 'PlungeShavingDynamicsViewModel.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def transverse_plane_on_gear_for_analysis(self) -> 'float':
        """float: 'TransversePlaneOnGearForAnalysis' is the original name of this property."""

        temp = self.wrapped.TransversePlaneOnGearForAnalysis

        if temp is None:
            return None

        return temp

    @transverse_plane_on_gear_for_analysis.setter
    def transverse_plane_on_gear_for_analysis(self, value: 'float'):
        self.wrapped.TransversePlaneOnGearForAnalysis = float(value) if value else 0.0

    @property
    def settings(self) -> '_722.PlungeShaverDynamicSettings':
        """PlungeShaverDynamicSettings: 'Settings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Settings

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
