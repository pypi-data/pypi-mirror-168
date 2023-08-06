"""overridable.py

Implementations of 'Overridable' in Python.
As Python does not have an implicit operator, this is the next
best solution for implementing these types properly.
"""


from enum import Enum
from typing import Generic, TypeVar

from mastapy._internal import (
    mixins, constructor, enum_with_selected_value_runtime, conversion
)
from mastapy._internal.python_net import python_net_import
from mastapy.materials import _227
from mastapy.gears import (
    _306, _291, _294, _309
)
from mastapy.bearings.bearing_designs.rolling import _1908, _1914, _1931
from mastapy.bearings import _1663
from mastapy.nodal_analysis.dev_tools_analyses import _181
from mastapy.nodal_analysis.fe_export_utility import _157
from mastapy.system_model.fe import _2152
from mastapy.materials.efficiency import _266, _268
from mastapy.bearings.bearing_results import _1706
from mastapy.system_model.part_model import _2228
from mastapy.bearings.bearing_results.rolling import _1734, _1828
from mastapy.gears.rating.cylindrical.iso6336 import _477
from mastapy.system_model.analyses_and_results.static_loads import _6649

_OVERRIDABLE = python_net_import('SMT.MastaAPI.Utility.Property', 'Overridable')


__docformat__ = 'restructuredtext en'
__all__ = (
    'Overridable_float', 'Overridable_int',
    'Overridable_CylindricalGearRatingMethods', 'Overridable_ISOToleranceStandard',
    'Overridable_CoefficientOfFrictionCalculationMethod', 'Overridable_T',
    'Overridable_bool', 'Overridable_DiameterSeries',
    'Overridable_HeightSeries', 'Overridable_WidthSeries',
    'Overridable_SealLocation', 'Overridable_RigidCouplingType',
    'Overridable_BoundaryConditionType', 'Overridable_NodeSelectionDepthOption',
    'Overridable_BearingEfficiencyRatingMethod', 'Overridable_CylindricalRollerMaxAxialLoadMethod',
    'Overridable_ContactRatioRequirements', 'Overridable_MicroGeometryModel',
    'Overridable_UnbalancedMassInclusionOption', 'Overridable_FrictionModelForGyroscopicMoment',
    'Overridable_RollerAnalysisMethod', 'Overridable_HelicalGearMicroGeometryOption',
    'Overridable_EfficiencyRatingMethod', 'Overridable_MeshStiffnessSource'
)


T = TypeVar('T')


class Overridable_float(float, mixins.OverridableMixin):
    """Overridable_float

    A specific implementation of 'Overridable' for 'float' types.
    """
    __qualname__ = 'float'

    def __new__(cls, instance_to_wrap: 'Overridable_float.TYPE'):
        return float.__new__(cls, instance_to_wrap.Value if instance_to_wrap.Value is not None else 0.0)

    def __init__(self, instance_to_wrap: 'Overridable_float.TYPE'):
        try:
            self.enclosing = instance_to_wrap
            self.wrapped = instance_to_wrap.Value
        except (TypeError, AttributeError):
            pass

    @classmethod
    def wrapper_type(cls) -> '_OVERRIDABLE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _OVERRIDABLE

    @classmethod
    def implicit_type(cls) -> 'float':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return float

    @property
    def value(self) -> 'float':
        """float: 'Value' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.enclosing.Value

        if temp is None:
            return None

        return temp

    @property
    def overridden(self) -> 'bool':
        """bool: 'Overridden' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.enclosing.Overridden

        if temp is None:
            return None

        return temp

    @property
    def override_value(self) -> 'float':
        """float: 'OverrideValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.enclosing.OverrideValue

        if temp is None:
            return None

        return temp

    @property
    def calculated_value(self) -> 'float':
        """float: 'CalculatedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.enclosing.CalculatedValue

        if temp is None:
            return None

        return temp


