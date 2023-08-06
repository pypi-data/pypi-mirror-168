"""_952.py

FaceGearDesign
"""


from mastapy.gears import _305
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy._internal.python_net import python_net_import
from mastapy.gears.gear_designs import _910

_DATABASE_WITH_SELECTED_ITEM = python_net_import('SMT.MastaAPI.UtilityGUI.Databases', 'DatabaseWithSelectedItem')
_FACE_GEAR_DESIGN = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Face', 'FaceGearDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearDesign',)


class FaceGearDesign(_910.GearDesign):
    """FaceGearDesign

    This is a mastapy class.
    """

    TYPE = _FACE_GEAR_DESIGN

    def __init__(self, instance_to_wrap: 'FaceGearDesign.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def hand(self) -> '_305.Hand':
        """Hand: 'Hand' is the original name of this property."""

        temp = self.wrapped.Hand

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_305.Hand)(value) if value is not None else None

    @hand.setter
    def hand(self, value: '_305.Hand'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.Hand = value

    @property
    def iso_material(self) -> 'str':
        """str: 'ISOMaterial' is the original name of this property."""

        temp = self.wrapped.ISOMaterial.SelectedItemName

        if temp is None:
            return None

        return temp

    @iso_material.setter
    def iso_material(self, value: 'str'):
        self.wrapped.ISOMaterial.SetSelectedItem(str(value) if value else '')

    @property
    def mean_point_to_crossing_point(self) -> 'float':
        """float: 'MeanPointToCrossingPoint' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeanPointToCrossingPoint

        if temp is None:
            return None

        return temp

    @property
    def pitch_angle(self) -> 'float':
        """float: 'PitchAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PitchAngle

        if temp is None:
            return None

        return temp

    @property
    def reference_diameter(self) -> 'float':
        """float: 'ReferenceDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ReferenceDiameter

        if temp is None:
            return None

        return temp

    @property
    def working_pitch_diameter(self) -> 'float':
        """float: 'WorkingPitchDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WorkingPitchDiameter

        if temp is None:
            return None

        return temp

    @property
    def working_pitch_radius(self) -> 'float':
        """float: 'WorkingPitchRadius' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WorkingPitchRadius

        if temp is None:
            return None

        return temp
