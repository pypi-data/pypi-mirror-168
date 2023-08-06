"""_772.py

PinionFinishMachineSettings
"""


from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.gears.gear_designs.conical import _1125
from mastapy.gears import _292
from mastapy._internal.python_net import python_net_import

_PINION_FINISH_MACHINE_SETTINGS = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Bevel', 'PinionFinishMachineSettings')


__docformat__ = 'restructuredtext en'
__all__ = ('PinionFinishMachineSettings',)


class PinionFinishMachineSettings(_292.ConicalGearToothSurface):
    """PinionFinishMachineSettings

    This is a mastapy class.
    """

    TYPE = _PINION_FINISH_MACHINE_SETTINGS

    def __init__(self, instance_to_wrap: 'PinionFinishMachineSettings.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def blade_edge_radius(self) -> 'float':
        """float: 'BladeEdgeRadius' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BladeEdgeRadius

        if temp is None:
            return None

        return temp

    @property
    def cc_angle(self) -> 'float':
        """float: 'CCAngle' is the original name of this property."""

        temp = self.wrapped.CCAngle

        if temp is None:
            return None

        return temp

    @cc_angle.setter
    def cc_angle(self, value: 'float'):
        self.wrapped.CCAngle = float(value) if value else 0.0

    @property
    def cutter_radius(self) -> 'float':
        """float: 'CutterRadius' is the original name of this property."""

        temp = self.wrapped.CutterRadius

        if temp is None:
            return None

        return temp

    @cutter_radius.setter
    def cutter_radius(self, value: 'float'):
        self.wrapped.CutterRadius = float(value) if value else 0.0

    @property
    def ease_off_at_heel_root(self) -> 'float':
        """float: 'EaseOffAtHeelRoot' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.EaseOffAtHeelRoot

        if temp is None:
            return None

        return temp

    @property
    def ease_off_at_heel_tip(self) -> 'float':
        """float: 'EaseOffAtHeelTip' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.EaseOffAtHeelTip

        if temp is None:
            return None

        return temp

    @property
    def ease_off_at_toe_root(self) -> 'float':
        """float: 'EaseOffAtToeRoot' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.EaseOffAtToeRoot

        if temp is None:
            return None

        return temp

    @property
    def ease_off_at_toe_tip(self) -> 'float':
        """float: 'EaseOffAtToeTip' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.EaseOffAtToeTip

        if temp is None:
            return None

        return temp

    @property
    def pinion_cutter_blade_angle(self) -> 'float':
        """float: 'PinionCutterBladeAngle' is the original name of this property."""

        temp = self.wrapped.PinionCutterBladeAngle

        if temp is None:
            return None

        return temp

    @pinion_cutter_blade_angle.setter
    def pinion_cutter_blade_angle(self, value: 'float'):
        self.wrapped.PinionCutterBladeAngle = float(value) if value else 0.0

    @property
    def toprem_angle(self) -> 'float':
        """float: 'TopremAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TopremAngle

        if temp is None:
            return None

        return temp

    @property
    def toprem_length(self) -> 'float':
        """float: 'TopremLength' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TopremLength

        if temp is None:
            return None

        return temp

    @property
    def toprem_letter(self) -> '_1125.TopremLetter':
        """TopremLetter: 'TopremLetter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TopremLetter

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1125.TopremLetter)(value) if value is not None else None