class Overridable_int(int, mixins.OverridableMixin):
    """Overridable_int

    A specific implementation of 'Overridable' for 'int' types.
    """
    __qualname__ = 'int'

    def __new__(cls, instance_to_wrap: 'Overridable_int.TYPE'):
        return int.__new__(cls, instance_to_wrap.Value if instance_to_wrap.Value is not None else 0)

    def __init__(self, instance_to_wrap: 'Overridable_int.TYPE'):
        try:
            self.enclosing = instance_to_wrap
            self.wrapped = instance_to_wrap.Value
        except (TypeError, AttributeError):
            pass

    @classmethod
    def wrapper_type(cls) -> '_OVERRIDABLE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _OVERRIDABLE

    @classmethod
    def implicit_type(cls) -> 'int':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return int

    @property
    def value(self) -> 'int':
        """int: 'Value' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.enclosing.Value

        if temp is None:
            return None

        return temp

    @property
    def overridden(self) -> 'bool':
        """bool: 'Overridden' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.enclosing.Overridden

        if temp is None:
            return None

        return temp

    @property
    def override_value(self) -> 'int':
        """int: 'OverrideValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.enclosing.OverrideValue

        if temp is None:
            return None

        return temp

    @property
    def calculated_value(self) -> 'int':
        """int: 'CalculatedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.enclosing.CalculatedValue

        if temp is None:
            return None

        return temp


class Overridable_CylindricalGearRatingMethods(mixins.OverridableMixin, Enum):
    """Overridable_CylindricalGearRatingMethods

    A specific implementation of 'Overridable' for 'CylindricalGearRatingMethods' types.
    """
    __qualname__ = 'CylindricalGearRatingMethods'

    @classmethod
    def wrapper_type(cls) -> '_OVERRIDABLE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _OVERRIDABLE

    @classmethod
    def wrapped_type(cls) -> '_227.CylindricalGearRatingMethods':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _227.CylindricalGearRatingMethods

    @classmethod
    def implicit_type(cls) -> '_227.CylindricalGearRatingMethods.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _227.CylindricalGearRatingMethods.type_()

    @property
    def value(self) -> '_227.CylindricalGearRatingMethods':
        """CylindricalGearRatingMethods: 'Value' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def overridden(self) -> 'bool':
        """bool: 'Overridden' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def override_value(self) -> '_227.CylindricalGearRatingMethods':
        """CylindricalGearRatingMethods: 'OverrideValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def calculated_value(self) -> '_227.CylindricalGearRatingMethods':
        """CylindricalGearRatingMethods: 'CalculatedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class Overridable_ISOToleranceStandard(mixins.OverridableMixin, Enum):
    """Overridable_ISOToleranceStandard

    A specific implementation of 'Overridable' for 'ISOToleranceStandard' types.
    """
    __qualname__ = 'ISOToleranceStandard'

    @classmethod
    def wrapper_type(cls) -> '_OVERRIDABLE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _OVERRIDABLE

    @classmethod
    def wrapped_type(cls) -> '_306.ISOToleranceStandard':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _306.ISOToleranceStandard

    @classmethod
    def implicit_type(cls) -> '_306.ISOToleranceStandard.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _306.ISOToleranceStandard.type_()

    @property
    def value(self) -> '_306.ISOToleranceStandard':
        """ISOToleranceStandard: 'Value' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def overridden(self) -> 'bool':
        """bool: 'Overridden' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def override_value(self) -> '_306.ISOToleranceStandard':
        """ISOToleranceStandard: 'OverrideValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def calculated_value(self) -> '_306.ISOToleranceStandard':
        """ISOToleranceStandard: 'CalculatedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class Overridable_CoefficientOfFrictionCalculationMethod(mixins.OverridableMixin, Enum):
    """Overridable_CoefficientOfFrictionCalculationMethod

    A specific implementation of 'Overridable' for 'CoefficientOfFrictionCalculationMethod' types.
    """
    __qualname__ = 'CoefficientOfFrictionCalculationMethod'

    @classmethod
    def wrapper_type(cls) -> '_OVERRIDABLE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _OVERRIDABLE

    @classmethod
    def wrapped_type(cls) -> '_291.CoefficientOfFrictionCalculationMethod':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _291.CoefficientOfFrictionCalculationMethod

    @classmethod
    def implicit_type(cls) -> '_291.CoefficientOfFrictionCalculationMethod.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _291.CoefficientOfFrictionCalculationMethod.type_()

    @property
    def value(self) -> '_291.CoefficientOfFrictionCalculationMethod':
        """CoefficientOfFrictionCalculationMethod: 'Value' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def overridden(self) -> 'bool':
        """bool: 'Overridden' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def override_value(self) -> '_291.CoefficientOfFrictionCalculationMethod':
        """CoefficientOfFrictionCalculationMethod: 'OverrideValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def calculated_value(self) -> '_291.CoefficientOfFrictionCalculationMethod':
        """CoefficientOfFrictionCalculationMethod: 'CalculatedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class Overridable_T(Generic[T], mixins.OverridableMixin):
    """Overridable_T

    A specific implementation of 'Overridable' for 'T' types.
    """
    __qualname__ = 'T'

    def __init__(self, instance_to_wrap: 'Overridable_T.TYPE'):
        try:
            self.enclosing = instance_to_wrap
            self.wrapped = instance_to_wrap.Value
        except (TypeError, AttributeError):
            pass

    @classmethod
    def wrapper_type(cls) -> '_OVERRIDABLE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _OVERRIDABLE

    @classmethod
    def implicit_type(cls) -> 'T':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return T

    @property
    def value(self) -> 'T':
        """T: 'Value' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.enclosing.Value

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def overridden(self) -> 'bool':
        """bool: 'Overridden' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.enclosing.Overridden

        if temp is None:
            return None

        return temp

    @property
    def override_value(self) -> 'T':
        """T: 'OverrideValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.enclosing.OverrideValue

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def calculated_value(self) -> 'T':
        """T: 'CalculatedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.enclosing.CalculatedValue

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None


