"""_974.py

CylindricalGearDefaults
"""


from mastapy._internal.python_net import python_net_import
from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.gears.gear_designs.cylindrical.thickness_stock_and_backlash import _1050
from mastapy.gears.gear_designs.cylindrical import _1008
from mastapy.gears.manufacturing.cylindrical.cutter_simulation import _708
from mastapy.gears.manufacturing.cylindrical.cutters import _688
from mastapy.gears.gear_designs.cylindrical.accuracy_and_tolerances import _1095
from mastapy.utility import _1395

_DATABASE_WITH_SELECTED_ITEM = python_net_import('SMT.MastaAPI.UtilityGUI.Databases', 'DatabaseWithSelectedItem')
_CYLINDRICAL_GEAR_DEFAULTS = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'CylindricalGearDefaults')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearDefaults',)


class CylindricalGearDefaults(_1395.PerMachineSettings):
    """CylindricalGearDefaults

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_GEAR_DEFAULTS

    def __init__(self, instance_to_wrap: 'CylindricalGearDefaults.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def agma_material(self) -> 'str':
        """str: 'AGMAMaterial' is the original name of this property."""

        temp = self.wrapped.AGMAMaterial.SelectedItemName

        if temp is None:
            return None

        return temp

    @agma_material.setter
    def agma_material(self, value: 'str'):
        self.wrapped.AGMAMaterial.SetSelectedItem(str(value) if value else '')

    @property
    def chamfer_angle(self) -> 'float':
        """float: 'ChamferAngle' is the original name of this property."""

        temp = self.wrapped.ChamferAngle

        if temp is None:
            return None

        return temp

    @chamfer_angle.setter
    def chamfer_angle(self, value: 'float'):
        self.wrapped.ChamferAngle = float(value) if value else 0.0

    @property
    def diameter_chamfer_height(self) -> 'float':
        """float: 'DiameterChamferHeight' is the original name of this property."""

        temp = self.wrapped.DiameterChamferHeight

        if temp is None:
            return None

        return temp

    @diameter_chamfer_height.setter
    def diameter_chamfer_height(self, value: 'float'):
        self.wrapped.DiameterChamferHeight = float(value) if value else 0.0

    @property
    def fillet_roughness(self) -> 'float':
        """float: 'FilletRoughness' is the original name of this property."""

        temp = self.wrapped.FilletRoughness

        if temp is None:
            return None

        return temp

    @fillet_roughness.setter
    def fillet_roughness(self, value: 'float'):
        self.wrapped.FilletRoughness = float(value) if value else 0.0

    @property
    def finish_stock_type(self) -> '_1050.FinishStockType':
        """FinishStockType: 'FinishStockType' is the original name of this property."""

        temp = self.wrapped.FinishStockType

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1050.FinishStockType)(value) if value is not None else None

    @finish_stock_type.setter
    def finish_stock_type(self, value: '_1050.FinishStockType'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.FinishStockType = value

    @property
    def flank_roughness(self) -> 'float':
        """float: 'FlankRoughness' is the original name of this property."""

        temp = self.wrapped.FlankRoughness

        if temp is None:
            return None

        return temp

    @flank_roughness.setter
    def flank_roughness(self, value: 'float'):
        self.wrapped.FlankRoughness = float(value) if value else 0.0

    @property
    def gear_fit_system(self) -> '_1008.GearFitSystems':
        """GearFitSystems: 'GearFitSystem' is the original name of this property."""

        temp = self.wrapped.GearFitSystem

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1008.GearFitSystems)(value) if value is not None else None

    @gear_fit_system.setter
    def gear_fit_system(self, value: '_1008.GearFitSystems'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.GearFitSystem = value

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
    def iso_quality_grade(self) -> 'int':
        """int: 'ISOQualityGrade' is the original name of this property."""

        temp = self.wrapped.ISOQualityGrade

        if temp is None:
            return None

        return temp

    @iso_quality_grade.setter
    def iso_quality_grade(self, value: 'int'):
        self.wrapped.ISOQualityGrade = int(value) if value else 0

    @property
    def finish_manufacturing_process_controls(self) -> '_708.ManufacturingProcessControls':
        """ManufacturingProcessControls: 'FinishManufacturingProcessControls' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FinishManufacturingProcessControls

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def rough_cutter_creation_settings(self) -> '_688.RoughCutterCreationSettings':
        """RoughCutterCreationSettings: 'RoughCutterCreationSettings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RoughCutterCreationSettings

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def rough_manufacturing_process_controls(self) -> '_708.ManufacturingProcessControls':
        """ManufacturingProcessControls: 'RoughManufacturingProcessControls' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RoughManufacturingProcessControls

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def system_of_fits_defaults(self) -> '_1095.DIN3967SystemOfGearFits':
        """DIN3967SystemOfGearFits: 'SystemOfFitsDefaults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SystemOfFitsDefaults

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
