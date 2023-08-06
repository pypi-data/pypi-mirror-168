"""_678.py

CylindricalGearRackDesign
"""


from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.gears import _305, _323
from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.gears.manufacturing.cylindrical.cutters.tangibles import _696, _691, _694
from mastapy._internal.cast_exception import CastException
from mastapy.gears.manufacturing.cylindrical.cutters import _679
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_RACK_DESIGN = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.Cutters', 'CylindricalGearRackDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearRackDesign',)


class CylindricalGearRackDesign(_679.CylindricalGearRealCutterDesign):
    """CylindricalGearRackDesign

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_GEAR_RACK_DESIGN

    def __init__(self, instance_to_wrap: 'CylindricalGearRackDesign.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def addendum(self) -> 'float':
        """float: 'Addendum' is the original name of this property."""

        temp = self.wrapped.Addendum

        if temp is None:
            return None

        return temp

    @addendum.setter
    def addendum(self, value: 'float'):
        self.wrapped.Addendum = float(value) if value else 0.0

    @property
    def addendum_factor(self) -> 'float':
        """float: 'AddendumFactor' is the original name of this property."""

        temp = self.wrapped.AddendumFactor

        if temp is None:
            return None

        return temp

    @addendum_factor.setter
    def addendum_factor(self, value: 'float'):
        self.wrapped.AddendumFactor = float(value) if value else 0.0

    @property
    def addendum_keeping_dedendum_constant(self) -> 'float':
        """float: 'AddendumKeepingDedendumConstant' is the original name of this property."""

        temp = self.wrapped.AddendumKeepingDedendumConstant

        if temp is None:
            return None

        return temp

    @addendum_keeping_dedendum_constant.setter
    def addendum_keeping_dedendum_constant(self, value: 'float'):
        self.wrapped.AddendumKeepingDedendumConstant = float(value) if value else 0.0

    @property
    def dedendum(self) -> 'float':
        """float: 'Dedendum' is the original name of this property."""

        temp = self.wrapped.Dedendum

        if temp is None:
            return None

        return temp

    @dedendum.setter
    def dedendum(self, value: 'float'):
        self.wrapped.Dedendum = float(value) if value else 0.0

    @property
    def dedendum_factor(self) -> 'float':
        """float: 'DedendumFactor' is the original name of this property."""

        temp = self.wrapped.DedendumFactor

        if temp is None:
            return None

        return temp

    @dedendum_factor.setter
    def dedendum_factor(self, value: 'float'):
        self.wrapped.DedendumFactor = float(value) if value else 0.0

    @property
    def edge_height(self) -> 'float':
        """float: 'EdgeHeight' is the original name of this property."""

        temp = self.wrapped.EdgeHeight

        if temp is None:
            return None

        return temp

    @edge_height.setter
    def edge_height(self, value: 'float'):
        self.wrapped.EdgeHeight = float(value) if value else 0.0

    @property
    def edge_radius(self) -> 'float':
        """float: 'EdgeRadius' is the original name of this property."""

        temp = self.wrapped.EdgeRadius

        if temp is None:
            return None

        return temp

    @edge_radius.setter
    def edge_radius(self, value: 'float'):
        self.wrapped.EdgeRadius = float(value) if value else 0.0

    @property
    def effective_length(self) -> 'float':
        """float: 'EffectiveLength' is the original name of this property."""

        temp = self.wrapped.EffectiveLength

        if temp is None:
            return None

        return temp

    @effective_length.setter
    def effective_length(self, value: 'float'):
        self.wrapped.EffectiveLength = float(value) if value else 0.0

    @property
    def flat_root_width(self) -> 'float':
        """float: 'FlatRootWidth' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FlatRootWidth

        if temp is None:
            return None

        return temp

    @property
    def flat_tip_width(self) -> 'float':
        """float: 'FlatTipWidth' is the original name of this property."""

        temp = self.wrapped.FlatTipWidth

        if temp is None:
            return None

        return temp

    @flat_tip_width.setter
    def flat_tip_width(self, value: 'float'):
        self.wrapped.FlatTipWidth = float(value) if value else 0.0

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
    def normal_thickness(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'NormalThickness' is the original name of this property."""

        temp = self.wrapped.NormalThickness

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @normal_thickness.setter
    def normal_thickness(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.NormalThickness = value

    @property
    def number_of_threads(self) -> 'int':
        """int: 'NumberOfThreads' is the original name of this property."""

        temp = self.wrapped.NumberOfThreads

        if temp is None:
            return None

        return temp

    @number_of_threads.setter
    def number_of_threads(self, value: 'int'):
        self.wrapped.NumberOfThreads = int(value) if value else 0

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
    def tip_diameter(self) -> 'float':
        """float: 'TipDiameter' is the original name of this property."""

        temp = self.wrapped.TipDiameter

        if temp is None:
            return None

        return temp

    @tip_diameter.setter
    def tip_diameter(self, value: 'float'):
        self.wrapped.TipDiameter = float(value) if value else 0.0

    @property
    def use_maximum_edge_radius(self) -> 'bool':
        """bool: 'UseMaximumEdgeRadius' is the original name of this property."""

        temp = self.wrapped.UseMaximumEdgeRadius

        if temp is None:
            return None

        return temp

    @use_maximum_edge_radius.setter
    def use_maximum_edge_radius(self, value: 'bool'):
        self.wrapped.UseMaximumEdgeRadius = bool(value) if value else False

    @property
    def whole_depth(self) -> 'float':
        """float: 'WholeDepth' is the original name of this property."""

        temp = self.wrapped.WholeDepth

        if temp is None:
            return None

        return temp

    @whole_depth.setter
    def whole_depth(self, value: 'float'):
        self.wrapped.WholeDepth = float(value) if value else 0.0

    @property
    def worm_type(self) -> '_323.WormType':
        """WormType: 'WormType' is the original name of this property."""

        temp = self.wrapped.WormType

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_323.WormType)(value) if value is not None else None

    @worm_type.setter
    def worm_type(self, value: '_323.WormType'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.WormType = value

    @property
    def nominal_rack_shape(self) -> '_696.RackShape':
        """RackShape: 'NominalRackShape' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NominalRackShape

        if temp is None:
            return None

        if _696.RackShape.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast nominal_rack_shape to RackShape. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def nominal_rack_shape_of_type_cylindrical_gear_hob_shape(self) -> '_691.CylindricalGearHobShape':
        """CylindricalGearHobShape: 'NominalRackShape' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NominalRackShape

        if temp is None:
            return None

        if _691.CylindricalGearHobShape.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast nominal_rack_shape to CylindricalGearHobShape. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def nominal_rack_shape_of_type_cylindrical_gear_worm_grinder_shape(self) -> '_694.CylindricalGearWormGrinderShape':
        """CylindricalGearWormGrinderShape: 'NominalRackShape' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NominalRackShape

        if temp is None:
            return None

        if _694.CylindricalGearWormGrinderShape.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast nominal_rack_shape to CylindricalGearWormGrinderShape. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    def convert_to_standard_thickness(self):
        """ 'ConvertToStandardThickness' is the original name of this method."""

        self.wrapped.ConvertToStandardThickness()