class Overridable_bool(mixins.OverridableMixin):
    """Overridable_bool

    A specific implementation of 'Overridable' for 'bool' types.
    """
    __qualname__ = 'bool'

    def __new__(cls, instance_to_wrap: 'Overridable_bool.TYPE'):
        return bool.__new__(cls, instance_to_wrap.Value if instance_to_wrap.Value is not None else False)

    def __init__(self, instance_to_wrap: 'Overridable_bool.TYPE'):
        try:
            self.enclosing = instance_to_wrap
            self.wrapped = instance_to_wrap.Value
        except (TypeError, AttributeError):
            pass

    @classmethod
    def wrapper_type(cls) -> '_OVERRIDABLE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _OVERRIDABLE

    @classmethod
    def implicit_type(cls) -> 'bool':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return bool

    @property
    def value(self) -> 'bool':
        """bool: 'Value' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.enclosing.Value

        if temp is None:
            return None

        return temp

    @property
    def overridden(self) -> 'bool':
        """bool: 'Overridden' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.enclosing.Overridden

        if temp is None:
            return None

        return temp

    @property
    def override_value(self) -> 'bool':
        """bool: 'OverrideValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.enclosing.OverrideValue

        if temp is None:
            return None

        return temp

    @property
    def calculated_value(self) -> 'bool':
        """bool: 'CalculatedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.enclosing.CalculatedValue

        if temp is None:
            return None

        return temp

    def __bool__(self):
        return self.value


