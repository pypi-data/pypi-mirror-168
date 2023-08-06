"""_1200.py

DIN5480SplineHalfDesign
"""


from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.detailed_rigid_connectors.splines import _1219, _1210, _1227
from mastapy._internal.python_net import python_net_import

_DIN5480_SPLINE_HALF_DESIGN = python_net_import('SMT.MastaAPI.DetailedRigidConnectors.Splines', 'DIN5480SplineHalfDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('DIN5480SplineHalfDesign',)


class DIN5480SplineHalfDesign(_1227.StandardSplineHalfDesign):
    """DIN5480SplineHalfDesign

    This is a mastapy class.
    """

    TYPE = _DIN5480_SPLINE_HALF_DESIGN

    def __init__(self, instance_to_wrap: 'DIN5480SplineHalfDesign.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def addendum_modification(self) -> 'float':
        """float: 'AddendumModification' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AddendumModification

        if temp is None:
            return None

        return temp

    @property
    def addendum_of_basic_rack(self) -> 'float':
        """float: 'AddendumOfBasicRack' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AddendumOfBasicRack

        if temp is None:
            return None

        return temp

    @property
    def base_form_circle_diameter_limit(self) -> 'float':
        """float: 'BaseFormCircleDiameterLimit' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BaseFormCircleDiameterLimit

        if temp is None:
            return None

        return temp

    @property
    def basic_rack_addendum_factor(self) -> 'float':
        """float: 'BasicRackAddendumFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BasicRackAddendumFactor

        if temp is None:
            return None

        return temp

    @property
    def basic_rack_dedendum_factor(self) -> 'float':
        """float: 'BasicRackDedendumFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BasicRackDedendumFactor

        if temp is None:
            return None

        return temp

    @property
    def bottom_clearance_of_basic_rack(self) -> 'float':
        """float: 'BottomClearanceOfBasicRack' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BottomClearanceOfBasicRack

        if temp is None:
            return None

        return temp

    @property
    def dedendum_of_basic_rack(self) -> 'float':
        """float: 'DedendumOfBasicRack' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DedendumOfBasicRack

        if temp is None:
            return None

        return temp

    @property
    def finishing_method(self) -> '_1219.FinishingMethods':
        """FinishingMethods: 'FinishingMethod' is the original name of this property."""

        temp = self.wrapped.FinishingMethod

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1219.FinishingMethods)(value) if value is not None else None

    @finishing_method.setter
    def finishing_method(self, value: '_1219.FinishingMethods'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.FinishingMethod = value

    @property
    def form_clearance_of_basic_rack(self) -> 'float':
        """float: 'FormClearanceOfBasicRack' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FormClearanceOfBasicRack

        if temp is None:
            return None

        return temp

    @property
    def manufacturing_type(self) -> '_1210.ManufacturingTypes':
        """ManufacturingTypes: 'ManufacturingType' is the original name of this property."""

        temp = self.wrapped.ManufacturingType

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1210.ManufacturingTypes)(value) if value is not None else None

    @manufacturing_type.setter
    def manufacturing_type(self, value: '_1210.ManufacturingTypes'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.ManufacturingType = value

    @property
    def maximum_actual_space_width(self) -> 'float':
        """float: 'MaximumActualSpaceWidth' is the original name of this property."""

        temp = self.wrapped.MaximumActualSpaceWidth

        if temp is None:
            return None

        return temp

    @maximum_actual_space_width.setter
    def maximum_actual_space_width(self, value: 'float'):
        self.wrapped.MaximumActualSpaceWidth = float(value) if value else 0.0

    @property
    def maximum_actual_tooth_thickness(self) -> 'float':
        """float: 'MaximumActualToothThickness' is the original name of this property."""

        temp = self.wrapped.MaximumActualToothThickness

        if temp is None:
            return None

        return temp

    @maximum_actual_tooth_thickness.setter
    def maximum_actual_tooth_thickness(self, value: 'float'):
        self.wrapped.MaximumActualToothThickness = float(value) if value else 0.0

    @property
    def maximum_effective_root_diameter(self) -> 'float':
        """float: 'MaximumEffectiveRootDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumEffectiveRootDiameter

        if temp is None:
            return None

        return temp

    @property
    def maximum_effective_tooth_thickness(self) -> 'float':
        """float: 'MaximumEffectiveToothThickness' is the original name of this property."""

        temp = self.wrapped.MaximumEffectiveToothThickness

        if temp is None:
            return None

        return temp

    @maximum_effective_tooth_thickness.setter
    def maximum_effective_tooth_thickness(self, value: 'float'):
        self.wrapped.MaximumEffectiveToothThickness = float(value) if value else 0.0

    @property
    def minimum_actual_space_width(self) -> 'float':
        """float: 'MinimumActualSpaceWidth' is the original name of this property."""

        temp = self.wrapped.MinimumActualSpaceWidth

        if temp is None:
            return None

        return temp

    @minimum_actual_space_width.setter
    def minimum_actual_space_width(self, value: 'float'):
        self.wrapped.MinimumActualSpaceWidth = float(value) if value else 0.0

    @property
    def minimum_actual_tooth_thickness(self) -> 'float':
        """float: 'MinimumActualToothThickness' is the original name of this property."""

        temp = self.wrapped.MinimumActualToothThickness

        if temp is None:
            return None

        return temp

    @minimum_actual_tooth_thickness.setter
    def minimum_actual_tooth_thickness(self, value: 'float'):
        self.wrapped.MinimumActualToothThickness = float(value) if value else 0.0

    @property
    def minimum_effective_root_diameter(self) -> 'float':
        """float: 'MinimumEffectiveRootDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinimumEffectiveRootDiameter

        if temp is None:
            return None

        return temp

    @property
    def minimum_effective_space_width(self) -> 'float':
        """float: 'MinimumEffectiveSpaceWidth' is the original name of this property."""

        temp = self.wrapped.MinimumEffectiveSpaceWidth

        if temp is None:
            return None

        return temp

    @minimum_effective_space_width.setter
    def minimum_effective_space_width(self, value: 'float'):
        self.wrapped.MinimumEffectiveSpaceWidth = float(value) if value else 0.0

    @property
    def root_diameter(self) -> 'float':
        """float: 'RootDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RootDiameter

        if temp is None:
            return None

        return temp

    @property
    def root_fillet_radius_factor(self) -> 'float':
        """float: 'RootFilletRadiusFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RootFilletRadiusFactor

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
    def tooth_height_of_basic_rack(self) -> 'float':
        """float: 'ToothHeightOfBasicRack' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ToothHeightOfBasicRack

        if temp is None:
            return None

        return temp
