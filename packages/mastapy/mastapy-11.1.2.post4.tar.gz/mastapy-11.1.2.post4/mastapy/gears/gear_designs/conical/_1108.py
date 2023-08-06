"""_1108.py

ConicalGearDesign
"""


from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.gears import _305
from mastapy.gears.manufacturing.bevel import _762
from mastapy.gears.gear_designs.cylindrical import _1039
from mastapy.gears.gear_designs import _910
from mastapy._internal.python_net import python_net_import

_CONICAL_GEAR_DESIGN = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Conical', 'ConicalGearDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalGearDesign',)


class ConicalGearDesign(_910.GearDesign):
    """ConicalGearDesign

    This is a mastapy class.
    """

    TYPE = _CONICAL_GEAR_DESIGN

    def __init__(self, instance_to_wrap: 'ConicalGearDesign.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def cutter_edge_radius_concave(self) -> 'float':
        """float: 'CutterEdgeRadiusConcave' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CutterEdgeRadiusConcave

        if temp is None:
            return None

        return temp

    @property
    def cutter_edge_radius_convex(self) -> 'float':
        """float: 'CutterEdgeRadiusConvex' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CutterEdgeRadiusConvex

        if temp is None:
            return None

        return temp

    @property
    def face_angle(self) -> 'float':
        """float: 'FaceAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FaceAngle

        if temp is None:
            return None

        return temp

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
    def inner_root_diameter(self) -> 'float':
        """float: 'InnerRootDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InnerRootDiameter

        if temp is None:
            return None

        return temp

    @property
    def inner_tip_diameter(self) -> 'float':
        """float: 'InnerTipDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InnerTipDiameter

        if temp is None:
            return None

        return temp

    @property
    def outer_root_diameter(self) -> 'float':
        """float: 'OuterRootDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterRootDiameter

        if temp is None:
            return None

        return temp

    @property
    def root_angle(self) -> 'float':
        """float: 'RootAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RootAngle

        if temp is None:
            return None

        return temp

    @property
    def straddle_mounted(self) -> 'bool':
        """bool: 'StraddleMounted' is the original name of this property."""

        temp = self.wrapped.StraddleMounted

        if temp is None:
            return None

        return temp

    @straddle_mounted.setter
    def straddle_mounted(self, value: 'bool'):
        self.wrapped.StraddleMounted = bool(value) if value else False

    @property
    def use_cutter_tilt(self) -> 'bool':
        """bool: 'UseCutterTilt' is the original name of this property."""

        temp = self.wrapped.UseCutterTilt

        if temp is None:
            return None

        return temp

    @use_cutter_tilt.setter
    def use_cutter_tilt(self, value: 'bool'):
        self.wrapped.UseCutterTilt = bool(value) if value else False

    @property
    def flank_measurement_border(self) -> '_762.FlankMeasurementBorder':
        """FlankMeasurementBorder: 'FlankMeasurementBorder' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FlankMeasurementBorder

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def surface_roughness(self) -> '_1039.SurfaceRoughness':
        """SurfaceRoughness: 'SurfaceRoughness' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SurfaceRoughness

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