class Overridable_DiameterSeries(mixins.OverridableMixin, Enum):
    """Overridable_DiameterSeries

    A specific implementation of 'Overridable' for 'DiameterSeries' types.
    """
    __qualname__ = 'DiameterSeries'

    @classmethod
    def wrapper_type(cls) -> '_OVERRIDABLE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _OVERRIDABLE

    @classmethod
    def wrapped_type(cls) -> '_1908.DiameterSeries':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _1908.DiameterSeries

    @classmethod
    def implicit_type(cls) -> '_1908.DiameterSeries.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _1908.DiameterSeries.type_()

    @property
    def value(self) -> '_1908.DiameterSeries':
        """DiameterSeries: 'Value' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def overridden(self) -> 'bool':
        """bool: 'Overridden' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def override_value(self) -> '_1908.DiameterSeries':
        """DiameterSeries: 'OverrideValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def calculated_value(self) -> '_1908.DiameterSeries':
        """DiameterSeries: 'CalculatedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class Overridable_HeightSeries(mixins.OverridableMixin, Enum):
    """Overridable_HeightSeries

    A specific implementation of 'Overridable' for 'HeightSeries' types.
    """
    __qualname__ = 'HeightSeries'

    @classmethod
    def wrapper_type(cls) -> '_OVERRIDABLE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _OVERRIDABLE

    @classmethod
    def wrapped_type(cls) -> '_1914.HeightSeries':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _1914.HeightSeries

    @classmethod
    def implicit_type(cls) -> '_1914.HeightSeries.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _1914.HeightSeries.type_()

    @property
    def value(self) -> '_1914.HeightSeries':
        """HeightSeries: 'Value' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def overridden(self) -> 'bool':
        """bool: 'Overridden' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def override_value(self) -> '_1914.HeightSeries':
        """HeightSeries: 'OverrideValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def calculated_value(self) -> '_1914.HeightSeries':
        """HeightSeries: 'CalculatedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class Overridable_WidthSeries(mixins.OverridableMixin, Enum):
    """Overridable_WidthSeries

    A specific implementation of 'Overridable' for 'WidthSeries' types.
    """
    __qualname__ = 'WidthSeries'

    @classmethod
    def wrapper_type(cls) -> '_OVERRIDABLE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _OVERRIDABLE

    @classmethod
    def wrapped_type(cls) -> '_1931.WidthSeries':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _1931.WidthSeries

    @classmethod
    def implicit_type(cls) -> '_1931.WidthSeries.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _1931.WidthSeries.type_()

    @property
    def value(self) -> '_1931.WidthSeries':
        """WidthSeries: 'Value' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def overridden(self) -> 'bool':
        """bool: 'Overridden' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def override_value(self) -> '_1931.WidthSeries':
        """WidthSeries: 'OverrideValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def calculated_value(self) -> '_1931.WidthSeries':
        """WidthSeries: 'CalculatedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class Overridable_SealLocation(mixins.OverridableMixin, Enum):
    """Overridable_SealLocation

    A specific implementation of 'Overridable' for 'SealLocation' types.
    """
    __qualname__ = 'SealLocation'

    @classmethod
    def wrapper_type(cls) -> '_OVERRIDABLE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _OVERRIDABLE

    @classmethod
    def wrapped_type(cls) -> '_1663.SealLocation':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _1663.SealLocation

    @classmethod
    def implicit_type(cls) -> '_1663.SealLocation.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _1663.SealLocation.type_()

    @property
    def value(self) -> '_1663.SealLocation':
        """SealLocation: 'Value' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def overridden(self) -> 'bool':
        """bool: 'Overridden' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def override_value(self) -> '_1663.SealLocation':
        """SealLocation: 'OverrideValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def calculated_value(self) -> '_1663.SealLocation':
        """SealLocation: 'CalculatedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class Overridable_RigidCouplingType(mixins.OverridableMixin, Enum):
    """Overridable_RigidCouplingType

    A specific implementation of 'Overridable' for 'RigidCouplingType' types.
    """
    __qualname__ = 'RigidCouplingType'

    @classmethod
    def wrapper_type(cls) -> '_OVERRIDABLE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _OVERRIDABLE

    @classmethod
    def wrapped_type(cls) -> '_181.RigidCouplingType':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _181.RigidCouplingType

    @classmethod
    def implicit_type(cls) -> '_181.RigidCouplingType.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _181.RigidCouplingType.type_()

    @property
    def value(self) -> '_181.RigidCouplingType':
        """RigidCouplingType: 'Value' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def overridden(self) -> 'bool':
        """bool: 'Overridden' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def override_value(self) -> '_181.RigidCouplingType':
        """RigidCouplingType: 'OverrideValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def calculated_value(self) -> '_181.RigidCouplingType':
        """RigidCouplingType: 'CalculatedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class Overridable_BoundaryConditionType(mixins.OverridableMixin, Enum):
    """Overridable_BoundaryConditionType

    A specific implementation of 'Overridable' for 'BoundaryConditionType' types.
    """
    __qualname__ = 'BoundaryConditionType'

    @classmethod
    def wrapper_type(cls) -> '_OVERRIDABLE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _OVERRIDABLE

    @classmethod
    def wrapped_type(cls) -> '_157.BoundaryConditionType':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _157.BoundaryConditionType

    @classmethod
    def implicit_type(cls) -> '_157.BoundaryConditionType.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _157.BoundaryConditionType.type_()

    @property
    def value(self) -> '_157.BoundaryConditionType':
        """BoundaryConditionType: 'Value' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def overridden(self) -> 'bool':
        """bool: 'Overridden' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def override_value(self) -> '_157.BoundaryConditionType':
        """BoundaryConditionType: 'OverrideValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def calculated_value(self) -> '_157.BoundaryConditionType':
        """BoundaryConditionType: 'CalculatedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class Overridable_NodeSelectionDepthOption(mixins.OverridableMixin, Enum):
    """Overridable_NodeSelectionDepthOption

    A specific implementation of 'Overridable' for 'NodeSelectionDepthOption' types.
    """
    __qualname__ = 'NodeSelectionDepthOption'

    @classmethod
    def wrapper_type(cls) -> '_OVERRIDABLE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _OVERRIDABLE

    @classmethod
    def wrapped_type(cls) -> '_2152.NodeSelectionDepthOption':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _2152.NodeSelectionDepthOption

    @classmethod
    def implicit_type(cls) -> '_2152.NodeSelectionDepthOption.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _2152.NodeSelectionDepthOption.type_()

    @property
    def value(self) -> '_2152.NodeSelectionDepthOption':
        """NodeSelectionDepthOption: 'Value' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def overridden(self) -> 'bool':
        """bool: 'Overridden' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def override_value(self) -> '_2152.NodeSelectionDepthOption':
        """NodeSelectionDepthOption: 'OverrideValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def calculated_value(self) -> '_2152.NodeSelectionDepthOption':
        """NodeSelectionDepthOption: 'CalculatedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class Overridable_BearingEfficiencyRatingMethod(mixins.OverridableMixin, Enum):
    """Overridable_BearingEfficiencyRatingMethod

    A specific implementation of 'Overridable' for 'BearingEfficiencyRatingMethod' types.
    """
    __qualname__ = 'BearingEfficiencyRatingMethod'

    @classmethod
    def wrapper_type(cls) -> '_OVERRIDABLE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _OVERRIDABLE

    @classmethod
    def wrapped_type(cls) -> '_266.BearingEfficiencyRatingMethod':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _266.BearingEfficiencyRatingMethod

    @classmethod
    def implicit_type(cls) -> '_266.BearingEfficiencyRatingMethod.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _266.BearingEfficiencyRatingMethod.type_()

    @property
    def value(self) -> '_266.BearingEfficiencyRatingMethod':
        """BearingEfficiencyRatingMethod: 'Value' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def overridden(self) -> 'bool':
        """bool: 'Overridden' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def override_value(self) -> '_266.BearingEfficiencyRatingMethod':
        """BearingEfficiencyRatingMethod: 'OverrideValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def calculated_value(self) -> '_266.BearingEfficiencyRatingMethod':
        """BearingEfficiencyRatingMethod: 'CalculatedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class Overridable_CylindricalRollerMaxAxialLoadMethod(mixins.OverridableMixin, Enum):
    """Overridable_CylindricalRollerMaxAxialLoadMethod

    A specific implementation of 'Overridable' for 'CylindricalRollerMaxAxialLoadMethod' types.
    """
    __qualname__ = 'CylindricalRollerMaxAxialLoadMethod'

    @classmethod
    def wrapper_type(cls) -> '_OVERRIDABLE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _OVERRIDABLE

    @classmethod
    def wrapped_type(cls) -> '_1706.CylindricalRollerMaxAxialLoadMethod':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _1706.CylindricalRollerMaxAxialLoadMethod

    @classmethod
    def implicit_type(cls) -> '_1706.CylindricalRollerMaxAxialLoadMethod.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _1706.CylindricalRollerMaxAxialLoadMethod.type_()

    @property
    def value(self) -> '_1706.CylindricalRollerMaxAxialLoadMethod':
        """CylindricalRollerMaxAxialLoadMethod: 'Value' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def overridden(self) -> 'bool':
        """bool: 'Overridden' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def override_value(self) -> '_1706.CylindricalRollerMaxAxialLoadMethod':
        """CylindricalRollerMaxAxialLoadMethod: 'OverrideValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def calculated_value(self) -> '_1706.CylindricalRollerMaxAxialLoadMethod':
        """CylindricalRollerMaxAxialLoadMethod: 'CalculatedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class Overridable_ContactRatioRequirements(mixins.OverridableMixin, Enum):
    """Overridable_ContactRatioRequirements

    A specific implementation of 'Overridable' for 'ContactRatioRequirements' types.
    """
    __qualname__ = 'ContactRatioRequirements'

    @classmethod
    def wrapper_type(cls) -> '_OVERRIDABLE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _OVERRIDABLE

    @classmethod
    def wrapped_type(cls) -> '_294.ContactRatioRequirements':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _294.ContactRatioRequirements

    @classmethod
    def implicit_type(cls) -> '_294.ContactRatioRequirements.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _294.ContactRatioRequirements.type_()

    @property
    def value(self) -> '_294.ContactRatioRequirements':
        """ContactRatioRequirements: 'Value' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def overridden(self) -> 'bool':
        """bool: 'Overridden' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def override_value(self) -> '_294.ContactRatioRequirements':
        """ContactRatioRequirements: 'OverrideValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def calculated_value(self) -> '_294.ContactRatioRequirements':
        """ContactRatioRequirements: 'CalculatedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class Overridable_MicroGeometryModel(mixins.OverridableMixin, Enum):
    """Overridable_MicroGeometryModel

    A specific implementation of 'Overridable' for 'MicroGeometryModel' types.
    """
    __qualname__ = 'MicroGeometryModel'

    @classmethod
    def wrapper_type(cls) -> '_OVERRIDABLE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _OVERRIDABLE

    @classmethod
    def wrapped_type(cls) -> '_309.MicroGeometryModel':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _309.MicroGeometryModel

    @classmethod
    def implicit_type(cls) -> '_309.MicroGeometryModel.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _309.MicroGeometryModel.type_()

    @property
    def value(self) -> '_309.MicroGeometryModel':
        """MicroGeometryModel: 'Value' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def overridden(self) -> 'bool':
        """bool: 'Overridden' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def override_value(self) -> '_309.MicroGeometryModel':
        """MicroGeometryModel: 'OverrideValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def calculated_value(self) -> '_309.MicroGeometryModel':
        """MicroGeometryModel: 'CalculatedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class Overridable_UnbalancedMassInclusionOption(mixins.OverridableMixin, Enum):
    """Overridable_UnbalancedMassInclusionOption

    A specific implementation of 'Overridable' for 'UnbalancedMassInclusionOption' types.
    """
    __qualname__ = 'UnbalancedMassInclusionOption'

    @classmethod
    def wrapper_type(cls) -> '_OVERRIDABLE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _OVERRIDABLE

    @classmethod
    def wrapped_type(cls) -> '_2228.UnbalancedMassInclusionOption':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _2228.UnbalancedMassInclusionOption

    @classmethod
    def implicit_type(cls) -> '_2228.UnbalancedMassInclusionOption.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _2228.UnbalancedMassInclusionOption.type_()

    @property
    def value(self) -> '_2228.UnbalancedMassInclusionOption':
        """UnbalancedMassInclusionOption: 'Value' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def overridden(self) -> 'bool':
        """bool: 'Overridden' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def override_value(self) -> '_2228.UnbalancedMassInclusionOption':
        """UnbalancedMassInclusionOption: 'OverrideValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def calculated_value(self) -> '_2228.UnbalancedMassInclusionOption':
        """UnbalancedMassInclusionOption: 'CalculatedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class Overridable_FrictionModelForGyroscopicMoment(mixins.OverridableMixin, Enum):
    """Overridable_FrictionModelForGyroscopicMoment

    A specific implementation of 'Overridable' for 'FrictionModelForGyroscopicMoment' types.
    """
    __qualname__ = 'FrictionModelForGyroscopicMoment'

    @classmethod
    def wrapper_type(cls) -> '_OVERRIDABLE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _OVERRIDABLE

    @classmethod
    def wrapped_type(cls) -> '_1734.FrictionModelForGyroscopicMoment':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _1734.FrictionModelForGyroscopicMoment

    @classmethod
    def implicit_type(cls) -> '_1734.FrictionModelForGyroscopicMoment.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _1734.FrictionModelForGyroscopicMoment.type_()

    @property
    def value(self) -> '_1734.FrictionModelForGyroscopicMoment':
        """FrictionModelForGyroscopicMoment: 'Value' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def overridden(self) -> 'bool':
        """bool: 'Overridden' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def override_value(self) -> '_1734.FrictionModelForGyroscopicMoment':
        """FrictionModelForGyroscopicMoment: 'OverrideValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def calculated_value(self) -> '_1734.FrictionModelForGyroscopicMoment':
        """FrictionModelForGyroscopicMoment: 'CalculatedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class Overridable_RollerAnalysisMethod(mixins.OverridableMixin, Enum):
    """Overridable_RollerAnalysisMethod

    A specific implementation of 'Overridable' for 'RollerAnalysisMethod' types.
    """
    __qualname__ = 'RollerAnalysisMethod'

    @classmethod
    def wrapper_type(cls) -> '_OVERRIDABLE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _OVERRIDABLE

    @classmethod
    def wrapped_type(cls) -> '_1828.RollerAnalysisMethod':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _1828.RollerAnalysisMethod

    @classmethod
    def implicit_type(cls) -> '_1828.RollerAnalysisMethod.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _1828.RollerAnalysisMethod.type_()

    @property
    def value(self) -> '_1828.RollerAnalysisMethod':
        """RollerAnalysisMethod: 'Value' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def overridden(self) -> 'bool':
        """bool: 'Overridden' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def override_value(self) -> '_1828.RollerAnalysisMethod':
        """RollerAnalysisMethod: 'OverrideValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def calculated_value(self) -> '_1828.RollerAnalysisMethod':
        """RollerAnalysisMethod: 'CalculatedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class Overridable_HelicalGearMicroGeometryOption(mixins.OverridableMixin, Enum):
    """Overridable_HelicalGearMicroGeometryOption

    A specific implementation of 'Overridable' for 'HelicalGearMicroGeometryOption' types.
    """
    __qualname__ = 'HelicalGearMicroGeometryOption'

    @classmethod
    def wrapper_type(cls) -> '_OVERRIDABLE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _OVERRIDABLE

    @classmethod
    def wrapped_type(cls) -> '_477.HelicalGearMicroGeometryOption':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _477.HelicalGearMicroGeometryOption

    @classmethod
    def implicit_type(cls) -> '_477.HelicalGearMicroGeometryOption.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _477.HelicalGearMicroGeometryOption.type_()

    @property
    def value(self) -> '_477.HelicalGearMicroGeometryOption':
        """HelicalGearMicroGeometryOption: 'Value' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def overridden(self) -> 'bool':
        """bool: 'Overridden' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def override_value(self) -> '_477.HelicalGearMicroGeometryOption':
        """HelicalGearMicroGeometryOption: 'OverrideValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def calculated_value(self) -> '_477.HelicalGearMicroGeometryOption':
        """HelicalGearMicroGeometryOption: 'CalculatedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class Overridable_EfficiencyRatingMethod(mixins.OverridableMixin, Enum):
    """Overridable_EfficiencyRatingMethod

    A specific implementation of 'Overridable' for 'EfficiencyRatingMethod' types.
    """
    __qualname__ = 'EfficiencyRatingMethod'

    @classmethod
    def wrapper_type(cls) -> '_OVERRIDABLE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _OVERRIDABLE

    @classmethod
    def wrapped_type(cls) -> '_268.EfficiencyRatingMethod':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _268.EfficiencyRatingMethod

    @classmethod
    def implicit_type(cls) -> '_268.EfficiencyRatingMethod.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _268.EfficiencyRatingMethod.type_()

    @property
    def value(self) -> '_268.EfficiencyRatingMethod':
        """EfficiencyRatingMethod: 'Value' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def overridden(self) -> 'bool':
        """bool: 'Overridden' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def override_value(self) -> '_268.EfficiencyRatingMethod':
        """EfficiencyRatingMethod: 'OverrideValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def calculated_value(self) -> '_268.EfficiencyRatingMethod':
        """EfficiencyRatingMethod: 'CalculatedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class Overridable_MeshStiffnessSource(mixins.OverridableMixin, Enum):
    """Overridable_MeshStiffnessSource

    A specific implementation of 'Overridable' for 'MeshStiffnessSource' types.
    """
    __qualname__ = 'MeshStiffnessSource'

    @classmethod
    def wrapper_type(cls) -> '_OVERRIDABLE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _OVERRIDABLE

    @classmethod
    def wrapped_type(cls) -> '_6649.MeshStiffnessSource':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _6649.MeshStiffnessSource

    @classmethod
    def implicit_type(cls) -> '_6649.MeshStiffnessSource.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _6649.MeshStiffnessSource.type_()

    @property
    def value(self) -> '_6649.MeshStiffnessSource':
        """MeshStiffnessSource: 'Value' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def overridden(self) -> 'bool':
        """bool: 'Overridden' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def override_value(self) -> '_6649.MeshStiffnessSource':
        """MeshStiffnessSource: 'OverrideValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def calculated_value(self) -> '_6649.MeshStiffnessSource':
        """MeshStiffnessSource: 'CalculatedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None
