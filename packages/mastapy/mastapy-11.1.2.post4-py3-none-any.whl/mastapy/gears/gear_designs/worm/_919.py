"""_919.py

WormDesign
"""


from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.gears import _322
from mastapy.gears.gear_designs.worm import _920
from mastapy._internal.python_net import python_net_import

_WORM_DESIGN = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Worm', 'WormDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('WormDesign',)


class WormDesign(_920.WormGearDesign):
    """WormDesign

    This is a mastapy class.
    """

    TYPE = _WORM_DESIGN

    def __init__(self, instance_to_wrap: 'WormDesign.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def addendum(self) -> 'float':
        """float: 'Addendum' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Addendum

        if temp is None:
            return None

        return temp

    @property
    def addendum_factor(self) -> '_322.WormAddendumFactor':
        """WormAddendumFactor: 'AddendumFactor' is the original name of this property."""

        temp = self.wrapped.AddendumFactor

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_322.WormAddendumFactor)(value) if value is not None else None

    @addendum_factor.setter
    def addendum_factor(self, value: '_322.WormAddendumFactor'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.AddendumFactor = value

    @property
    def axial_pitch(self) -> 'float':
        """float: 'AxialPitch' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AxialPitch

        if temp is None:
            return None

        return temp

    @property
    def axial_thickness(self) -> 'float':
        """float: 'AxialThickness' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AxialThickness

        if temp is None:
            return None

        return temp

    @property
    def clearance(self) -> 'float':
        """float: 'Clearance' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Clearance

        if temp is None:
            return None

        return temp

    @property
    def clearance_factor(self) -> 'float':
        """float: 'ClearanceFactor' is the original name of this property."""

        temp = self.wrapped.ClearanceFactor

        if temp is None:
            return None

        return temp

    @clearance_factor.setter
    def clearance_factor(self, value: 'float'):
        self.wrapped.ClearanceFactor = float(value) if value else 0.0

    @property
    def dedendum(self) -> 'float':
        """float: 'Dedendum' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Dedendum

        if temp is None:
            return None

        return temp

    @property
    def diameter_factor(self) -> 'float':
        """float: 'DiameterFactor' is the original name of this property."""

        temp = self.wrapped.DiameterFactor

        if temp is None:
            return None

        return temp

    @diameter_factor.setter
    def diameter_factor(self, value: 'float'):
        self.wrapped.DiameterFactor = float(value) if value else 0.0

    @property
    def face_width(self) -> 'float':
        """float: 'FaceWidth' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FaceWidth

        if temp is None:
            return None

        return temp

    @property
    def fillet_radius(self) -> 'float':
        """float: 'FilletRadius' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FilletRadius

        if temp is None:
            return None

        return temp

    @property
    def fillet_radius_factor(self) -> 'float':
        """float: 'FilletRadiusFactor' is the original name of this property."""

        temp = self.wrapped.FilletRadiusFactor

        if temp is None:
            return None

        return temp

    @fillet_radius_factor.setter
    def fillet_radius_factor(self, value: 'float'):
        self.wrapped.FilletRadiusFactor = float(value) if value else 0.0

    @property
    def lead(self) -> 'float':
        """float: 'Lead' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Lead

        if temp is None:
            return None

        return temp

    @property
    def normal_thickness(self) -> 'float':
        """float: 'NormalThickness' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NormalThickness

        if temp is None:
            return None

        return temp

    @property
    def reference_diameter(self) -> 'float':
        """float: 'ReferenceDiameter' is the original name of this property."""

        temp = self.wrapped.ReferenceDiameter

        if temp is None:
            return None

        return temp

    @reference_diameter.setter
    def reference_diameter(self, value: 'float'):
        self.wrapped.ReferenceDiameter = float(value) if value else 0.0

    @property
    def reference_lead_angle(self) -> 'float':
        """float: 'ReferenceLeadAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ReferenceLeadAngle

        if temp is None:
            return None

        return temp

    @property
    def tip_diameter(self) -> 'float':
        """float: 'TipDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TipDiameter

        if temp is None:
            return None

        return temp

    @property
    def working_depth_factor(self) -> 'float':
        """float: 'WorkingDepthFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WorkingDepthFactor

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
    def working_pitch_lead_angle(self) -> 'float':
        """float: 'WorkingPitchLeadAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WorkingPitchLeadAngle

        if temp is None:
            return None

        return temp

    @property
    def worm_starts(self) -> 'int':
        """int: 'WormStarts' is the original name of this property."""

        temp = self.wrapped.WormStarts

        if temp is None:
            return None

        return temp

    @worm_starts.setter
    def worm_starts(self, value: 'int'):
        self.wrapped.WormStarts = int(value) if value else 0
